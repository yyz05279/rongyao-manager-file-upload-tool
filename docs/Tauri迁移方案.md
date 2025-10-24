# 🚀 Tauri 迁移方案

## 📋 项目概况分析

### 当前架构 (PyQt6)

```
PyQt6 GUI 前端 ────────────┐
                            ├──→ Python 后端服务
Qthread 异步处理 ───────────┘

后端服务:
- AuthService (登录认证)
- ProjectService (项目查询)
- UploadService (Excel 解析上传)
- ConfigService (配置管理)
```

### 目标架构 (Tauri + Rust)

```
React/Vue 前端 ─────────────┐
IPC Bridge                  ├──→ Tauri Rust 后端
Hooks 状态管理 ─────────────┘

Rust 后端:
- 认证模块 (HTTP 请求)
- 项目模块 (API 调用)
- 上传模块 (Excel 解析 + HTTP)
- 工具模块 (文件管理)
```

---

## 🎯 迁移路线图

### 第一阶段: 项目初始化 (1-2 小时)

#### 1.1 安装 Rust 和 Tauri

```bash
# 安装 Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 验证安装
rustc --version
cargo --version

# 全局安装 Tauri CLI
cargo install tauri-cli

# 验证
cargo tauri --version
```

#### 1.2 初始化 Tauri 项目

```bash
# 在项目根目录初始化 Tauri
cargo tauri init

# 配置参数:
# - 项目名: molten-salt-upload
# - 窗口标题: 熔盐管理文件上传工具
# - 前端: React (或 Vue)
# - 打包工具: npm
```

#### 1.3 项目结构设置

```
熔盐管理文件上传工具/
├── src-tauri/                 # Rust 后端
│   ├── src/
│   │   ├── main.rs           # 入口
│   │   ├── auth.rs           # 认证模块
│   │   ├── project.rs        # 项目模块
│   │   ├── upload.rs         # 上传模块
│   │   ├── excel.rs          # Excel 解析
│   │   └── models.rs         # 数据模型
│   ├── Cargo.toml
│   └── tauri.conf.json
├── src/                       # React/Vue 前端
│   ├── components/
│   │   ├── LoginForm.jsx
│   │   ├── UploadForm.jsx
│   │   └── ProgressBar.jsx
│   ├── hooks/
│   │   ├── useAuth.js
│   │   └── useUpload.js
│   ├── services/
│   │   └── api.js            # IPC 调用
│   └── App.jsx
├── package.json
└── README.md
```

---

### 第二阶段: Rust 后端迁移 (3-4 小时)

#### 2.1 配置 Cargo.toml

```toml
[package]
name = "molten-salt-upload"
version = "1.0.0"

[dependencies]
tauri = { version = "2", features = ["all"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
reqwest = { version = "0.11", features = ["json"] }
openpyxl = "0.0.2"  # 或用 calamine crate
calamine = "0.22"   # Excel 解析 (推荐)
regex = "1"
chrono = "0.4"
```

#### 2.2 创建认证模块 (src-tauri/src/auth.rs)

```rust
use serde::{Deserialize, Serialize};
use regex::Regex;
use tauri::State;

#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct AuthResponse {
    pub token: String,
    pub refresh_token: String,
    pub user_info: UserInfo,
}

#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct UserInfo {
    pub id: i32,
    pub username: String,
    pub email: String,
}

pub struct AuthService {
    api_base_url: String,
    token: Option<String>,
    refresh_token: Option<String>,
}

impl AuthService {
    pub fn new(api_base_url: String) -> Self {
        Self {
            api_base_url,
            token: None,
            refresh_token: None,
        }
    }

    /// 判断是否是手机号
    fn is_phone_number(value: &str) -> bool {
        let phone_regex = Regex::new(r"^1\d{10}$").unwrap();
        phone_regex.is_match(&value.replace(&[' ', '-', '(', ')'][..], ""))
    }

    /// 用户登录 (Tauri Command)
    pub async fn login(&mut self, username: &str, password: &str) -> Result<AuthResponse, String> {
        let client = reqwest::Client::new();
        let login_url = format!("{}/api/v1/auth/login", self.api_base_url);

        let payload = serde_json::json!({
            "username": username,
            "password": password,
        });

        let response = client
            .post(&login_url)
            .json(&payload)
            .send()
            .await
            .map_err(|e| format!("请求失败: {}", e))?;

        if response.status() != 200 {
            return Err("登录失败: 用户名或密码错误".to_string());
        }

        let data: AuthResponse = response
            .json()
            .await
            .map_err(|e| format!("解析响应失败: {}", e))?;

        self.token = Some(data.token.clone());
        self.refresh_token = Some(data.refresh_token.clone());

        Ok(data)
    }

    pub fn get_token(&self) -> Option<&str> {
        self.token.as_deref()
    }
}
```

