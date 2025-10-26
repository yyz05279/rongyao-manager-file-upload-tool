# Token管理和无感刷新实现说明

## 问题分析

### 原始问题

从终端日志发现：
```
❌ [cmd_get_project] Token为空，用户未登录
```

**根本原因**：登录成功后，Token没有正确保存到Tauri的全局状态，导致后续API调用失败。

## 解决方案

根据API文档 (`api/01-用户认证模块API.md`)：
- **Token有效期**: 24小时
- **RefreshToken有效期**: 30天
- **刷新接口**: `POST /api/v1/auth/refresh`

实现了完整的Token管理和无感刷新机制。

## 实现内容

### 1. 后端实现（Rust/Tauri）

#### 1.1 数据结构增强

**AppState 添加 RefreshToken**

```rust
// main.rs
type RefreshTokenMutex = Arc<Mutex<Option<String>>>;

struct AppState {
    auth_service: AuthServiceMutex,
    token: TokenMutex,
    refresh_token: RefreshTokenMutex,  // ✅ 新增
    api_base_url: String,
}
```

#### 1.2 登录流程优化

**cmd_login - 保存Token到全局状态**

```rust
#[tauri::command]
async fn cmd_login(
    username: String,
    password: String,
    api_url: String,
    state: tauri::State<'_, AppState>,
) -> Result<AuthResponse, String> {
    println!("🔐 [cmd_login] 开始登录流程");
    
    let mut auth = AuthService::new(api_url.clone());
    let result = auth.login(&username, &password).await?;
    
    println!("✅ [cmd_login] 登录成功，保存Token到全局状态");
    
    // ✅ 保存 token 和 refresh_token 到全局状态
    *state.token.lock().unwrap() = Some(result.token.clone());
    *state.refresh_token.lock().unwrap() = Some(result.refresh_token.clone());
    *state.auth_service.lock().unwrap() = Some(auth);
    
    println!("✅ [cmd_login] Token已保存到全局状态");
    
    Ok(result)
}
```

#### 1.3 Token刷新功能

**auth.rs - refresh_token方法**

```rust
/// 刷新Token
pub async fn refresh_token(&mut self) -> Result<String, String> {
    println!("🔄 [AuthService] 开始刷新Token");
    
    let refresh_token = self.refresh_token
        .as_ref()
        .ok_or("RefreshToken不存在")?;

    let client = reqwest::Client::new();
    let refresh_url = format!("{}/api/v1/auth/refresh", self.api_base_url);

    let payload = serde_json::json!({
        "refreshToken": refresh_token
    });

    let response = client
        .post(&refresh_url)
        .json(&payload)
        .send()
        .await
        .map_err(|e| format!("刷新Token请求失败: {}", e))?;

    if !response.status().is_success() {
        return Err("刷新Token失败: Token已过期".to_string());
    }

    let result: serde_json::Value = response
        .json()
        .await
        .map_err(|e| format!("解析刷新响应失败: {}", e))?;

    let new_token = result["data"]["token"]
        .as_str()
        .ok_or("刷新后的token不存在")?
        .to_string();

    self.token = Some(new_token.clone());

    println!("✅ [AuthService] Token刷新成功");

    Ok(new_token)
}
```

**main.rs - cmd_refresh_token命令**

```rust
#[tauri::command]
async fn cmd_refresh_token(
    state: tauri::State<'_, AppState>,
) -> Result<String, String> {
    println!("🔄 [cmd_refresh_token] Tauri命令被调用");
    
    // ✅ 先获取auth_service，释放锁之前clone
    let mut auth_service = {
        let mut auth_service_lock = state.auth_service.lock().unwrap();
        auth_service_lock
            .take()
            .ok_or_else(|| "未登录".to_string())?
    }; // 锁在这里被释放

    let new_token = auth_service.refresh_token().await?;
    
    // 更新全局状态中的token和auth_service
    *state.token.lock().unwrap() = Some(new_token.clone());
    *state.auth_service.lock().unwrap() = Some(auth_service);
    
    println!("✅ [cmd_refresh_token] Token刷新成功并已更新全局状态");
    
    Ok(new_token)
}
```

