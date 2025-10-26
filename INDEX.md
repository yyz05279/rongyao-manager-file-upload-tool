# 📚 熔盐管理文件上传工具 - 项目文档索引

快速找到你需要的文档和脚本！

---

## 🎯 快速导航

### 📖 项目结构说明

| 文档                                     | 说明                                       | 适合人群          |
| ---------------------------------------- | ------------------------------------------ | ----------------- |
| **项目结构说明.md**                      | ⭐ 项目整体结构，区分 Tauri 和 Python 版本 | 推荐首先阅读      |
| **[tauri-app/docs/](tauri-app/docs/)**   | Tauri 版本详细文档（15+ 个）               | Tauri 开发者必读  |
| **[python-app/docs/](python-app/docs/)** | Python 版本详细文档                        | Python 开发者必读 |

### 🚀 立即开始

**Tauri 版本（推荐）:**

```bash
# 进入Tauri目录
cd tauri-app

# 安装依赖
npm install

# 启动开发模式
npm run tauri dev
```

**Python 版本:**

```bash
# 进入 Python 目录
cd python-app

# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

**详细指南**: 阅读 `TAURI_QUICKSTART.md` 或 `PROJECT_SUMMARY.md`

---

## 📖 所有文档

### 📂 文档分类导航

| 分类            | 位置               | 说明                             |
| --------------- | ------------------ | -------------------------------- |
| **Tauri 文档**  | `tauri-app/docs/`  | Tauri 版本相关文档（15+ 个）     |
| **Python 文档** | `python-app/docs/` | Python 版本相关文档              |
| **通用文档**    | `docs/`            | 项目通用文档（13+ 个）           |
| **历史记录**    | `docs/历史记录/`   | 历史文档归档（13+ 个）           |
| **API 文档**    | `api/`             | API 接口文档                     |
| **核心文档**    | 根目录             | 项目核心文档（README、INDEX 等） |

---

### 📋 总结类文档

| 文档                                                                     | 说明                       | 适合人群          |
| ------------------------------------------------------------------------ | -------------------------- | ----------------- |
| **项目结构说明.md**                                                      | ⭐ 项目整体架构和目录说明  | 推荐首先阅读      |
| **文档整理完成说明.md**                                                  | 文档整理说明，查找指南     | 需要查找文档      |
| **目录重组完成说明.md**                                                  | 目录重组说明               | 了解目录变更      |
| **[docs/项目总结.md](docs/项目总结.md)**                                 | 项目完整总结，包含所有信息 | 想了解项目全貌    |
| **[tauri-app/docs/TAURI_COMPLETE.md](tauri-app/docs/TAURI_COMPLETE.md)** | 完成报告，包含亮点和功能   | 想了解 Tauri 版本 |
| **[docs/迁移总结.md](docs/迁移总结.md)**                                 | 迁移总结，为什么选择 Tauri | 想了解迁移决策    |

### 📚 详细指南

| 文档                                                                         | 说明                    | 适合人群           |
| ---------------------------------------------------------------------------- | ----------------------- | ------------------ |
| **[tauri-app/docs/](tauri-app/docs/)**                                       | Tauri 项目完整文档目录  | Tauri 开发者       |
| **[python-app/docs/](python-app/docs/)**                                     | Python 项目完整文档目录 | Python 开发者      |
| **[tauri-app/docs/TAURI_QUICKSTART.md](tauri-app/docs/TAURI_QUICKSTART.md)** | 30 分钟快速开始         | 希望快速上手       |
| **[docs/Tauri 迁移方案.md](docs/Tauri迁移方案.md)**                          | 详细技术方案和代码      | 想深入了解技术细节 |
| **[docs/方案对比分析.md](docs/方案对比分析.md)**                             | PyQt6 vs Tauri 对比     | 想了解技术选择     |
| **[docs/检查清单.md](docs/检查清单.md)**                                     | 详细任务清单            | 需要一步步指导     |

### 🔧 实用工具

| 脚本                      | 说明         | 使用方法                     |
| ------------------------- | ------------ | ---------------------------- |
| **START_DEV.sh**          | 开发启动脚本 | `bash START_DEV.sh`          |
| **INIT_TAURI_PROJECT.sh** | 项目初始化   | `bash INIT_TAURI_PROJECT.sh` |
| **START_MIGRATION.sh**    | 环境检查     | `bash START_MIGRATION.sh`    |

---

## 📂 项目文件结构

```
/Users/yyz/Desktop/熔盐管理文件上传工具/
│
├── 📚 文档文件
│   ├── INDEX.md                         ← 你在这里
│   ├── 项目结构说明.md                   ⭐ 项目整体结构
│   ├── TAURI_PROJECT_STRUCTURE.md       Tauri版本结构
│   ├── PYTHON_PROJECT_STRUCTURE.md      Python版本结构
│   ├── PROJECT_SUMMARY.md               项目完整总结
│   ├── TAURI_COMPLETE.md                Tauri完成报告
│   ├── TAURI_QUICKSTART.md              快速开始指南
│   ├── MIGRATION_SUMMARY.md             迁移总结
│   ├── CHECKLIST.md                     任务清单
│   └── docs/                            详细文档目录
│       ├── Tauri迁移方案.md             技术方案
│       ├── 方案对比分析.md              方案对比
│       └── ... (50+ 文档)
│
├── 🚀 启动脚本
│   ├── START_DEV.sh                     开发启动脚本
│   ├── INIT_TAURI_PROJECT.sh            项目初始化
│   ├── START_MIGRATION.sh               环境检查
│   ├── build_macos.sh                   macOS打包
│   ├── build_windows.bat                Windows打包
│   └── run_macos.sh                     运行Python版本
│
├── 📦 Tauri应用（推荐使用）
│   └── tauri-app/                       Tauri 应用目录
│       ├── src/                         React 前端代码
│       │   ├── components/              4 个组件
│       │   ├── stores/                  状态管理
│       │   ├── services/                API封装
│       │   ├── App.jsx                  主应用
│       │   └── index.css                全局样式
│       ├── src-tauri/                   Rust 后端代码
│       │   ├── src/
│       │   │   ├── api/                 API模块
│       │   │   ├── commands/            Tauri命令
│       │   │   ├── utils/               工具函数
│       │   │   └── main.rs              入口文件
│       │   └── Cargo.toml               Rust依赖
│       ├── package.json                 Node依赖
│       └── vite.config.js               构建配置
│
├── 🐍 Python 应用（备用）
│   └── python-app/                      Python 版本目录
│       ├── main.py                      Python 入口
│       ├── ui/                          PyQt 界面
│       │   ├── main_window.py           主窗口
│       │   ├── login_widget.py          登录界面
│       │   └── upload_widget.py         上传界面
│       ├── services/                    服务层
│       │   ├── auth_service.py          认证服务
│       │   ├── project_service.py       项目服务
│       │   └── upload_service.py        上传服务
│       ├── run_macos.sh                 macOS 运行脚本
│       ├── build_macos.sh               macOS 打包脚本
│       ├── requirements.txt             Python 依赖
│       └── 熔盐管理文件上传工具.spec    打包配置
│
├── 📋 API文档
│   └── api/
│       ├── 01-用户认证模块API.md
│       └── 19-项目日报批量导入API.md
│
└── 🔧 配置文件
    ├── .gitignore                       Git忽略配置
    └── API_URL_CONFIG.md                API配置说明