#### 2.3 创建项目模块 (src-tauri/src/project.rs)

```rust
use serde::{Deserialize, Serialize};

#[derive(Clone, Serialize, Deserialize, Debug)]
pub struct ProjectInfo {
    pub id: i32,
    pub name: String,
    pub type_display_name: String,
    pub status_display_name: String,
    pub manager: String,
}

pub struct ProjectService {
    api_base_url: String,
    token: String,
}

impl ProjectService {
    pub fn new(api_base_url: String, token: String) -> Self {
        Self {
            api_base_url,
            token,
        }
    }

    /// 获取用户项目 (Tauri Command)
    pub async fn get_my_project(&self) -> Result<ProjectInfo, String> {
        let client = reqwest::Client::new();
        let url = format!("{}/api/v1/projects/my-project", self.api_base_url);

        let response = client
            .get(&url)
            .header("Authorization", format!("Bearer {}", self.token))
            .send()
            .await
            .map_err(|e| format!("请求失败: {}", e))?;

        if response.status() != 200 {
            return Err("获取项目信息失败".to_string());
        }

        let data: ProjectInfo = response
            .json()
            .await
            .map_err(|e| format!("解析数据失败: {}", e))?;

        Ok(data)
    }
}
```

#### 2.4 创建上传模块 (src-tauri/src/upload.rs)

```rust
use serde_json::json;
use tauri::api::dialog::FileDialogBuilder;

pub struct UploadService {
    api_base_url: String,
    token: String,
}

impl UploadService {
    pub fn new(api_base_url: String, token: String) -> Self {
        Self {
            api_base_url,
            token,
        }
    }

    /// 上传日报 (Tauri Command)
    pub async fn upload_daily_report(
        &self,
        file_path: String,
        project_id: i32,
        reporter_id: i32,
    ) -> Result<String, String> {
        // 1. 解析 Excel (调用 excel.rs 模块)
        let data = parse_excel(&file_path)?;

        // 2. 转换为 API 格式
        let api_data = convert_to_api_format(data, project_id, reporter_id)?;

        // 3. 调用上传 API
        let client = reqwest::Client::new();
        let url = format!("{}/api/v1/daily-reports/batch-import", self.api_base_url);

        let response = client
            .post(&url)
            .header("Authorization", format!("Bearer {}", self.token))
            .json(&api_data)
            .send()
            .await
            .map_err(|e| format!("上传失败: {}", e))?;

        if response.status() != 200 {
            return Err("服务器返回错误".to_string());
        }

        Ok("上传成功".to_string())
    }
}

fn parse_excel(file_path: &str) -> Result<Vec<serde_json::Value>, String> {
    // 使用 calamine crate 解析 Excel
    // 返回解析后的数据
    Ok(vec![])
}

fn convert_to_api_format(
    data: Vec<serde_json::Value>,
    project_id: i32,
    reporter_id: i32,
) -> Result<serde_json::Value, String> {
    // 转换数据格式
    Ok(json!({"data": data}))
}
```

#### 2.5 主程序入口 (src-tauri/src/main.rs)

```rust
// Prevents additional console window on Windows in release, MUST COME BEFORE ANY OTHER ITEMS
#![cfg_attr(all(not(debug_assertions), target_os = "windows"), windows_subsystem = "windows")]

mod auth;
mod project;
mod upload;
mod excel;

use tauri::State;
use auth::{AuthService, AuthResponse};
use project::ProjectService;
use upload::UploadService;

// 全局应用状态
struct AppState {
    api_base_url: String,
}

#[tauri::command]
async fn cmd_login(
    username: String,
    password: String,
    api_url: String,
    state: State<'_, AppState>,
) -> Result<AuthResponse, String> {
    let mut auth = AuthService::new(api_url);
    auth.login(&username, &password).await
}

#[tauri::command]
async fn cmd_get_project(
    token: String,
    state: State<'_, AppState>,
) -> Result<project::ProjectInfo, String> {
    let service = ProjectService::new(state.api_base_url.clone(), token);
    service.get_my_project().await
}

#[tauri::command]
async fn cmd_upload_file(
    file_path: String,
    project_id: i32,
    reporter_id: i32,
    token: String,
    state: State<'_, AppState>,
) -> Result<String, String> {
    let service = UploadService::new(state.api_base_url.clone(), token);
    service.upload_daily_report(file_path, project_id, reporter_id).await
}

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            cmd_login,
            cmd_get_project,
            cmd_upload_file,
            greet
        ])
        .manage(AppState {
            api_base_url: "http://your-api.com".to_string(),
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

---

### 第三阶段: 前端迁移 (4-5 小时)

#### 3.1 React 项目初始化

```bash
# 使用 Tauri 创建 React 模板
cargo tauri init --app-name molten-salt-upload --ui react