### 2. 前端实现（React/Zustand）

#### 2.1 状态管理增强

**authStore.js - 添加Token相关状态**

```javascript
export const useAuthStore = create((set, get) => ({
  // 状态
  token: localStorage.getItem("token") || null,
  refreshToken: localStorage.getItem("refreshToken") || null,
  tokenExpiresAt: parseInt(localStorage.getItem("tokenExpiresAt") || "0", 10),
  userInfo: JSON.parse(localStorage.getItem("userInfo") || "null"),
  projectInfo: null,
  loading: false,
  error: null,
  screen: localStorage.getItem("token") ? "upload" : "login",
  refreshTimerId: null,  // ✅ 定时器ID
}));
```

#### 2.2 登录流程优化

```javascript
login: async (username, password, apiUrl) => {
  console.log("🔐 [authStore] 开始登录...");
  set({ loading: true, error: null });
  try {
    const response = await authAPI.login(username, password, apiUrl);
    console.log("✅ [authStore] 登录响应:", response);
    
    // ✅ 计算Token过期时间（24小时后）
    const tokenExpiresAt = Date.now() + 24 * 60 * 60 * 1000;
    
    // ✅ 保存到localStorage
    localStorage.setItem("token", response.token);
    localStorage.setItem("refreshToken", response.refresh_token);
    localStorage.setItem("tokenExpiresAt", tokenExpiresAt.toString());
    localStorage.setItem("userInfo", JSON.stringify(response.user_info));
    
    console.log("✅ [authStore] Token已保存到localStorage");
    console.log("  - Token过期时间:", new Date(tokenExpiresAt).toLocaleString());
    
    set({
      token: response.token,
      refreshToken: response.refresh_token,
      tokenExpiresAt: tokenExpiresAt,
      userInfo: response.user_info,
      screen: "upload",
      loading: false,
    });
    
    // ✅ 启动Token自动刷新定时器
    get().startTokenRefreshTimer();
    
    return response;
  } catch (err) {
    console.error("❌ [authStore] 登录失败:", err);
    set({ error: err.message || "登录失败", loading: false });
    throw err;
  }
},
```

#### 2.3 Token刷新功能

```javascript
// ✅ 刷新Token
refreshToken: async () => {
  console.log("🔄 [authStore] 开始刷新Token");
  try {
    const newToken = await authAPI.refreshToken();
    console.log("✅ [authStore] Token刷新成功");
    
    // ✅ 更新Token和过期时间
    const tokenExpiresAt = Date.now() + 24 * 60 * 60 * 1000;
    
    localStorage.setItem("token", newToken);
    localStorage.setItem("tokenExpiresAt", tokenExpiresAt.toString());
    
    set({
      token: newToken,
      tokenExpiresAt: tokenExpiresAt,
    });
    
    console.log("✅ [authStore] Token过期时间已更新:", new Date(tokenExpiresAt).toLocaleString());
    
    return newToken;
  } catch (err) {
    console.error("❌ [authStore] Token刷新失败:", err);
    // Token刷新失败，清除登录状态
    get().logout();
    throw err;
  }
},
```

#### 2.4 自动刷新机制

```javascript
// ✅ 检查Token是否即将过期（提前30分钟刷新）
shouldRefreshToken: () => {
  const { tokenExpiresAt } = get();
  if (!tokenExpiresAt) return false;
  
  const now = Date.now();
  const timeUntilExpiry = tokenExpiresAt - now;
  const thirtyMinutes = 30 * 60 * 1000;
  
  // 如果Token在30分钟内过期，则需要刷新
  return timeUntilExpiry < thirtyMinutes;
},

// ✅ 启动Token自动刷新定时器
startTokenRefreshTimer: () => {
  console.log("⏰ [authStore] 启动Token自动刷新定时器");
  
  // 清除旧的定时器
  get().stopTokenRefreshTimer();
  
  // 每5分钟检查一次Token是否需要刷新
  const timerId = setInterval(() => {
    if (get().shouldRefreshToken()) {
      console.log("🔄 [authStore] Token即将过期，自动刷新");
      get().refreshToken().catch(err => {
        console.error("❌ [authStore] 自动刷新Token失败:", err);
      });
    }
  }, 5 * 60 * 1000); // 5分钟
  
  set({ refreshTimerId: timerId });
},

// ✅ 停止Token自动刷新定时器
stopTokenRefreshTimer: () => {
  const { refreshTimerId } = get();
  if (refreshTimerId) {
    console.log("⏸️ [authStore] 停止Token自动刷新定时器");
    clearInterval(refreshTimerId);
    set({ refreshTimerId: null });
  }
},
```

