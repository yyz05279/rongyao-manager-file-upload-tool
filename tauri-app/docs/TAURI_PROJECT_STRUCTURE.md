# Tauri 版本 - 项目结构详解

> 基于 React + Rust + Tauri 2.x 的现代化桌面应用

---

## 📁 完整目录树

```
tauri-app/
│
├── 📄 package.json                    # Node.js项目配置
├── 📄 package-lock.json               # 依赖锁定文件
├── 📄 vite.config.js                  # Vite构建配置
├── 📄 index.html                      # HTML入口文件
│
├── 📂 src/                            # 前端源代码（React + JavaScript）
│   │
│   ├── 📄 main.jsx                    # React应用入口
│   ├── 📄 App.jsx                     # 主应用组件
│   ├── 📄 App.css                     # 主应用样式
│   ├── 📄 index.css                   # 全局样式（渐变背景、通用样式）
│   │
│   ├── 📂 components/                 # React组件目录
│   │   ├── 📄 LoginForm.jsx           # 登录表单组件
│   │   ├── 📄 LoginForm.css           # 登录表单样式
│   │   ├── 📄 UploadForm.jsx          # 上传表单组件
│   │   ├── 📄 UploadForm.css          # 上传表单样式
│   │   ├── 📄 PreviewDialog.jsx       # 数据预览对话框组件
│   │   ├── 📄 PreviewDialog.css       # 预览对话框样式
│   │   ├── 📄 DetailDialog.jsx        # 详情对话框组件
│   │   └── 📄 DetailDialog.css        # 详情对话框样式
│   │
│   ├── 📂 services/                   # 前端服务层
│   │   └── 📄 api.js                  # API接口封装（Axios）
│   │
│   └── 📂 stores/                     # 状态管理
│       └── 📄 authStore.js            # 认证状态管理（Zustand）
│
├── 📂 src-tauri/                      # Tauri后端（Rust）
│   │
│   ├── 📄 Cargo.toml                  # Rust项目配置
│   ├── 📄 Cargo.lock                  # Rust依赖锁定
│   ├── 📄 build.rs                    # Rust构建脚本
│   ├── 📄 tauri.conf.json             # Tauri配置文件
│   │
│   ├── 📂 src/                        # Rust源代码
│   │   │
│   │   ├── 📄 main.rs                 # Rust入口文件
│   │   │   ├── setup_app_state()      # 应用状态初始化
│   │   │   └── tauri::Builder         # Tauri应用构建器
│   │   │
│   │   ├── 📂 api/                    # API模块（HTTP请求）
│   │   │   ├── 📄 mod.rs              # 模块入口
│   │   │   ├── 📄 auth.rs             # 认证API（登录、刷新Token）
│   │   │   ├── 📄 project.rs          # 项目API（获取项目列表、信息）
│   │   │   └── 📄 upload.rs           # 上传API（批量上传日报）
│   │   │
│   │   ├── 📂 commands/               # Tauri命令（前端调用）
│   │   │   ├── 📄 mod.rs              # 模块入口
│   │   │   ├── 📄 auth_commands.rs    # 认证命令
│   │   │   │   ├── login_command()    # 用户登录
│   │   │   │   └── refresh_token_command() # 刷新Token
│   │   │   ├── 📄 project_commands.rs # 项目命令
│   │   │   │   ├── get_projects_command() # 获取项目列表
│   │   │   │   └── get_project_info_command() # 获取项目信息
│   │   │   └── 📄 upload_commands.rs  # 上传命令
│   │   │       ├── parse_excel_command() # 解析Excel文件
│   │   │       └── upload_reports_command() # 批量上传日报
│   │   │
│   │   └── 📂 utils/                  # 工具模块
│   │       ├── 📄 mod.rs              # 模块入口
│   │       ├── 📄 excel.rs            # Excel解析（calamine）
│   │       │   ├── parse_excel_file() # 解析Excel文件
│   │       │   └── extract_cell_value() # 提取单元格值
│   │       └── 📄 http.rs             # HTTP客户端（reqwest）
│   │           ├── create_client()    # 创建HTTP客户端
│   │           └── handle_response()  # 处理响应
│   │
│   ├── 📂 capabilities/               # Tauri权限配置
│   │   └── 📄 default.json            # 默认权限配置
│   │
│   ├── 📂 icons/                      # 应用图标
│   │   └── 🖼️ icon.png                # 主图标（512x512）
│   │
│   ├── 📂 gen/                        # 自动生成的文件（不需要编辑）
│   │   └── 📂 schemas/                # JSON Schema文件
│   │
│   └── 📂 target/                     # Rust编译输出（忽略）
│
└── 📂 node_modules/                   # Node.js依赖（忽略）
```