```

---

## 🎯 按场景选择文档

### 🆕 我是新用户，刚接触这个项目

**推荐阅读顺序：**

1. 这个文件 (INDEX.md) - 快速了解项目
2. `项目结构说明.md` - ⭐ 理解项目整体架构
3. `PROJECT_SUMMARY.md` - 了解项目全貌
4. `TAURI_QUICKSTART.md` - 快速启动

### 👨‍💻 我是 Tauri 开发者

**推荐阅读：**

1. `项目结构说明.md` - 了解整体架构
2. `TAURI_PROJECT_STRUCTURE.md` - Tauri 项目详细结构
3. `docs/Tauri迁移方案.md` - 技术方案和代码
4. 直接查看 `tauri-app/` 源代码

### 🐍 我是 Python 开发者

**推荐阅读：**

1. `项目结构说明.md` - 了解整体架构
2. `PYTHON_PROJECT_STRUCTURE.md` - Python 项目详细结构
3. 直接查看 `python-app/main.py`、`python-app/ui/`、`python-app/services/` 源代码

### 🤔 我想了解为什么选择 Tauri

**推荐阅读：**

1. `项目结构说明.md` - 版本对比
2. `docs/方案对比分析.md` - 详细对比
3. `MIGRATION_SUMMARY.md` - 迁移原因
4. `TAURI_COMPLETE.md` - 项目亮点

### 🚀 我想立即开始开发

**Tauri 版本（推荐）：**

```bash
# 进入目录
cd tauri-app

