# 熔盐管理文件上传工具

一个基于 PyQt6 的跨平台桌面应用程序，用于上传项目日报 Excel 文件到熔盐管理系统。

## 功能特性

✅ **跨平台支持**：支持 Windows 和 macOS 系统  
✅ **用户认证**：账号密码登录，支持 JWT Token  
✅ **文件上传**：批量上传日报 Excel 文件  
✅ **数据解析**：自动解析 Excel 并转换为 API 格式  
✅ **进度显示**：实时显示上传进度  
✅ **美观界面**：现代化 UI 设计，用户体验友好

## 技术栈

- **GUI 框架**：PyQt6
- **HTTP 客户端**：requests
- **Excel 处理**：openpyxl
- **打包工具**：PyInstaller

## 安装依赖

### 方式一：使用 pip（推荐）

```bash
pip install -r requirements.txt
```

### 方式二：手动安装

```bash
pip install PyQt6>=6.6.0
pip install requests>=2.31.0
pip install openpyxl>=3.1.0
pip install PyInstaller>=6.0.0
```

## 运行应用

### 开发模式

```bash
python main.py
```

### 打包为可执行文件

#### Windows 系统

```bash
# 打包为单个exe文件
pyinstaller --onefile --windowed --name="熔盐管理文件上传工具" main.py

# 打包完成后，可执行文件位于 dist 目录
```

#### macOS 系统

```bash
# 使用打包脚本（已优化，解决闪退问题）
chmod +x build_macos.sh
./build_macos.sh

# 如果需要调试，使用调试版
chmod +x build_macos_debug.sh
./build_macos_debug.sh
```

**⚠️ 如果打包后应用闪退，请查看：**

- [QUICK_FIX.md](QUICK_FIX.md) - 快速修复指南
- [DEBUG.md](DEBUG.md) - 详细调试步骤

## 使用说明

### 1. 登录

- 输入服务器地址（如：`http://42.192.76.234:8081
`）
- 输入用户名和密码
- 点击"登录"按钮

### 2. 添加文件

- 登录成功后，选择项目
- 点击"添加文件"按钮
- 选择要上传的 Excel 文件（支持.xlsx 和.xls 格式）
- 可以一次添加多个文件

### 3. 开始上传

- 点击"开始上传"按钮
- 等待上传完成
- 查看上传结果统计

### 4. 退出登录

- 点击右上角"退出登录"按钮
- 返回登录界面

## 项目结构

```
熔盐管理文件上传工具/
├── main.py                          # 程序入口
├── requirements.txt                 # 依赖列表
├── README.md                        # 说明文档
├── ui/                              # UI界面模块
│   ├── __init__.py
│   ├── main_window.py              # 主窗口
│   ├── login_widget.py             # 登录界面
│   └── upload_widget.py            # 上传界面
├── services/                        # 服务模块
│   ├── __init__.py
│   ├── auth_service.py             # 认证服务
│   └── upload_service.py           # 上传服务
├── parse_daily_report_excel.py     # Excel解析工具
├── convert_to_api_format.py        # 格式转换工具
└── api/                             # API文档
    └── 19-项目日报批量导入API.md
```

## API 接口

本工具调用以下 API 接口：

### 1. 用户登录

- **路径**：`/api/v1/auth/login`
- **方法**：POST
- **说明**：用户认证，获取 JWT Token

### 2. 批量导入日报

- **路径**：`/api/v1/daily-reports/batch-import`
- **方法**：POST
- **认证**：需要 JWT Token
- **说明**：批量导入解析后的日报数据

详细 API 文档请查看：[api/19-项目日报批量导入 API.md](api/19-项目日报批量导入API.md)

## 配置说明

### 服务器地址配置

默认服务器地址为：`http://42.192.76.234:8081
`

可以在登录界面修改为实际的服务器地址。

### 项目配置

项目列表目前是硬编码的，位于 `ui/upload_widget.py` 的 `set_user_info` 方法中。

如需从 API 动态获取项目列表，请修改此处代码。

## 常见问题

### Q1: 安装 PyQt6 时出错？

**A**: 确保使用 Python 3.8 或更高版本：

```bash
python --version  # 检查Python版本
pip install --upgrade pip  # 更新pip
pip install PyQt6
```

### Q2: 运行时报"无法连接到服务器"？

**A**: 请检查：

- 服务器地址是否正确
- 服务器是否正在运行
- 网络连接是否正常
- 防火墙是否阻止了连接

### Q3: 上传时显示"登录已过期"？

**A**: Token 可能已过期，请重新登录。

### Q4: Excel 文件解析失败？

**A**: 请确保：

- Excel 文件格式正确
- 文件未损坏
- 文件未被其他程序占用
- Excel 文件符合预期的模板格式

### Q5: 打包后的程序体积很大？

**A**: PyInstaller 会打包所有依赖，这是正常的。如需减小体积：

- 使用虚拟环境，只安装必要的包
- 使用 `--exclude-module` 参数排除不需要的模块

### Q6: macOS 上提示"无法打开应用"？

**A**: 需要允许来自未知开发者的应用：

```bash
# 方式一：系统设置
# 系统偏好设置 -> 安全性与隐私 -> 通用 -> 允许从以下位置下载的App

# 方式二：命令行
xattr -cr "dist/熔盐管理文件上传工具.app"
```

### Q7: 打包后应用一闪就退出？

**A**: 这是 PyQt6 打包的常见问题，请使用修复版：

```bash
# 1. 使用打包脚本
./build_macos.sh

# 2. 如果还是失败，运行调试版查看错误
./build_macos_debug.sh
./dist/熔盐管理文件上传工具/熔盐管理文件上传工具
```

详见：[QUICK_FIX.md](QUICK_FIX.md)

## 开发指南

### 添加新功能

1. 在 `ui/` 目录添加新的界面组件
2. 在 `services/` 目录添加新的业务逻辑
3. 更新 `main_window.py` 集成新功能

### 修改样式

所有样式都使用内联 CSS 定义，可以在各个 Widget 的`setup_ui`方法中修改。

### 调试技巧

```python
# 开启调试模式，显示详细错误信息
import traceback
try:
    # 你的代码
    pass
except Exception as e:
    traceback.print_exc()
```

## 系统要求

### Windows

- Windows 10 或更高版本
- Python 3.8+

### macOS

- macOS 10.14 (Mojave) 或更高版本
- Python 3.8+

## 更新日志

### v1.0.0 (2025-10-23)

- ✨ 初始版本发布
- ✅ 用户登录功能
- ✅ Excel 文件上传功能
- ✅ 批量导入日报数据
- ✅ 跨平台支持（Windows/macOS）

## 许可证

本项目仅供内部使用。

## 联系方式

如有问题或建议，请联系开发团队。

---

**开发者**：YourCompany  
**最后更新**：2025-10-23