# 或手动配置
npm install react react-dom
npm install axios zustand
npm install @tauri-apps/api
```

#### 3.2 IPC 通信层 (src/services/api.js)

```javascript
import { invoke } from "@tauri-apps/api/tauri";

export const authAPI = {
  login: (username, password, apiUrl) =>
    invoke("cmd_login", { username, password, apiUrl }),

  logout: () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
  },
};

export const projectAPI = {
  getMyProject: (token) => invoke("cmd_get_project", { token }),
};

export const uploadAPI = {
  uploadFile: (filePath, projectId, reporterId, token) =>
    invoke("cmd_upload_file", {
      file_path: filePath,
      project_id: projectId,
      reporter_id: reporterId,
      token,
    }),
};
```

#### 3.3 状态管理 (src/stores/authStore.js)

```javascript
import { create } from "zustand";

export const useAuthStore = create((set) => ({
  token: localStorage.getItem("token"),
  userInfo: JSON.parse(localStorage.getItem("userInfo") || "{}"),

  login: async (username, password, apiUrl) => {
    const response = await authAPI.login(username, password, apiUrl);
    localStorage.setItem("token", response.token);
    localStorage.setItem("refresh_token", response.refresh_token);
    localStorage.setItem("userInfo", JSON.stringify(response.user_info));
    set({ token: response.token, userInfo: response.user_info });
  },

  logout: () => {
    authAPI.logout();
    set({ token: null, userInfo: {} });
  },
}));
```

#### 3.4 登录组件 (src/components/LoginForm.jsx)

```jsx
import React, { useState } from "react";
import { useAuthStore } from "../stores/authStore";
import "./LoginForm.css";

export function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [apiUrl, setApiUrl] = useState("http://api.example.com");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const login = useAuthStore((state) => state.login);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await login(username, password, apiUrl);
      onLoginSuccess();
    } catch (err) {
      setError(err.message || "登录失败");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h1>熔盐管理文件上传工具</h1>

        <div className="form-group">
          <label>API 服务器:</label>
          <input
            type="text"
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
            placeholder="http://api.example.com"
          />
        </div>

        <div className="form-group">
          <label>用户名/手机号:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="输入用户名或手机号"
          />
        </div>

        <div className="form-group">
          <label>密码:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="输入密码"
          />
        </div>

        {error && <div className="error-message">{error}</div>}

        <button type="submit" disabled={loading} className="btn-login">
          {loading ? "登录中..." : "登录"}
        </button>
      </form>
    </div>
  );
}
```

#### 3.5 上传组件 (src/components/UploadForm.jsx)

```jsx
import React, { useState } from "react";
import { open } from "@tauri-apps/api/dialog";
import { uploadAPI } from "../services/api";
import { useAuthStore } from "../stores/authStore";
import "./UploadForm.css";