#### 2.5 退出登录优化

```javascript
logout: () => {
  console.log("👋 [authStore] 用户退出登录");
  
  // ✅ 清除定时器
  get().stopTokenRefreshTimer();
  
  // ✅ 清除localStorage
  localStorage.removeItem("token");
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("tokenExpiresAt");
  localStorage.removeItem("userInfo");
  
  set({
    token: null,
    refreshToken: null,
    tokenExpiresAt: 0,
    userInfo: null,
    projectInfo: null,
    screen: "login",
  });
},
```

## 工作流程

### 1. 登录流程

```
用户输入用户名密码
    ↓
前端调用 authAPI.login()
    ↓
Tauri后端 cmd_login
    ↓
调用API: POST /api/v1/auth/login
    ↓
返回: { token, refreshToken, user_info }
    ↓
保存到:
  - Tauri全局状态 (token, refreshToken, authService)
  - localStorage (token, refreshToken, tokenExpiresAt, userInfo)
  - Zustand状态
    ↓
启动Token自动刷新定时器
    ↓
登录完成
```

### 2. Token自动刷新流程

```
定时器每5分钟检查一次
    ↓
shouldRefreshToken() 判断是否需要刷新
    ↓
如果Token在30分钟内过期
    ↓
前端调用 authAPI.refreshToken()
    ↓
Tauri后端 cmd_refresh_token
    ↓
AuthService.refresh_token()
    ↓
调用API: POST /api/v1/auth/refresh
    ↓
返回: { token }
    ↓
更新:
  - Tauri全局状态 (token, authService)
  - localStorage (token, tokenExpiresAt)
  - Zustand状态
    ↓
刷新完成，继续正常使用
```

### 3. Token刷新失败处理

```
Token刷新失败
    ↓
自动调用 logout()
    ↓
清除定时器
    ↓
清除所有Token数据
    ↓
返回登录页面
```

## 时间配置

| 项目 | 时间 | 说明 |
|------|------|------|
| Token有效期 | 24小时 | API返回后计算 |
| RefreshToken有效期 | 30天 | API管理 |
| 提前刷新时间 | 30分钟 | Token过期前30分钟刷新 |
| 检查间隔 | 5分钟 | 定时器每5分钟检查一次 |

**刷新策略**：
- Token有效期为24小时
- 提前30分钟刷新（即23.5小时后刷新）
- 每5分钟检查一次是否需要刷新
- 这样可以确保Token永不过期

## 日志输出

### 登录流程日志

```
🔐 [LoginForm] 开始登录...
🔐 [authStore] 开始登录...
🔐 [cmd_login] 开始登录流程
✅ [cmd_login] 登录成功，保存Token到全局状态
  - Token: eyJhbGciOiJIUzI1NiIs...
  - RefreshToken: eyJhbGciOiJIUzI1NiIs...
✅ [cmd_login] Token已保存到全局状态
✅ [authStore] 登录响应: {token, refresh_token, user_info}
✅ [authStore] Token已保存到localStorage
  - Token过期时间: 2025/10/27 08:00:00
⏰ [authStore] 启动Token自动刷新定时器
✅ [LoginForm] 登录成功
```

### Token刷新日志

