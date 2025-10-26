# Token 传入方式说明

## 问题分析

### 原始错误

在开发过程中，发现 Token 传入方式不正确，导致 API 调用失败。

### 根本原因

**错误的实现**（使用 `Authorization` header）:

```rust
.header("Authorization", format!("Bearer {}", self.token))
```

**正确的实现**（使用 `token` header）:

```rust
.header("token", &self.token)
```

## Python 实现参考

### BaseService 中的实现

**文件**: `services/base_service.py`

```python
def _get_headers(self, custom_headers: Dict = None, include_token: bool = True) -> Dict:
    """
    获取请求头，自动添加token

    :param custom_headers: 自定义请求头
    :param include_token: 是否包含token
    :return: 完整的请求头
    """
    headers = {
        'Content-Type': 'application/json'
    }

    # ✅ 添加token到请求头
    if include_token and self.token:
        headers['token'] = self.token  # ← 关键：使用 'token' 而不是 'Authorization'

    # 合并自定义请求头
    if custom_headers:
        headers.update(custom_headers)

    return headers
```

### 请求示例

**GET 请求**:

```python
response = requests.get(
    url,
    params=params,
    headers={
        'Content-Type': 'application/json',
        'token': 'eyJhbGciOiJIUzUxMiJ9...'  # ← 完整的token，无需前缀
    },
    timeout=timeout
)
```

**POST 请求**:

```python
response = requests.post(
    url,
    json=json_data,
    headers={
        'Content-Type': 'application/json',
        'token': 'eyJhbGciOiJIUzUxMiJ9...'  # ← 完整的token，无需前缀
    },
    timeout=timeout
)
```

## Rust/Tauri 实现

### 1. 获取项目信息

**文件**: `tauri-app/src-tauri/src/project.rs`

```rust
pub async fn get_my_project(&self) -> Result<ProjectInfo, String> {
    let client = reqwest::Client::new();
    let url = format!("{}/api/v1/projects/my-project", self.api_base_url);

    // ✅ 使用 "token" 作为 header key
    let response = client
        .get(&url)
        .header("token", &self.token)  // ← 正确：使用 "token"
        .send()
        .await
        .map_err(|e| format!("请求失败: {}", e))?;

    // ...
}
```

### 2. 上传日报

**文件**: `tauri-app/src-tauri/src/upload.rs`

```rust
pub async fn upload_daily_report(
    &self,
    file_path: String,
    project_id: i32,
    reporter_id: i32,
) -> Result<String, String> {
    let client = reqwest::Client::new();
    let url = format!("{}/api/v1/daily-reports/batch-import", self.api_base_url);

    // ✅ 使用 "token" 作为 header key
    let response = client
        .post(&url)
        .header("token", &self.token)  // ← 正确：使用 "token"
        .json(&api_data)
        .send()
        .await
        .map_err(|e| format!("上传失败: {}", e))?;

    // ...
}
```

## HTTP Header 对比

### 错误的方式（之前的实现）

```
Authorization: Bearer eyJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoiTUFOQUdFUiIsInRva2VuVHlwZSI6ImFjY2VzcyIsInVzZXJJZCI6MTAsInVzZXJuYW1lIjoiMTM5NTkxNDEyMzIiLCJpYXQiOjE3NjE0NDI0MTgsImV4cCI6MTc2MTUyODgxOH0.7kpOtjitu9tAD_uErOm2RunJ54jkHqV9UuyXab4ZC3EyOo--mWnT1KMVS72C1zp2TdkfJzIS-smmVYvj4UIU3g
```

**问题**:

- ❌ Header key 使用了 `Authorization`
- ❌ Token 前面添加了 `Bearer ` 前缀

### 正确的方式（当前实现）

```
token: eyJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoiTUFOQUdFUiIsInRva2VuVHlwZSI6ImFjY2VzcyIsInVzZXJJZCI6MTAsInVzZXJuYW1lIjoiMTM5NTkxNDEyMzIiLCJpYXQiOjE3NjE0NDI0MTgsImV4cCI6MTc2MTUyODgxOH0.7kpOtjitu9tAD_uErOm2RunJ54jkHqV9UuyXab4ZC3EyOo--mWnT1KMVS72C1zp2TdkfJzIS-smmVYvj4UIU3g
```

**特点**:

- ✅ Header key 使用 `token`
- ✅ Token 直接传入，无需任何前缀
- ✅ Token 完整传入（208 个字符）

## Token 格式

### JWT Token 结构

完整的 JWT Token 由三部分组成，用 `.` 分隔：

```
eyJhbGciOiJIUzUxMiJ9
  ↓ Header (算法和令牌类型)

.eyJyb2xlIjoiTUFOQUdFUiIsInRva2VuVHlwZSI6ImFjY2VzcyIsInVzZXJJZCI6MTAsInVzZXJuYW1lIjoiMTM5NTkxNDEyMzIiLCJpYXQiOjE3NjE0NDI0MTgsImV4cCI6MTc2MTUyODgxOH0
  ↓ Payload (数据)

.7kpOtjitu9tAD_uErOm2RunJ54jkHqV9UuyXab4ZC3EyOo--mWnT1KMVS72C1zp2TdkfJzIS-smmVYvj4UIU3g
  ↓ Signature (签名)
```

**解析 Payload**（Base64 解码后）:

```json
{
  "role": "MANAGER",
  "tokenType": "access",
  "userId": 10,
  "username": "13959141232",
  "iat": 1761442418,
  "exp": 1761528818
}
```

**字段说明**:

