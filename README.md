# 熔盐管理文件上传工具

> 一个用于熔盐管理系统的桌面文件上传工具，提供 **Tauri** 和 **Python** 两个版本

---

## 🚀 快速开始

### Tauri 版本（推荐）

```bash
cd tauri-app
npm install
npm run tauri dev
```

### Python 版本

```bash
cd python-app
pip install -r requirements.txt
python main.py
```

---

## 📖 文档导航

### 必读文档

- **[项目结构说明.md](./项目结构说明.md)** - ⭐ 首先阅读，了解项目整体结构
- **[INDEX.md](./INDEX.md)** - 完整文档索引和快速导航
- **[macOS 应用快速修复卡片.md](./macOS应用快速修复卡片.md)** - 🚨 应用无法打开？1 分钟修复

### 详细文档

- **[TAURI_PROJECT_STRUCTURE.md](./TAURI_PROJECT_STRUCTURE.md)** - Tauri 版本详细结构
- **[PYTHON_PROJECT_STRUCTURE.md](./PYTHON_PROJECT_STRUCTURE.md)** - Python 版本详细结构
- **[TAURI_QUICKSTART.md](./TAURI_QUICKSTART.md)** - Tauri 快速开始指南
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - 项目完整总结

### 打包和部署

- **[docs/Tauri-CI-CD-QuickStart.md](./docs/Tauri-CI-CD-QuickStart.md)** - 5 分钟配置自动打包和签名
- **[docs/macOS 应用无法打开解决方案.md](./docs/macOS应用无法打开解决方案.md)** - macOS 安全问题完整解决方案
- **[打包指南.md](./打包指南.md)** - 跨平台打包完整指南

---

## 📦 项目结构

```
熔盐管理文件上传工具/
├── tauri-app/              # Tauri 版本（React + Rust）
│   ├── src/                # React 前端
│   └── src-tauri/          # Rust 后端
│
├── python-app/             # Python 版本
│   ├── main.py             # Python 入口
│   ├── ui/                 # PyQt 界面
│   └── services/           # 服务层
│
├── docs/                   # 文档目录
├── api/                    # API 接口文档
└── README.md               # 本文件
```

---

## ✨ 主要功能

- ✅ 用户登录认证
- ✅ Token 自动刷新
- ✅ 项目选择
- ✅ Excel 文件解析
- ✅ 数据预览
- ✅ 批量上传
- ✅ 进度显示
- ✅ 覆盖选项

---

## 🔧 技术栈

### Tauri 版本

- **前端**: React 18 + Vite + Zustand
- **后端**: Rust + Tauri 2.x
- **Excel 解析**: calamine
- **HTTP 客户端**: axios (前端) + reqwest (Rust)

### Python 版本

- **界面**: PyQt5
- **HTTP 客户端**: requests
- **Excel 解析**: openpyxl + pandas
- **打包**: PyInstaller

---

## 📊 版本对比

| 特性         | Tauri 版本          | Python 版本   |
| ------------ | ------------------- | ------------- |
| **性能**     | ⭐⭐⭐⭐⭐          | ⭐⭐⭐        |
| **体积**     | ~5MB                | ~50MB+        |
| **界面**     | 现代化 Web 界面     | 原生桌面界面  |
| **跨平台**   | Windows/macOS/Linux | Windows/macOS |
| **开发效率** | 高                  | 中            |
| **维护性**   | 优秀                | 良好          |

**推荐使用**: ⭐ Tauri 版本

---

## 🛠️ 开发命令

### Tauri 版本

```bash
npm run tauri dev      # 开发模式
npm run tauri build    # 构建应用
```

### Python 版本

```bash
cd python-app
python main.py              # 运行应用
./build_macos.sh           # macOS 打包
./build_windows.bat        # Windows 打包
```

---

## 📝 开发指南

1. **阅读文档**: 从 [项目结构说明.md](./项目结构说明.md) 开始
2. **选择版本**: Tauri 版本（推荐）或 Python 版本
3. **安装依赖**: 按照上述快速开始步骤操作
4. **开始开发**: 参考对应版本的详细结构文档

---

## 🐛 常见问题

### ⚠️ macOS 应用无法打开？

**问题**: 提示"这台 Mac 不支持此应用程序"

**快速修复**:

```bash
# 在项目根目录运行
./fix-macos-app.sh auto
```

**详细说明**: 查看 [macOS 应用无法打开解决方案.md](./docs/macOS应用无法打开解决方案.md)

---

### Tauri 版本

- **前端不显示**: 检查端口 5173 是否被占用
- **Rust 编译失败**: 运行 `cargo clean` 后重试
- **依赖安装失败**: 使用 `npm install --legacy-peer-deps`

### Python 版本

- **导入错误**: 确认已安装所有依赖 `pip install -r requirements.txt`
- **PyQt5 错误**: 重新安装 PyQt5
- **打包失败**: 删除 `build/` 和 `dist/` 目录后重试

更多问题请查看 [INDEX.md](./INDEX.md) 的"常见问题速查"部分。

---

## 📄 许可证

本项目仅供内部使用。

---

## 👥 贡献

如有问题或建议，请联系开发团队。

---

## 🔗 相关链接

- [Tauri 官方文档](https://tauri.app)
- [React 官方文档](https://react.dev)
- [PyQt5 文档](https://www.riverbankcomputing.com/static/Docs/PyQt5/)

---

**最后更新**: 2025 年 10 月 26 日  
**版本**: v2.0  
**状态**: 🟢 可运行

---

**开始使用**: 阅读 [项目结构说明.md](./项目结构说明.md) 📚
