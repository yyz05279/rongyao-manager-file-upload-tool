# API 配置说明

## API Base URL 配置

### 当前配置

**生产环境 API 地址**: `http://42.192.76.234:8081`

### 配置位置

#### 1. 后端配置（Rust/Tauri）

**文件**: `tauri-app/src-tauri/src/main.rs`

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .manage(AppState {
            auth_service: Arc::new(Mutex::new(None)),
            token: Arc::new(Mutex::new(None)),
            refresh_token: Arc::new(Mutex::new(None)),
            api_base_url: "http://42.192.76.234:8081".to_string(),  // ✅ 生产环境地址
        })
        // ...
}
```

**说明**:
- 这是 Tauri 后端的全局 API 配置
- 所有通过 Tauri 命令调用的 API 都使用此地址
- 包括：登录、刷新 Token、获取项目信息、上传文件等

#### 2. 前端配置（React）

**文件**: `tauri-app/src/components/LoginForm.jsx`

```javascript
const API_URL = "http://42.192.76.234:8081";  // ✅ 生产环境地址
```

**说明**:
- 登录时传递给后端的 API URL
- 用于初始化 AuthService

### API 端点清单

基于配置的 base URL，所有 API 端点如下：

| 功能 | 方法 | 端点 | 完整 URL |
|------|------|------|----------|
| 用户登录 | POST | `/api/v1/auth/login` | `http://42.192.76.234:8081/api/v1/auth/login` |
| 刷新 Token | POST | `/api/v1/auth/refresh` | `http://42.192.76.234:8081/api/v1/auth/refresh` |
| 获取项目信息 | GET | `/api/v1/projects/my-project` | `http://42.192.76.234:8081/api/v1/projects/my-project` |
| 批量上传日报 | POST | `/api/v1/daily-reports/batch-import` | `http://42.192.76.234:8081/api/v1/daily-reports/batch-import` |

### 修改历史

#### 2025-10-26
- ✅ 将后端 `api_base_url` 从 `http://localhost:3000` 修改为 `http://42.192.76.234:8081`
- ✅ 前端已配置为 `http://42.192.76.234:8081`

#### 原配置
```rust
// ❌ 旧配置（本地开发）
api_base_url: "http://localhost:3000".to_string(),
```

#### 当前配置
```rust
// ✅ 新配置（生产环境）
api_base_url: "http://42.192.76.234:8081".to_string(),
```

### 环境切换指南

如需在不同环境之间切换，请修改以下两处：

#### 本地开发环境

1. **后端**: `tauri-app/src-tauri/src/main.rs` (第 143 行)
```rust
api_base_url: "http://localhost:3000".to_string(),
```

2. **前端**: `tauri-app/src/components/LoginForm.jsx` (第 6 行)
```javascript
const API_URL = "http://localhost:3000";
```

#### 生产环境

1. **后端**: `tauri-app/src-tauri/src/main.rs` (第 143 行)
```rust
api_base_url: "http://42.192.76.234:8081".to_string(),
```

2. **前端**: `tauri-app/src/components/LoginForm.jsx` (第 6 行)
```javascript
const API_URL = "http://42.192.76.234:8081";
```

### 配置验证

修改后可以通过以下方式验证配置是否正确：

#### 1. 编译检查
```bash
cd tauri-app/src-tauri
cargo check
```

应该看到：
```
✅ Checking molten-salt-upload v0.1.0
✅ Finished `dev` profile
```

#### 2. 运行时检查

启动应用并尝试登录：
```bash
cd tauri-app
npm run tauri dev
```

登录时查看终端日志：
```
🔐 [cmd_login] 开始登录流程
🔐 [AuthService] 登录 URL: http://42.192.76.234:8081/api/v1/auth/login
✅ [cmd_login] 登录成功
```

#### 3. 项目信息获取检查

登录后查看终端日志：
```
🔍 [ProjectService] 开始获取项目信息
  - URL: http://42.192.76.234:8081/api/v1/projects/my-project
✅ [ProjectService] 项目信息解析成功
```

### 注意事项

1. **CORS 配置**: 确保后端 API 服务器允许来自 Tauri 应用的跨域请求
2. **网络连接**: 确保客户端能够访问 `42.192.76.234:8081`
3. **防火墙规则**: 检查防火墙是否允许访问该 IP 和端口
4. **SSL/TLS**: 当前使用 HTTP，如需安全连接可切换到 HTTPS

### 优化建议

#### 使用环境变量

可以考虑使用环境变量来配置 API URL，避免硬编码：

**Rust 端**:
```rust
// 在 main.rs 中
let api_base_url = std::env::var("API_BASE_URL")
    .unwrap_or_else(|_| "http://42.192.76.234:8081".to_string());

.manage(AppState {
    api_base_url,
    // ...
})
```

**React 端**:
```javascript
// 在 LoginForm.jsx 中
const API_URL = import.meta.env.VITE_API_URL || "http://42.192.76.234:8081";
```

**配置文件**:
```bash
# .env
VITE_API_URL=http://42.192.76.234:8081
```

#### 配置文件方案

创建配置文件 `config.json`:
```json
{
  "apiBaseUrl": "http://42.192.76.234:8081",
  "environment": "production"
}
```

在应用启动时读取配置文件。

### 故障排查

#### 问题 1: 连接失败

**症状**: 登录时提示"网络错误"或"连接超时"

**解决方案**:
1. 检查网络连接
2. 使用浏览器访问 `http://42.192.76.234:8081` 确认服务器可达
3. 检查防火墙设置

#### 问题 2: 401 未授权

**症状**: 登录后的 API 调用返回 401

**解决方案**:
1. 检查 Token 是否正确保存
2. 查看终端日志确认 Token 已传递
3. 验证后端 Token 验证逻辑

#### 问题 3: 跨域错误

**症状**: 浏览器控制台显示 CORS 错误

**解决方案**:
1. 后端需要配置 CORS 允许来自 Tauri 的请求
2. 检查 `Access-Control-Allow-Origin` 响应头

### 测试清单

- [x] 修改后端 API URL
- [x] 验证前端 API URL 配置
- [x] Rust 代码编译检查通过
- [ ] 登录功能测试
- [ ] 项目信息获取测试
- [ ] 文件上传功能测试
- [ ] Token 刷新功能测试

### 总结

✅ **API Base URL 已成功配置为**: `http://42.192.76.234:8081`

**涉及的文件**:
1. `tauri-app/src-tauri/src/main.rs` - 后端全局配置
2. `tauri-app/src/components/LoginForm.jsx` - 前端登录配置

**下次启动应用时，所有 API 请求都将发送到生产环境服务器！** 🚀

