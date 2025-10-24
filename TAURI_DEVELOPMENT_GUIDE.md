# 🚀 Tauri 项目完整开发指南

**项目名**: 熔盐管理文件上传工具 - Tauri 版本  
**更新时间**: 2025-10-24  
**项目状态**: ✅ 90% 完成 - 可用状态

---

## 📋 项目概述

这是一个使用 **Tauri + React + Rust** 构建的跨平台文件上传管理工具。

### 核心功能

- ✅ 用户登录 (支持用户名/手机号)
- ✅ 项目查询
- ✅ Excel 文件上传
- ✅ 多工作表解析
- ✅ 进度显示
- ✅ 状态管理
- ✅ 错误处理

---

## 🔧 环境要求

### 必需工具

- **Rust**: 1.70+
- **Node.js**: 18+
- **npm**: 8+
- **macOS/Linux/Windows**

### 检查环境

```bash
rustc --version          # 查看 Rust 版本
node --version          # 查看 Node 版本
npm --version           # 查看 npm 版本
cargo --version         # 查看 Cargo 版本
```

---

## ⚙️ 项目初始化

### 第 1 步: 进入项目目录

```bash
cd /Users/yyz/Desktop/熔盐管理文件上传工具/tauri-app
```

### 第 2 步: 安装依赖

```bash
# npm 依赖
npm install

# Rust 依赖 (自动处理)
```

### 第 3 步: 验证安装

```bash
# 检查 npm 依赖
npm list

# 检查 Rust 配置
cd src-tauri && cargo check
```

---

## 🏃 开发运行

### 方式 1: 完整开发模式（推荐）

```bash
cd /Users/yyz/Desktop/熔盐管理文件上传工具/tauri-app

# 启动 Tauri 开发服务器
# 这会同时启动 React 前端 + Rust 后端
npm run dev
```

**预期输出:**

- ✅ Vite 开发服务器启动 (端口 5173)
- ✅ Rust 后端编译
- ✅ Tauri 窗口打开
- ✅ React 组件热加载

### 方式 2: 分离开发（高级）

**终端 1 - 启动前端:**

```bash
cd tauri-app
npm run dev
```

**终端 2 - 启动后端:**

```bash
cd tauri-app/src-tauri
cargo build
```

---

## 🧪 测试应用

### 1. 登录测试

```
API 服务器: http://localhost:3000
用户名: test_user 或 13800138000
密码: test_password
```

**预期结果:**

- ✅ 登录成功
- ✅ 跳转到上传页面
- ✅ 显示用户信息

### 2. 项目查询测试

**预期结果:**

- ✅ 显示项目名称
- ✅ 显示项目状态
- ✅ 显示项目 ID

### 3. 文件上传测试

**准备文件:**

- 使用 Excel 文件 (`.xlsx` 或 `.xls`)
- 确保包含日报数据

**步骤:**

1. 点击 "选择文件"
2. 选择 Excel 文件
3. 点击 "开始上传"
4. 查看进度条和消息

**预期结果:**

- ✅ 文件选择对话框打开
- ✅ 进度条显示
- ✅ 上传成功/失败消息
- ✅ 文件路径显示

---

## 📁 项目结构

```
tauri-app/
├── src/                          # React 前端代码
│   ├── components/
│   │   ├── LoginForm.jsx        # 登录表单
│   │   ├── UploadForm.jsx       # 上传表单
│   │   ├── LoginForm.css        # (样式在 App.css)
│   │   └── UploadForm.css       # (样式在 App.css)
│   ├── stores/
│   │   └── authStore.js         # Zustand 状态管理
│   ├── services/
│   │   └── api.js               # IPC 通信服务
│   ├── App.jsx                  # 主应用组件
│   ├── App.css                  # 应用样式
│   ├── index.css                # 全局样式
│   └── main.jsx                 # React 入口
│
├── src-tauri/                    # Rust 后端代码
│   ├── src/
│   │   ├── main.rs              # 应用入口 + IPC 命令
│   │   ├── auth.rs              # 认证模块
│   │   ├── project.rs           # 项目模块
│   │   ├── upload.rs            # 上传模块
│   │   └── excel.rs             # Excel 解析模块
│   └── Cargo.toml               # Rust 依赖配置
│
├── index.html                    # HTML 模板
├── vite.config.js               # Vite 构建配置
├── package.json                 # npm 配置
└── package-lock.json            # 依赖锁定文件
```

---

## 🔌 IPC 通信接口

### 后端命令 (Rust)

#### 1. `cmd_login`

**参数:**

```javascript
{
  username: string,      // 用户名或手机号
  password: string,      // 密码
  api_url: string        // API 服务器地址
}
```

**返回:**

```javascript
{
  token: string,
  refresh_token: string,
  user_info: {
    id: number,
    username: string,
    email: string,
    phone: string
  }
}
```

#### 2. `cmd_get_project`

**参数:** 无

**返回:**

```javascript
{
  id: number,
  name: string,
  status_display_name: string
}
```

#### 3. `cmd_upload_file`

**参数:**

```javascript
{
  file_path: string,      // 文件路径
  project_id: number,     // 项目 ID
  reporter_id: number     // 报告者 ID
}
```

**返回:** 成功消息 (字符串)

#### 4. `greet`

**参数:**

```javascript
{
  name: string;
}
```

**返回:** 问候消息

---

## 💾 前端状态管理 (Zustand)

### authStore 状态和方法

```javascript
// 状态
- token: string | null              // 登录 Token
- userInfo: object | null           // 用户信息
- projectInfo: object | null        // 项目信息
- loading: boolean                  // 加载状态
- error: string | null              // 错误信息
- screen: 'login' | 'upload'        // 当前屏幕

// 方法
- login(username, password, apiUrl)  // 登录
- logout()                          // 登出
- getProject()                      // 获取项目
- setError(error)                   // 设置错误
- clearError()                      // 清除错误
```