---

## 🔧 核心文件说明

### 前端（React）

#### `src/main.jsx`

React 应用入口，初始化 React 和状态管理

```javascript
- createRoot() 创建React根节点
- StrictMode 严格模式
- App组件渲染
```

#### `src/App.jsx`

主应用组件，路由和布局管理

```javascript
- 登录状态判断
- LoginForm / UploadForm 切换
- 全局错误处理
```

#### `src/components/LoginForm.jsx`

登录表单组件

```javascript
- 用户名/密码输入
- 记住密码功能
- 调用 invoke('login_command')
- Token存储到 authStore
```

#### `src/components/UploadForm.jsx`

上传表单组件

```javascript
-项目选择 - 文件选择 - Excel解析预览 - 批量上传 - 进度显示;
```

#### `src/components/PreviewDialog.jsx`

数据预览对话框

```javascript
-表格展示解析结果 - 按施工区域分组 - 支持勾选 / 全选 - 覆盖旧记录选项;
```

#### `src/components/DetailDialog.jsx`

详情对话框

```javascript
-显示单条日报详细信息 - 字段格式化显示 - 关闭按钮;
```

#### `src/services/api.js`

API 接口封装

```javascript
- axios实例配置
- 请求拦截器（添加Token）
- 响应拦截器（错误处理）
- Token刷新逻辑
```

#### `src/stores/authStore.js`

认证状态管理（Zustand）

```javascript
- token: 访问令牌
- refreshToken: 刷新令牌
- userInfo: 用户信息
- login/logout: 登录登出方法
- 持久化到localStorage
```

---

### 后端（Rust）

#### `src-tauri/src/main.rs`

Rust 应用入口

```rust
- setup_app_state() 初始化应用状态
- 注册所有Tauri命令
- 配置窗口和权限
- 启动应用
```

#### `src-tauri/src/api/auth.rs`

认证 API 实现

```rust
pub struct LoginRequest {
    username: String,
    password: String,
}

pub async fn login(client: &Client, req: LoginRequest) -> Result<LoginResponse>
pub async fn refresh_token(client: &Client, token: &str) -> Result<TokenResponse>
```

#### `src-tauri/src/api/project.rs`

项目 API 实现

```rust
pub async fn get_projects(client: &Client, token: &str) -> Result<Vec<Project>>
pub async fn get_project_info(client: &Client, token: &str, id: i32) -> Result<ProjectInfo>
```

#### `src-tauri/src/api/upload.rs`

上传 API 实现

```rust
pub struct DailyReport {
    project_id: i32,
    date: String,
    data: serde_json::Value,
}

pub async fn batch_upload(client: &Client, token: &str, reports: Vec<DailyReport>) -> Result<()>
```

#### `src-tauri/src/commands/auth_commands.rs`

认证命令

```rust
#[tauri::command]
pub async fn login_command(username: String, password: String) -> Result<LoginResponse, String>

#[tauri::command]
pub async fn refresh_token_command(token: String) -> Result<TokenResponse, String>
```

#### `src-tauri/src/commands/project_commands.rs`

项目命令

```rust
#[tauri::command]
pub async fn get_projects_command(token: String) -> Result<Vec<Project>, String>

#[tauri::command]
pub async fn get_project_info_command(token: String, project_id: i32) -> Result<ProjectInfo, String>
```

#### `src-tauri/src/commands/upload_commands.rs`

上传命令

```rust
#[tauri::command]
pub async fn parse_excel_command(file_path: String) -> Result<Vec<DailyReport>, String>

#[tauri::command]
pub async fn upload_reports_command(
    token: String,
    project_id: i32,
    reports: Vec<DailyReport>,
    overwrite: bool,
) -> Result<UploadResult, String>
```

#### `src-tauri/src/utils/excel.rs`

Excel 解析工具

```rust
use calamine::{Reader, Xlsx, open_workbook};

pub fn parse_excel_file(path: &str) -> Result<Vec<DailyReport>, Error>
- 打开Excel文件
- 遍历工作表
- 解析单元格数据
- 验证必填字段
- 返回结构化数据
```