export function UploadForm() {
  const [filePath, setFilePath] = useState("");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const { token, userInfo } = useAuthStore();
  const projectInfo = useProjectStore();

  const handleSelectFile = async () => {
    const file = await open({
      filters: [{ name: "Excel", extensions: ["xlsx", "xls"] }],
    });
    setFilePath(file);
  };

  const handleUpload = async () => {
    if (!filePath) {
      setMessage("请先选择文件");
      return;
    }

    setLoading(true);
    try {
      const result = await uploadAPI.uploadFile(
        filePath,
        projectInfo.id,
        userInfo.id,
        token
      );
      setMessage("上传成功: " + result);
      setUploadProgress(100);
    } catch (err) {
      setMessage("上传失败: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <div className="file-selector">
        <input
          type="text"
          value={filePath}
          readOnly
          placeholder="选择 Excel 文件"
        />
        <button onClick={handleSelectFile}>选择文件</button>
      </div>

      <div className="progress-bar">
        <div className="progress" style={{ width: `${uploadProgress}%` }} />
      </div>

      <button
        onClick={handleUpload}
        disabled={loading || !filePath}
        className="btn-upload"
      >
        {loading ? "上传中..." : "开始上传"}
      </button>

      {message && <div className="message">{message}</div>}
    </div>
  );
}
```

---

### 第四阶段: Excel 解析迁移 (2-3 小时)

#### 4.1 Rust Excel 解析 (src-tauri/src/excel.rs)

```rust
use calamine::{Reader, Xlsx};
use serde_json::{json, Value};

pub fn parse_excel_file(file_path: &str) -> Result<Vec<Value>, String> {
    let mut workbook = Xlsx::open(file_path)
        .map_err(|e| format!("无法打开 Excel 文件: {}", e))?;

    let mut all_data = Vec::new();

    for sheet_name in workbook.sheet_names() {
        let sheet_data = parse_sheet(&mut workbook, &sheet_name)?;
        all_data.extend(sheet_data);
    }

    Ok(all_data)
}

fn parse_sheet(
    workbook: &mut Xlsx<std::fs::File>,
    sheet_name: &str,
) -> Result<Vec<Value>, String> {
    let range = workbook
        .worksheet_range(sheet_name)
        .map_err(|e| format!("读取工作表失败: {}", e))?
        .map_err(|e| format!("工作表范围错误: {}", e))?;

    let mut data = Vec::new();

    for row in range.rows().skip(1) {  // 跳过标题行
        let record = json!({
            "date": row.get(0).map(|v| v.to_string()),
            "content": row.get(1).map(|v| v.to_string()),
            "status": row.get(2).map(|v| v.to_string()),
        });
        data.push(record);
    }

    Ok(data)
}
```

---

### 第五阶段: 测试与优化 (2 小时)

#### 5.1 编译和测试

```bash
# 开发模式运行
cargo tauri dev

# 检查编译错误
cargo build

# 发布编译
cargo tauri build
```

#### 5.2 性能优化建议

| 优化项   | 方案       | 预期效果    |
| -------- | ---------- | ----------- |
| 包体积   | UPX 压缩   | 减少 30-40% |
| 启动速度 | 预加载资源 | 减少 50%    |
| 内存占用 | 异步操作   | 减少 60%    |

---

### 第六阶段: CI/CD 配置 (1 小时)

#### 6.1 GitHub Actions 多平台打包

```yaml
# .github/workflows/tauri-build.yml
name: Build Tauri App

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-tauri:
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: ubuntu-latest
            rust_target: x86_64-unknown-linux-gnu
          - os: macos-latest
            rust_target: x86_64-apple-darwin
          - os: windows-latest
            rust_target: x86_64-pc-windows-msvc

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v3

      - name: Install Node
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable

      - name: Cache cargo
        uses: Swatinem/rust-cache@v2
        with:
          workspaces: "src-tauri"

      - name: Install dependencies (Ubuntu)
        if: matrix.os == 'ubuntu-latest'
        run: |
          sudo apt-get update
          sudo apt-get install -y libgtk-3-dev libwebkit2gtk-4.0-dev libappindicator3-dev librsvg2-dev patchelf

      - name: Build app
        run: npm install && npm run build

      - name: Build Tauri
        run: npm run tauri build

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: tauri-app-${{ matrix.os }}
          path: src-tauri/target/release/bundle/
```

---

## 📊 迁移对比

### 性能提升

| 指标     | PyInstaller | Tauri    | 提升         |
| -------- | ----------- | -------- | ------------ |
| 包体积   | 150MB       | 60MB     | **减少 60%** |
| 启动时间 | 3-4s        | 0.5-1s   | **减少 75%** |
| 内存占用 | 200-300MB   | 80-120MB | **减少 60%** |
| CPU 占用 | 高          | 低       | **减少 50%** |

### 开发体验

| 方面       | PyQt6      | Tauri+React            |
| ---------- | ---------- | ---------------------- |
| 热加载     | ❌         | ✅                     |
| 调试工具   | 基础       | 完整 (Chrome DevTools) |
| 跨平台编译 | 需分别打包 | 一次编译               |
| 依赖管理   | pip        | npm + cargo            |

---

## ⚠️ 注意事项

1. **Rust 学习成本**: 需要基本的 Rust 语法理解
2. **Excel 库选择**: `calamine` 性能最优，但功能较少；`rust-excel` 功能全面
3. **跨平台测试**: 务必在 Win/Mac/Linux 上都测试一遍
4. **签名和公证**: macOS 发布需要开发者账号

---

## 🔄 迁移时间表

| 阶段     | 预计时间   | 备注         |
| -------- | ---------- | ------------ |
| 第一阶段 | 1-2h       | 环境配置     |
| 第二阶段 | 3-4h       | Rust 后端    |
| 第三阶段 | 4-5h       | React 前端   |
| 第四阶段 | 2-3h       | Excel 解析   |
| 第五阶段 | 2h         | 测试优化     |
| 第六阶段 | 1h         | CI/CD        |
| **总计** | **13-18h** | 2-3 天工作量 |

---

## 📚 参考资源

- [Tauri 官方文档](https://tauri.app/en/docs/)
- [Rust 学习资源](https://www.rust-lang.org/learn)
- [Calamine Excel 解析](https://docs.rs/calamine/)
- [Tauri IPC 通信](https://tauri.app/en/docs/features/command)
- [React + Tauri 实例](https://github.com/tauri-apps/tauri-docs/tree/dev/examples)