---

## 🚀 构建和打包

### 1. 开发构建（测试用）

```bash
cd tauri-app

# 只构建前端
npm run build

# 输出: dist/ 目录
```

### 2. 生产构建

```bash
cd tauri-app

# 完整打包（所有平台）
npm run tauri:build

# 输出位置:
# - macOS: src-tauri/target/release/bundle/dmg/
# - Windows: src-tauri/target/release/bundle/msi/
# - Linux: src-tauri/target/release/bundle/deb/
```

### 3. 平台特定构建

```bash
# 仅构建 macOS
cargo tauri build --target universal-apple-darwin

# 仅构建 Windows
cargo tauri build --target x86_64-pc-windows-msvc

# 仅构建 Linux
cargo tauri build --target x86_64-unknown-linux-gnu
```

---

## 🔍 调试

### 前端调试

1. **Chrome DevTools**

   - 在 Tauri 窗口中按 `F12`
   - 查看 Console、Elements、Network 等

2. **console.log**

   ```javascript
   // 在 React 组件中
   console.log("Debug info:", state);
   ```

3. **React DevTools**
   ```bash
   # 扩展程序: React Developer Tools
   ```

### 后端调试

1. **println! 宏**

   ```rust
   println!("Debug: {:?}", variable);
   ```

2. **日志输出**
   ```bash
   # 在开发窗口查看输出
   ```

---

## ⚡ 性能优化

### 前端优化

1. **代码分割**

   ```javascript
   // 使用动态导入
   const LoginForm = lazy(() => import("./components/LoginForm"));
   ```

2. **记忆化**

   ```javascript
   // 使用 useMemo, useCallback
   const memoizedValue = useMemo(() => computeValue(), [deps]);
   ```

3. **图片优化**
   - 使用 WebP 格式
   - 压缩图片大小

### 后端优化

1. **异步操作**

   - 已使用 tokio
   - 支持并发请求

2. **缓存**
   - Token 存储在前端 localStorage
   - 项目信息缓存

---

## 📊 常见问题排查

### Q1: npm install 失败

**解决方案:**

```bash
# 清除缓存
npm cache clean --force

# 重新安装
npm install --legacy-peer-deps
```

### Q2: Cargo 编译失败

**解决方案:**

```bash
# 清除构建缓存
cargo clean

# 重新编译
cargo build
```

### Q3: 前端显示空白

**解决方案:**

1. 检查浏览器控制台错误
2. 清除浏览器缓存
3. 硬刷新 (Cmd+Shift+R / Ctrl+Shift+R)
4. 检查 `npm run dev` 是否运行

### Q4: 登录请求失败

**解决方案:**

1. 检查 API 地址是否正确
2. 确保后端服务运行中
3. 检查网络连接
4. 查看浏览器 Network 标签

### Q5: 文件上传失败

**解决方案:**

1. 检查文件格式 (Excel)
2. 检查文件权限
3. 查看后端日志
4. 检查 API 响应状态

---

## 📚 技术栈详情

| 层级            | 技术            | 版本   | 用途       |
| --------------- | --------------- | ------ | ---------- |
| **UI 框架**     | React           | 18.3.1 | 用户界面   |
| **状态管理**    | Zustand         | 4.5.7  | 状态管理   |
| **前端构建**    | Vite            | 5.4.21 | 极速构建   |
| **前端到后端**  | @tauri-apps/api | 2.9.0  | IPC 通信   |
| **应用框架**    | Tauri           | 2      | 跨平台应用 |
| **后端语言**    | Rust            | 1.90+  | 后端开发   |
| **异步运行**    | tokio           | 1      | 异步运行时 |
| **HTTP 客户端** | reqwest         | 0.11   | HTTP 请求  |
| **序列化**      | serde_json      | 1      | JSON 处理  |
| **Excel 解析**  | calamine        | 0.22   | 文件解析   |
| **正则表达式**  | regex           | 1      | 文本处理   |

---

## 🎯 开发工作流

### 修改 React 代码

```bash
# 1. 修改 src/App.jsx 或其他 React 文件
# 2. 保存文件
# 3. 浏览器自动刷新 (热加载)
```

### 修改 Rust 代码

```bash
# 1. 修改 src-tauri/src/main.rs 或其他 Rust 文件
# 2. 在另一个终端重新编译:
cd src-tauri && cargo build

# 3. 重启 Tauri 应用
```

### 修改样式

```bash
# 1. 修改 src/App.css
# 2. 保存文件
# 3. 浏览器自动刷新
```

---

## ✅ 发布清单

在生产发布前，请检查：

- [ ] 所有代码已测试
- [ ] 没有 console.log 调试代码
- [ ] 没有 TODO 或 FIXME 注释
- [ ] 错误处理完善
- [ ] API 地址已正确配置
- [ ] 依赖已锁定版本
- [ ] 构建无错误
- [ ] 应用可正常启动
- [ ] 登录功能正常
- [ ] 上传功能正常
- [ ] UI 在各尺寸正确显示
- [ ] 性能可接受

---

## 🔗 相关资源

- [Tauri 官方文档](https://tauri.app)
- [React 官方文档](https://react.dev)
- [Zustand GitHub](https://github.com/pmndrs/zustand)
- [Rust 官方文档](https://doc.rust-lang.org)
- [Vite 官方文档](https://vitejs.dev)

---

## 📞 支持和帮助

如遇到问题，请：

1. 检查本文档的常见问题部分
2. 查看项目日志和错误消息
3. 参考相关技术文档
4. 检查项目代码注释

---

**最后更新**: 2025-10-24  
**项目版本**: v0.1.0  
**开发状态**: 🟢 可用