# 安装依赖（首次）
npm install

# 启动开发模式
npm run tauri dev
```

**Python 版本：**

```bash
# 进入 Python 目录
cd python-app

# 安装依赖（首次）
pip install -r requirements.txt

# 运行应用
python main.py
```

---

## 📊 项目统计

### Tauri 版本

| 项         | 数值    |
| ---------- | ------- |
| React 组件 | 4 个    |
| Rust 模块  | 5 个    |
| Tauri 命令 | 8 个    |
| npm 依赖   | 110+ 个 |
| 代码行数   | ~1500+  |
| 完成度     | 90% ✅  |

### Python 版本

| 项          | 数值   |
| ----------- | ------ |
| PyQt 组件   | 4 个   |
| 服务模块    | 6 个   |
| Python 依赖 | 6 个   |
| 代码行数    | ~2000+ |
| 完成度      | 85% ✅ |

### 文档统计

| 项       | 数值   |
| -------- | ------ |
| 总文档数 | 60+ 篇 |
| API 文档 | 2 篇   |
| 脚本文件 | 8 个   |

---

## 💡 核心命令速查

### Tauri 版本命令

```bash
# 开发
cd tauri-app
npm run dev                      # 启动前端开发服务器
npm run tauri dev                # 启动Tauri开发模式（推荐）

# 构建
npm run build                    # 构建前端
npm run tauri build              # 构建可执行文件
cd src-tauri && cargo build --release  # Release模式编译Rust

# 维护
npm install                      # 安装Node依赖
cargo clean                      # 清理Rust缓存
npm audit                        # 检查依赖安全

# 信息
npm list                         # 查看npm依赖
cargo --version                  # 查看Cargo版本
rustc --version                  # 查看Rust版本
```

### Python 版本命令

```bash
# 进入目录
cd python-app

# 开发
python main.py                   # 运行应用
./run_macos.sh                   # macOS 启动脚本

# 打包
./build_macos.sh                 # macOS 打包
./build_windows.bat              # Windows 打包（Windows 系统）
pyinstaller 熔盐管理文件上传工具.spec  # 使用 spec 文件打包

# 维护
pip install -r requirements.txt  # 安装依赖
pip list                         # 查看已安装包
pip freeze > requirements.txt    # 更新依赖列表

# 信息
python --version                 # 查看 Python 版本
pip show PyQt5                   # 查看包信息
```

---

## 🧠 核心概念速查

### Tauri 架构流程

**IPC 通信流程:**

```
React 前端
  ↓
authStore.js (Zustand状态管理)
  ↓
api.js (IPC层 - invoke调用)
  ↓
Tauri 框架
  ↓
main.rs (Rust - 命令注册)
  ↓
commands/ (认证/项目/上传命令)
  ↓
api/ (HTTP请求)
  ↓
后端API服务器
```

**状态管理:**

```
localStorage (持久化存储)
  ↓
Zustand store (内存状态)
  ↓
React components (UI组件)
```

### Python 架构流程

**应用流程:**

```
python-app/main.py (入口)
  ↓
MainWindow (主窗口)
  ↓
LoginWidget / UploadWidget (界面组件)
  ↓
services/ (服务层)
  ↓
BaseService (HTTP 客户端)
  ↓
后端 API 服务器
```

**状态管理:**

```
AppState (全局单例)
  ↓
Token / UserInfo (内存状态)
  ↓
ConfigService (配置持久化)
  ↓