- `role`: 用户角色（MANAGER/OPERATOR）
- `tokenType`: Token 类型（access/refresh）
- `userId`: 用户 ID
- `username`: 用户名
- `iat`: 签发时间（Issue At Time）
- `exp`: 过期时间（Expiration Time）

### Token 长度

标准 JWT Token 长度通常为：

- **Header**: ~20-30 字符
- **Payload**: ~100-150 字符
- **Signature**: ~80-90 字符
- **总长度**: ~208 字符（包括两个 `.` 分隔符）

## API 接口说明

### 1. 获取项目信息

**接口**: `GET /api/v1/projects/my-project`

**请求头**:

```
Content-Type: application/json
token: eyJhbGciOiJIUzUxMiJ9...
```

**响应示例**:

```json
{
  "code": 1,
  "message": "成功",
  "data": {
    "id": 1,
    "name": "淮安项目",
    "typeDisplayName": "熔盐储热",
    "statusDisplayName": "进行中",
    "manager": "张三",
    "completionProgress": 60,
    "estimatedSaltAmount": 10000,
    "actualSaltAmount": 6000
  }
}
```

### 2. 批量上传日报

**接口**: `POST /api/v1/daily-reports/batch-import`

**请求头**:

```
Content-Type: application/json
token: eyJhbGciOiJIUzUxMiJ9...
```

**请求体**:

```json
{
  "data": [...],
  "projectId": 1,
  "reporterId": 10
}
```

**响应示例**:

```json
{
  "code": 1,
  "message": "导入成功",
  "data": {
    "successCount": 5,
    "failCount": 0
  }
}
```

## 调试日志

### Python 端日志

```
[GET] http://42.192.76.234:8081/api/v1/projects/my-project
Headers: {'Content-Type': 'application/json', 'token': 'eyJhbGciOiJIUzUxMiJ9...'}
Response: 200
```

### Rust/Tauri 端日志

```
🔍 [ProjectService] 开始获取项目信息
  - URL: http://42.192.76.234:8081/api/v1/projects/my-project
  - Token长度: 208 字符
  - Token前20字符: eyJhbGciOiJIUzUxMiJ9
  - Token后20字符: -smmVYvj4UIU3g
  - 完整Token: eyJhbGciOiJIUzUxMiJ9...
  - token Header: eyJhbGciOiJIUzUxMiJ9...
📡 [ProjectService] 响应状态: 200 OK
✅ [ProjectService] 项目信息解析成功
```

## 常见问题

### Q1: 为什么不使用标准的 Authorization Bearer?

**A**: 这是后端 API 的设计决定。不同的 API 可能采用不同的认证方式：

1. **标准 OAuth 2.0 方式**:

   ```
   Authorization: Bearer <token>
   ```

2. **自定义 Header 方式**（本项目采用）:

   ```
   token: <token>
   ```

3. **API Key 方式**:
   ```
   X-API-Key: <key>
   ```

### Q2: Token 如何存储？

**前端（localStorage）**:

```javascript
localStorage.setItem("token", response.token);
localStorage.setItem("refreshToken", response.refresh_token);
localStorage.setItem("tokenExpiresAt", tokenExpiresAt.toString());
```

**后端（Tauri 全局状态）**:

```rust
*state.token.lock().unwrap() = Some(result.token.clone());
*state.refresh_token.lock().unwrap() = Some(result.refresh_token.clone());
```

### Q3: Token 何时失效？

根据 JWT Payload 中的 `exp` 字段：

- **Access Token**: 24 小时有效期
- **Refresh Token**: 30 天有效期

过期后需要调用刷新接口或重新登录。

### Q4: Token 安全性如何保证？

1. **HTTPS 传输**（生产环境建议）
2. **过期时间限制**（24 小时）
3. **刷新机制**（自动刷新）
4. **本地存储**（localStorage + Tauri 状态）

## 修改历史

### 2025-10-26 - Token Header 修正

**修改前**:

```rust
.header("Authorization", format!("Bearer {}", self.token))
```

**修改后**:

```rust
.header("token", &self.token)
```

**影响的文件**:

1. `tauri-app/src-tauri/src/project.rs` - 获取项目信息接口
2. `tauri-app/src-tauri/src/upload.rs` - 批量上传日报接口

**修改原因**:

- 与 Python 实现保持一致
- 符合后端 API 的预期格式
- 修复 Token 认证失败问题

## 测试验证

### 1. 测试获取项目信息

```bash
curl -X GET \
  http://42.192.76.234:8081/api/v1/projects/my-project \
  -H "Content-Type: application/json" \
  -H "token: eyJhbGciOiJIUzUxMiJ9..."
```

**预期响应**: 200 OK + 项目信息

### 2. 测试上传日报

```bash
curl -X POST \
  http://42.192.76.234:8081/api/v1/daily-reports/batch-import \
  -H "Content-Type: application/json" \
  -H "token: eyJhbGciOiJIUzUxMiJ9..." \
  -d '{
    "data": [...],
    "projectId": 1,
    "reporterId": 10
  }'
```

**预期响应**: 200 OK + 导入结果

## 总结

✅ **Token 传入方式已修正**

**关键要点**:

1. ✅ Header key 使用 `token`，而不是 `Authorization`
2. ✅ Token 直接传入，无需 `Bearer ` 前缀
3. ✅ Token 完整传入（208 个字符）
4. ✅ 与 Python 实现完全一致
5. ✅ 所有 API 调用统一使用相同格式

**验证方法**:

- 查看终端日志，确认 token header 格式正确
- 测试登录后获取项目信息
- 测试上传日报功能
- 确认 API 返回 200 OK

现在 Token 传入方式已经与 Python 版本完全一致！🎉
