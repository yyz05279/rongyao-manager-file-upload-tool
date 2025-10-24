# Tauri 应用修复总结

## 修复时间

2025 年 10 月 24 日

## 问题描述

1. **dialog.open 权限错误**

   - 错误信息：`dialog.open not allowed. Permissions associated with this command: dialog:allow-open, dialog:default`
   - 原因：Tauri 2.x 需要显式配置权限

2. **用户信息显示不完整**
   - 需求：显示用户姓名+角色，以及项目名称
   - 当前：只显示用户名

## 修复方案

### 1. 修复 dialog.open 权限问题

#### 创建权限配置文件

文件路径：`tauri-app/src-tauri/capabilities/default.json`

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default permissions for the application",
  "platforms": ["macOS", "windows", "linux"],
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:path:default",
    "dialog:default",
    "dialog:allow-open",
    "dialog:allow-save",
    "dialog:allow-message",
    "dialog:allow-ask",
    "dialog:allow-confirm"
  ]
}
```

**注意**：Tauri 2.x 的权限名称必须使用正确的前缀（如 `core:path:default` 而不是 `path:default`）。

#### 更新 tauri.conf.json

在 `app.windows` 中添加 `label: "main"`：

```json
{
  "label": "main",
  "title": "熔盐管理文件上传工具",
  ...
}
```

在 `app.security` 中添加 capabilities 引用：

```json
{
  "security": {
    "csp": null,
    "capabilities": ["default"]
  }
}
```

### 2. 添加用户信息字段

#### 修改 Rust UserInfo 结构

文件路径：`tauri-app/src-tauri/src/auth.rs`

```rust
#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct UserInfo {
    pub id: i32,
    pub username: String,
    pub name: String,      // ✅ 新增：姓名
    pub email: String,
    pub phone: String,
    pub role: String,      // ✅ 新增：角色
}
```

#### 更新登录响应解析

在 `login` 函数中添加字段解析：

```rust
let user_info = UserInfo {
    id: result["data"]["user"]["id"].as_i64().unwrap_or(0) as i32,
    username: result["data"]["user"]["username"]
        .as_str()
        .unwrap_or("")
        .to_string(),
    name: result["data"]["user"]["name"]      // ✅ 新增
        .as_str()
        .unwrap_or("")
        .to_string(),
    email: result["data"]["user"]["email"]
        .as_str()
        .unwrap_or("")
        .to_string(),
    phone: result["data"]["user"]["phone"]
        .as_str()
        .unwrap_or("")
        .to_string(),
    role: result["data"]["user"]["role"]      // ✅ 新增
        .as_str()
        .unwrap_or("")
        .to_string(),
};
```

### 3. 更新前端显示

#### 修改 UploadForm.jsx

文件路径：`tauri-app/src/components/UploadForm.jsx`

显示用户姓名和角色：

```jsx
// 角色映射（参考 Python 代码）
const roleMap = {
  ADMIN: "管理员",
  MANAGER: "项目经理",
  OPERATOR: "运维人员",
};

const getRoleText = (role) => {
  return roleMap[role] || role;
};

// 显示用户信息
<div className="user-info">
  <span>
    👤 {userInfo?.name || userInfo?.username}
    {userInfo?.role && ` (${getRoleText(userInfo.role)})`}
  </span>
  <button className="btn-logout" onClick={logout}>
    退出
  </button>
</div>;
```

**角色转换规则**：

- `ADMIN` → `管理员`
- `MANAGER` → `项目经理`
- `OPERATOR` → `运维人员`
- 其他未知角色保持原样

简化项目信息显示（只显示项目名称）：

```jsx
{
  projectInfo && (
    <div className="project-info">
      <p>
        <strong>项目:</strong> {projectInfo.name}
      </p>
    </div>
  );
}
```

## 测试方法

### 启动开发服务器

```bash
cd tauri-app
npm run tauri dev
```

或使用测试脚本：

```bash
cd tauri-app
chmod +x test-fixes.sh
./test-fixes.sh
```

### 测试清单

1. **文件选择功能**

   - [ ] 点击"选择文件"按钮
   - [ ] 文件对话框正常打开（不再报权限错误）
   - [ ] 可以选择 Excel 文件

2. **用户信息显示**

   - [ ] 登录后显示用户姓名（而不是用户名）
   - [ ] 显示用户角色（例如：张三 (管理员)）
   - [ ] 如果没有姓名，fallback 到用户名

3. **项目信息显示**
   - [ ] 登录后显示项目名称
   - [ ] 项目名称正确显示

## 参考的 Python 代码

### Python 用户信息显示逻辑

文件：`ui/upload_widget.py`

```python
# 显示用户信息：姓名 + 手机号
name = user_info.get('name', '未知用户')
phone = user_info.get('phone') or user_info.get('username', '')

# 构建显示文本：姓名 手机号
if phone:
    display_text = f"{name} {phone}"
else:
    display_text = name
```

### Python 项目信息显示逻辑

```python
if project_info:
    # 只显示项目名称
    project_name = project_info.get('name', '未知项目')
    self.project_name_value.setText(project_name)
```

## 修改文件清单

1. ✅ `tauri-app/src-tauri/capabilities/default.json` - 新建
2. ✅ `tauri-app/src-tauri/tauri.conf.json` - 修改
3. ✅ `tauri-app/src-tauri/src/auth.rs` - 修改
4. ✅ `tauri-app/src/components/UploadForm.jsx` - 修改
5. ✅ `tauri-app/test-fixes.sh` - 新建（测试脚本）

## 注意事项

1. 权限配置只在开发模式和生产构建时生效
2. 如果权限配置无效，需要清理构建缓存：

   ```bash
   cd tauri-app/src-tauri
   cargo clean
   cd ..
   npm run tauri dev
   ```

3. 用户信息字段依赖后端 API 返回，确保后端返回包含 `name` 和 `role` 字段

## 后续优化建议

1. 添加更多用户信息显示（如部门、职位等）
2. 优化项目信息的展示方式
3. 添加项目切换功能（如果用户有多个项目）
4. 添加用户头像显示