JSON文件 (~/.molten_salt_manager/)
```

---

## 🔍 常见问题速查

### Tauri 版本问题

**前端问题:**

- ❌ 前端不显示？

  - 检查 `npm run dev` 是否运行
  - 检查端口是否为 5173
  - 清空浏览器缓存
  - 查看控制台错误信息

- ❌ npm install 失败？
  - 使用 `npm install --legacy-peer-deps`
  - 检查网络连接
  - 删除 `node_modules` 和 `package-lock.json` 后重试

**后端问题:**

- ❌ cargo build 失败？

  - 运行 `cargo clean` 后重试
  - 检查 Rust 版本 (1.90+)
  - 检查 Cargo.toml 配置

- ❌ IPC 通信失败？
  - 检查 Rust 命令名称与前端调用是否一致
  - 查看浏览器控制台错误
  - 检查 tauri.conf.json 权限配置

### Python 版本问题

**运行问题:**

- ❌ 导入错误？

  - 检查是否安装了所有依赖: `pip install -r requirements.txt`
  - 检查 Python 版本 (3.8+)
  - 确认虚拟环境是否激活

- ❌ PyQt5 错误？
  - 重新安装: `pip uninstall PyQt5 && pip install PyQt5`
  - macOS 可能需要: `brew install qt@5`
  - Windows 需要确保安装了 VC++运行库

**打包问题:**

- ❌ PyInstaller 打包失败？

  - 运行 `pyinstaller --clean 熔盐管理文件上传工具.spec`
  - 删除 `build/` 和 `dist/` 后重试
  - 检查隐藏导入是否完整

- ❌ 打包后无法运行？
  - 检查资源文件是否正确打包（ui/, services/）
  - 查看日志文件获取错误信息
  - 使用 `--debug` 模式重新打包

---

## 📞 获取帮助

### 文档资源

- **Tauri 官方文档**: https://tauri.app
- **React 官方文档**: https://react.dev
- **Rust 官方文档**: https://doc.rust-lang.org

### 本地资源

查看各文档中的"问题排查"章节

---

## ✨ 项目亮点

- 🎨 现代 UI 设计
- 📱 响应式界面
- ⚡ 极速性能
- 🔐 安全认证
- 📤 完整上传
- 🛠️ 易于维护
- 🌍 跨平台支持

---

## 🎊 下一步

### 立即做

```bash
# 1. 启动前端开发
cd tauri-app
npm run dev

# 2. 在新终端编译后端
cd tauri-app/src-tauri
cargo build

# 3. 打开浏览器测试
open http://localhost:5173
```

### 之后

- 连接到你的 API 服务器
- 测试登录和上传功能
- 根据需要调整 UI
- 构建可执行文件

---

## 📝 文档更新记录

| 时间       | 更新                          | 版本 |
| ---------- | ----------------------------- | ---- |
| 2025-10-26 | 创建项目结构说明文档          | v2.0 |
| 2025-10-26 | 区分 Tauri 和 Python 项目结构 | v2.0 |
| 2025-10-26 | 更新 INDEX.md 文档索引        | v2.0 |
| 2025-10-24 | 创建完整文档体系              | v1.5 |
| 2025-10-24 | 完成前端开发                  | v1.0 |
| 2025-10-24 | 完成后端开发                  | v1.0 |
| 2025-10-24 | 创建启动脚本                  | v1.0 |

---

## 🎯 项目路线图

### Tauri 版本

```
✅ 环境配置          完成
✅ React前端开发      完成
✅ Rust后端开发       完成
✅ IPC通信集成        完成
✅ 状态管理          完成
⏳ 功能测试          进行中 (90%)
⏳ 性能优化          待开始
⏳ 自动更新          待开始
⏳ CI/CD配置         待开始
```

### Python 版本

```
✅ PyQt界面开发       完成
✅ 服务层实现         完成
✅ Excel解析         完成
✅ macOS打包         完成
✅ Windows打包       完成
⏳ 功能测试          进行中 (85%)
⏳ Bug修复           待开始
```

---

## 🎊 下一步行动

### 立即开始（推荐 Tauri 版本）

```bash
# 1️⃣ 阅读项目结构
cat 项目结构说明.md
cat TAURI_PROJECT_STRUCTURE.md

# 2️⃣ 进入Tauri目录
cd tauri-app

# 3️⃣ 安装依赖
npm install

# 4️⃣ 启动开发
npm run tauri dev
```

### 或使用 Python 版本

```bash
# 1️⃣ 阅读项目结构
cat 项目结构说明.md
cat PYTHON_PROJECT_STRUCTURE.md

# 2️⃣ 进入 Python 目录
cd python-app

# 3️⃣ 安装依赖
pip install -r requirements.txt

# 4️⃣ 运行应用
python main.py
```

---

**最后更新**: 2025-10-26  
**项目状态**: 🟢 **两个版本均可运行**  
**推荐版本**: ⭐ **Tauri 版本**（更现代化、性能更好）

---

## 🎉 总结

本项目提供了两个独立的实现：

1. **Tauri 版本** - 使用 React + Rust，现代化、高性能、体积小
2. **Python 版本** - 使用 PyQt5，传统桌面应用，成熟稳定

两个版本共享相同的 API 接口和业务逻辑，可以根据团队技术栈和需求选择合适的版本。

现在开始你的开发之旅吧！🚀