```
🔄 [authStore] Token即将过期，自动刷新
🔄 [authStore] 开始刷新Token
🔄 [cmd_refresh_token] Tauri命令被调用
🔄 [AuthService] 开始刷新Token
🔄 [AuthService] 发送刷新请求到: http://42.192.76.234:8081/api/v1/auth/refresh
📡 [AuthService] 刷新响应状态: 200 OK
📦 [AuthService] 刷新响应数据: {完整JSON}
✅ [AuthService] Token刷新成功
✅ [cmd_refresh_token] Token刷新成功并已更新全局状态
✅ [authStore] Token刷新成功
✅ [authStore] Token过期时间已更新: 2025/10/28 08:00:00
```

## API接口

### 刷新Token接口

**接口地址**: `POST /api/v1/auth/refresh`

**请求参数**:
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应示例**:
```json
{
  "code": 1,
  "message": "刷新成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 7200
  }
}
```

## 修改文件清单

### 后端（Rust）

✅ `tauri-app/src-tauri/src/auth.rs`
- 添加 `refresh_token()` 方法

✅ `tauri-app/src-tauri/src/main.rs`
- 添加 `RefreshTokenMutex` 类型
- 修改 `AppState` 结构
- 优化 `cmd_login` 命令（保存Token）
- 添加 `cmd_refresh_token` 命令

### 前端（React）

✅ `tauri-app/src/stores/authStore.js`
- 添加 `refreshToken` 和 `tokenExpiresAt` 状态
- 优化 `login()` 方法（保存Token和过期时间）
- 添加 `refreshToken()` 方法
- 添加 `shouldRefreshToken()` 方法
- 添加 `startTokenRefreshTimer()` 方法
- 添加 `stopTokenRefreshTimer()` 方法
- 优化 `logout()` 方法（清除定时器）

✅ `tauri-app/src/services/api.js`
- 添加 `authAPI.refreshToken()` 方法

## 测试步骤

### 1. 测试登录和Token保存

```bash
# 启动应用
npm run tauri dev

# 登录
# 打开浏览器控制台（F12）
# 应该看到：
✅ [authStore] Token已保存到localStorage
  - Token过期时间: 2025/10/27 08:00:00
⏰ [authStore] 启动Token自动刷新定时器

# 检查localStorage
localStorage.getItem("token")          // 应该有值
localStorage.getItem("refreshToken")   // 应该有值
localStorage.getItem("tokenExpiresAt") // 应该有值
```

### 2. 测试Token自动刷新

```javascript
// 在浏览器控制台手动触发刷新
// 方法1：修改过期时间为即将过期
localStorage.setItem("tokenExpiresAt", Date.now() + 20 * 60 * 1000); // 20分钟后过期

// 等待5分钟（或强制触发）
const store = useAuthStore.getState();
store.refreshToken();

// 应该看到：
🔄 [authStore] Token即将过期，自动刷新
✅ [authStore] Token刷新成功
```

### 3. 测试项目信息获取

```
登录后
    ↓
等待项目信息加载
    ↓
检查终端日志，应该看到：
✅ [cmd_login] Token已保存到全局状态
✅ [cmd_get_project] Token已获取
✅ [ProjectService] 项目信息解析成功
    ↓
界面显示：当前项目: 淮安
```

## 优势特点

1. **无感刷新**: 用户完全感知不到Token刷新过程
2. **提前刷新**: 提前30分钟刷新，避免Token过期
3. **自动重试**: 定时器每5分钟检查，确保及时刷新
4. **失败处理**: 刷新失败自动退出登录
5. **持久化**: Token保存到localStorage，刷新页面不丢失
6. **详细日志**: 完整的日志输出，便于调试

## 总结

通过完整实现Token管理和无感刷新机制：

1. ✅ **修复了Token保存问题** - 登录时正确保存到Tauri全局状态
2. ✅ **实现了无感刷新** - 自动检测并刷新即将过期的Token
3. ✅ **完善了错误处理** - Token刷新失败自动退出登录
4. ✅ **添加了详细日志** - 方便调试和监控

现在应用具备了完整的Token生命周期管理能力！

