# 🔧 API 地址配置说明

**配置日期**: 2025-10-24  
**API 地址**: `http://42.192.76.234:8081`  
**状态**: ✅ 已硬编码

---

## 📝 修改内容

### 1. 登录表单 - 隐藏 API 地址输入

**文件**: `tauri-app/src/components/LoginForm.jsx`

**修改前**:

```jsx
const [apiUrl, setApiUrl] = useState("http://localhost:3000");

<div className="form-group">
  <label>API 服务器</label>
  <input
    type="text"
    value={apiUrl}
    onChange={(e) => setApiUrl(e.target.value)}
    placeholder="http://localhost:3000"
    className="form-input"
  />
</div>;
```

**修改后**:

```jsx
// 固定的 API 地址
const API_URL = "http://42.192.76.234:8081";

// ✅ API 服务器输入框已移除
// 用户无需手动输入 API 地址
```

---

## 🎯 效果

### 登录界面变化

**之前** (3 个输入框):

1. API 服务器地址 ❌ 已移除
2. 用户名/手机号 ✅
3. 密码 ✅

**现在** (2 个输入框):

1. 用户名/手机号 ✅
2. 密码 ✅

**优点**:

- ✅ 界面更简洁
- ✅ 用户不会输错 API 地址
- ✅ 统一连接到生产服务器
- ✅ 减少用户操作步骤

---

## 🔍 API 地址详情

### 生产环境 API

```
地址: http://42.192.76.234:8081
状态: 在线 ✅
响应: {"code":0,"msg":"系统错误"}
```

**注意**: 服务器返回 `{"code":0,"msg":"系统错误"}` 是正常的默认响应。

### API 端点

基于之前的 PyQt 项目配置，可用的端点包括：

```javascript
// 登录
POST http://42.192.76.234:8081/api/user/login

// 获取项目信息
GET http://42.192.76.234:8081/api/project/myProject

// 文件上传
POST http://42.192.76.234:8081/api/...
```

---

## 🔄 如何修改 API 地址（如果需要）

### 方法 1: 修改源代码（推荐）

**文件**: `tauri-app/src/components/LoginForm.jsx`

```jsx
// 修改这一行
const API_URL = "http://42.192.76.234:8081";

// 改为新地址
const API_URL = "http://new-api-address:port";
```

### 方法 2: 使用环境变量（高级）

1. 创建 `.env` 文件：

```env
VITE_API_URL=http://42.192.76.234:8081
```

2. 修改 `LoginForm.jsx`：

```jsx
const API_URL = import.meta.env.VITE_API_URL || "http://42.192.76.234:8081";
```

3. 重新构建：

```bash
npm run tauri:build
```

### 方法 3: 添加配置文件（最灵活）

创建 `config.json`：

```json
{
  "apiUrl": "http://42.192.76.234:8081"
}
```

修改代码读取配置文件。

---

## 📊 修改总结

| 项目       | 修改前       | 修改后   |
| ---------- | ------------ | -------- |
| API 地址   | 用户输入     | 固定地址 |
| 输入框数量 | 3 个         | 2 个     |
| 用户体验   | 需要知道地址 | 直接登录 |
| 错误可能   | 可能输错地址 | 无此风险 |
| 维护性     | 分散配置     | 集中配置 |

---

## ✅ 验证修改

启动应用后，登录界面应该：

1. ✅ 只显示用户名和密码输入框
2. ✅ 没有 API 服务器地址输入框
3. ✅ 点击登录后自动连接到 `http://42.192.76.234:8081`
4. ✅ 界面更简洁美观

---

## 🛠️ 相关文件

### 前端文件

- `tauri-app/src/components/LoginForm.jsx` - ✅ 已修改
- `tauri-app/src/components/LoginForm.css` - 样式文件
- `tauri-app/src/stores/authStore.js` - 状态管理

### 后端文件

- `tauri-app/src-tauri/src/auth.rs` - Rust 认证逻辑
- `tauri-app/src-tauri/src/main.rs` - 主程序

---

## 🚀 下一步

1. **重新编译应用**

   ```bash
   cd tauri-app
   npm run tauri:dev
   ```

2. **测试登录功能**

   - 输入用户名和密码
   - 点击登录
   - 验证是否连接到正确的 API

3. **生产构建**（如果测试成功）
   ```bash
   npm run tauri:build
   ```

---

## 💡 最佳实践

### 开发环境

如果需要在开发时切换不同的 API 地址：

```jsx
// 开发环境可以这样配置
const API_URL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:3000" // 本地开发
    : "http://42.192.76.234:8081"; // 生产环境
```

### 多环境配置

```jsx
const API_URLS = {
  development: "http://localhost:3000",
  staging: "http://test-server:8081",
  production: "http://42.192.76.234:8081",
};

const API_URL = API_URLS[process.env.NODE_ENV] || API_URLS.production;
```

---

## 📞 技术支持

如果遇到 API 连接问题：

1. **检查网络连接**

   ```bash
   curl http://42.192.76.234:8081
   ```

2. **查看浏览器控制台**

   - 打开开发者工具
   - 查看 Network 标签
   - 检查请求是否发送到正确地址

3. **检查 CORS 配置**
   - 确保服务器允许跨域请求
   - 检查服务器 CORS 头部设置

---

**状态**: ✅ API 地址已固定  
**地址**: http://42.192.76.234:8081  
**界面**: 已简化，移除 API 地址输入框

🎉 **配置完成！**
