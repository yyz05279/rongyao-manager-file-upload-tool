# 🎉 从这里开始

欢迎使用**熔盐管理文件上传工具**！

## ⚡ 立即开始（3 步搞定）

### 第 1 步：安装依赖

打开终端，执行：

```bash
cd "/Users/yyz/Desktop/熔盐管理文件上传工具"
./install.sh
```

### 第 2 步：运行程序

```bash
python3 main.py
```

### 第 3 步：使用程序

1. 输入服务器地址、用户名、密码
2. 登录后选择项目
3. 添加 Excel 文件
4. 点击上传

**就这么简单！** 🚀

---

## 📚 完整文档

- **新手必读**：[快速开始.md](快速开始.md) - 5 分钟上手
- **详细手册**：[README.md](README.md) - 完整功能说明
- **架构设计**：[ARCHITECTURE.md](ARCHITECTURE.md) - 技术细节
- **项目总结**：[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目概览

---

## 🔧 打包为应用（可选）

### macOS

```bash
./build_macos.sh
```

生成：`dist/熔盐管理文件上传工具.app`

### Windows

```cmd
build_windows.bat
```

生成：`dist\熔盐管理文件上传工具.exe`

---

## ❓ 遇到问题？

### 安装失败？

确保 Python 版本 >= 3.8：

```bash
python3 --version
```

### 无法连接服务器？

检查服务器地址是否正确，例如：

- ✅ `http://localhost:8080`
- ✅ `http://192.168.1.100:8080`
- ❌ `localhost:8080` （缺少 http://）

### Excel 解析失败？

确保 Excel 文件：

- 格式正确（.xlsx 或 .xls）
- 未被其他程序占用
- 包含有效数据

---

## 🎯 技术方案说明

本项目使用 **PyQt6** 作为 GUI 框架，这是经过对比多个方案后的最优选择：

| 方案      | 优势                                                | 选择        |
| --------- | --------------------------------------------------- | ----------- |
| **PyQt6** | ✅ 复用现有 Python 代码<br>✅ 快速开发<br>✅ 跨平台 | ✅ **推荐** |
| Electron  | 需重写代码，体积大                                  | ❌          |
| Tauri     | 需学 Rust，周期长                                   | ❌          |

---

## 📁 项目结构

```
熔盐管理文件上传工具/
├── main.py              # 👈 从这里运行
├── requirements.txt     # 依赖列表
├── ui/                  # 界面模块
│   ├── login_widget.py  # 登录界面
│   └── upload_widget.py # 上传界面
├── services/            # 服务模块
│   ├── auth_service.py  # 认证服务
│   └── upload_service.py # 上传服务
└── 文档/
    ├── README.md           # 完整手册
    ├── 快速开始.md         # 5分钟教程
    └── ARCHITECTURE.md     # 架构设计
```

---

## ✨ 核心特性

✅ **跨平台**：支持 Windows 和 macOS  
✅ **用户友好**：现代化 UI 设计  
✅ **高性能**：异步处理，不阻塞界面  
✅ **安全可靠**：JWT 认证，完善的错误处理  
✅ **生产级别**：遵循 SOLID 原则，代码质量高

---

## 🚀 立即开始

不要犹豫，现在就试试吧：

```bash
# 1. 安装
./install.sh

# 2. 运行
python3 main.py
```

**就是这么简单！** 🎉

---

**祝使用愉快！**

有问题？查看 [README.md](README.md) 获取详细帮助。