#### `src-tauri/src/utils/http.rs`

HTTP 客户端工具

```rust
use reqwest::Client;

pub fn create_client() -> Client
- 创建带超时的HTTP客户端
- 配置User-Agent
- 启用gzip压缩

pub async fn handle_response<T>(resp: Response) -> Result<T, Error>
- 检查HTTP状态码
- 解析JSON响应
- 统一错误处理
```

---

## 🔌 API 端点配置

在 `src-tauri/tauri.conf.json` 中配置：

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devPath": "http://localhost:5173",
    "distDir": "../dist"
  },
  "tauri": {
    "allowlist": {
      "all": false,
      "fs": {
        "all": false,
        "readFile": true,
        "scope": ["$HOME/**"]
      },
      "dialog": {
        "all": false,
        "open": true
      }
    }
  }
}
```

---

## 🚀 开发命令

```bash
# 安装依赖
npm install

# 开发模式（热重载）
npm run tauri dev

# 构建生产版本
npm run tauri build

# 仅构建前端
npm run build

# 仅构建Rust
cd src-tauri
cargo build --release
```

---

## 📦 构建输出

构建后的文件位于：

**macOS:**

```
src-tauri/target/release/bundle/macos/
└── 熔盐管理文件上传工具.app
```

**Windows:**

```
src-tauri/target/release/bundle/msi/
└── 熔盐管理文件上传工具_1.0.0_x64.msi
```

**Linux:**

```
src-tauri/target/release/bundle/deb/
└── molten-salt-manager_1.0.0_amd64.deb
```

---

## 🔑 权限说明

### `capabilities/default.json`

```json
{
  "identifier": "default",
  "windows": ["main"],
  "permissions": ["core:default", "fs:allow-read-file", "dialog:allow-open"]
}
```

说明：

- `core:default` - 核心权限（窗口、事件等）
- `fs:allow-read-file` - 允许读取文件
- `dialog:allow-open` - 允许打开文件对话框

---

## 🛠️ 依赖说明

### 前端依赖（package.json）

```json
{
  "dependencies": {
    "react": "^18.3.1", // React框架
    "react-dom": "^18.3.1", // React DOM操作
    "zustand": "^4.5.0", // 状态管理
    "axios": "^1.7.7", // HTTP客户端
    "@tauri-apps/api": "^2.0.0" // Tauri前端API
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.3", // Vite React插件
    "vite": "^5.4.10" // 构建工具
  }
}
```

### Rust 依赖（Cargo.toml）

```toml
[dependencies]
tauri = "2.0.0"                      # Tauri框架
serde = { version = "1", features = ["derive"] }  # 序列化
serde_json = "1"                     # JSON处理
reqwest = { version = "0.12", features = ["json"] }  # HTTP客户端
tokio = { version = "1", features = ["full"] }  # 异步运行时
calamine = "0.25"                    # Excel解析
```

---

## 🎨 样式说明

### 全局样式（index.css）

- 天蓝色渐变背景
- 现代化卡片设计
- 响应式布局
- 平滑过渡动画

### 组件样式

- 统一的颜色主题
- 一致的间距和圆角
- 悬停和焦点效果
- 加载动画

---

## 🐛 调试技巧

### 前端调试

```bash
# 在开发模式下打开浏览器开发者工具
npm run tauri dev
# 按 F12 打开DevTools
```

### Rust 调试

```rust
// 在main.rs中添加
println!("Debug: {:?}", variable);

// 或使用日志
use log::{info, warn, error};
info!("Info message");
```

### 查看日志

```bash
# macOS/Linux
tail -f ~/Library/Logs/熔盐管理文件上传工具/app.log

# Windows
type %APPDATA%\熔盐管理文件上传工具\logs\app.log
```

---

## 📝 开发建议

1. **前端开发**: 修改 `src/` 下的文件，热重载自动生效
2. **Rust 开发**: 修改 `src-tauri/src/` 下的文件，需要重启 `tauri dev`
3. **添加新命令**:
   - 在 `src-tauri/src/commands/` 添加命令函数
   - 在 `main.rs` 中注册命令
   - 在前端用 `invoke()` 调用
4. **样式调整**: 修改对应的 `.css` 文件
5. **状态管理**: 使用 Zustand store，避免 prop drilling

---

**文档版本**: 1.0.0
**最后更新**: 2025 年 10 月 26 日
