# Token 持久化问题修复说明

## 问题描述

用户登录后，token 信息没有正确持久化，导致以下问题：

- 前端从 localStorage 恢复 token（持久化存储）
- 后端 Rust 全局状态中没有 token（内存存储，应用重启后丢失）
- 前端认为已登录，但后端返回"未登录"错误

终端错误日志：

```
🔍 [cmd_get_project] Tauri命令被调用
❌ [cmd_get_project] Token为空，用户未登录
```

## 问题根因

**架构矛盾**：

1. **前端状态管理**：使用 localStorage 持久化存储 token，页面刷新后能恢复
2. **后端状态管理**：使用 Rust 全局内存状态存储 token，应用重启后丢失
3. **状态不同步**：前端有 token，后端没有 token，导致 API 调用失败

## 解决方案

采用**无状态架构**，前端在每次调用后端命令时传递 token，后端不维护全局 token 状态。

### 修改内容

#### 1. 修改 Rust 命令签名（添加 token 参数）

**文件：`src-tauri/src/main.rs`**

```rust
// ✅ cmd_get_project：添加token参数
#[tauri::command]
async fn cmd_get_project(
    token: String,  // 新增
    state: tauri::State<'_, AppState>,
) -> Result<project::ProjectInfo, String>

// ✅ cmd_upload_file：添加token参数
#[tauri::command]
async fn cmd_upload_file(
    file_path: String,
    project_id: i32,
    reporter_id: i32,
    token: String,  // 新增
    state: tauri::State<'_, AppState>,
) -> Result<String, String>

// ✅ cmd_refresh_token：添加refreshToken参数
#[tauri::command]
async fn cmd_refresh_token(
    refresh_token: String,  // 新增
    state: tauri::State<'_, AppState>,
) -> Result<String, String>
```

#### 2. 修改 AuthService 支持 refresh_token 场景

**文件：`src-tauri/src/auth.rs`**

```rust
/// 创建带有refresh_token的实例（用于刷新token场景）
pub fn with_refresh_token(api_base_url: String, refresh_token: String) -> Self {
    Self {
        api_base_url,
        token: None,
        refresh_token: Some(refresh_token),
    }
}
```

#### 3. 修改前端 API 调用（传递 token）

**文件：`src/services/api.js`**

```javascript
export const authAPI = {
  login: (username, password, apiUrl) =>
    safeInvoke("cmd_login", { username, password, apiUrl }),

  refreshToken: (
    refreshToken // ✅ 添加refreshToken参数
  ) => safeInvoke("cmd_refresh_token", { refreshToken }),
};

export const projectAPI = {
  getMyProject: (
    token // ✅ 添加token参数
  ) => safeInvoke("cmd_get_project", { token }),
};

export const uploadAPI = {
  uploadFile: (
    filePath,
    projectId,
    reporterId,
    token // ✅ 添加token参数
  ) =>
    safeInvoke("cmd_upload_file", { filePath, projectId, reporterId, token }),
};
```

#### 4. 修改 authStore 传递 token

**文件：`src/stores/authStore.js`**

```javascript
// ✅ getProject：从状态中获取token并传递
getProject: async () => {
  const { token } = get();

  if (!token) {
    throw new Error("未登录，无法获取项目信息");
  }

  const projectInfo = await projectAPI.getMyProject(token);
  set({ projectInfo, loading: false });
  return projectInfo;
},

// ✅ refreshToken：从状态中获取refreshToken并传递
refreshToken: async () => {
  const { refreshToken } = get();

  if (!refreshToken) {
    throw new Error("RefreshToken不存在");
  }

  const newToken = await authAPI.refreshToken(refreshToken);
  // 更新localStorage和状态
  localStorage.setItem("token", newToken);
  set({ token: newToken });
  return newToken;
},
```

#### 5. 修改 UploadForm 传递 token

**文件：`src/components/UploadForm.jsx`**

```javascript
const result = await uploadAPI.uploadFile(
  filePath,
  projectInfo.id,
  userInfo.id,
  token // ✅ 传入token
);
```

## 架构优势

### 修复前（有状态架构）

```
前端 (localStorage)     后端 (内存状态)
   token ✅    ----X---->   token ❌
                         (重启后丢失)
```

### 修复后（无状态架构）

```
前端 (localStorage)     后端 (无状态)
   token ✅    -------->   每次调用传递token ✅
                         (不需要维护状态)
```

### 优点

1. **✅ 持久化**：token 存储在前端 localStorage，刷新页面不丢失
2. **✅ 安全性**：每次调用都验证 token，更安全
3. **✅ 简化架构**：后端不需要维护全局状态
4. **✅ 易于调试**：token 传递过程清晰可见
5. **✅ 可扩展**：支持多窗口、多标签页使用

## 验证步骤

1. 启动应用并登录
2. 登录成功后，查看控制台日志，确认 token 保存到 localStorage
3. 自动调用 getProject 接口，应该成功返回项目信息
4. 刷新页面，应该自动从 localStorage 恢复登录状态
5. 再次调用项目信息接口，应该成功

## 测试要点

- [x] 登录成功后 token 保存到 localStorage
- [x] 获取项目信息时传递 token
- [x] 上传文件时传递 token
- [x] 刷新 token 时传递 refreshToken
- [x] 页面刷新后能恢复登录状态
- [x] 后端正确接收和验证 token

## 总结

通过将 token 管理从"后端全局状态"改为"前端 localStorage + 每次传递"的架构，彻底解决了 token 持久化问题。这是一个更符合 Web 应用开发最佳实践的方案。

## 相关文件

- `src-tauri/src/main.rs` - Rust 命令处理
- `src-tauri/src/auth.rs` - 认证服务
- `src/services/api.js` - API 调用封装
- `src/stores/authStore.js` - 前端状态管理
- `src/components/UploadForm.jsx` - 上传表单组件

## 修复时间

2025-10-26
