# 系统架构设计文档

## 1. 技术选型

### 1.1 为什么选择 PyQt6？

经过对比三种主流跨平台桌面应用方案，最终选择 PyQt6 作为技术栈：

| 技术方案  | 优势                                                                                                                                      | 劣势                                                                     | 评分       |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ---------- |
| **PyQt6** | ✅ 无缝集成现有 Python 代码<br>✅ 跨平台支持（Windows/Mac/Linux）<br>✅ 打包简单（PyInstaller）<br>✅ 开发效率高<br>✅ 社区活跃，文档完善 | ❌ 打包体积较大（~50MB）<br>❌ 需要 Python 环境                          | ⭐⭐⭐⭐⭐ |
| Electron  | ✅ 界面美观<br>✅ Web 技术栈<br>✅ 生态丰富                                                                                               | ❌ 需要用 JS 重写 Python 代码<br>❌ 体积巨大（~100MB+）<br>❌ 内存占用高 | ⭐⭐⭐     |
| Tauri     | ✅ 体积小（~10MB）<br>✅ 性能优秀<br>✅ 安全性高                                                                                          | ❌ 需要学习 Rust<br>❌ 开发周期长<br>❌ 与 Python 集成复杂               | ⭐⭐       |

**结论**：PyQt6 是本项目的最佳选择，能够最大化复用现有代码，快速交付产品。

## 2. 系统架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                   Presentation Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ MainWindow   │  │ LoginWidget  │  │UploadWidget  │  │
│  │              │  │              │  │              │  │
│  │ • 窗口管理   │  │ • 用户登录   │  │ • 文件管理   │  │
│  │ • 页面切换   │  │ • 表单验证   │  │ • 上传控制   │  │
│  │ • 事件路由   │  │ • 异步登录   │  │ • 进度显示   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          │                  ▼                  ▼
┌─────────┼────────────────────────────────────────────────┐
│         │              Business Layer                     │
│  ┌──────▼─────────────┐          ┌──────────────────┐   │
│  │   AuthService      │          │  UploadService   │   │
│  │                    │          │                  │   │
│  │ • JWT Token管理    │          │ • 文件解析       │   │
│  │ • 登录认证         │◄─────────┤ • 格式转换       │   │
│  │ • Token持久化      │          │ • API调用        │   │
│  └────────────────────┘          │ • 进度管理       │   │
│                                   └─────────┬────────┘   │
└─────────────────────────────────────────────┼────────────┘
                                              │
┌─────────────────────────────────────────────┼────────────┐
│                  Data Processing Layer      │            │
│  ┌───────────────────────────────────────┐  │            │
│  │   DailyReportExcelParser              │◄─┘            │
│  │                                       │               │
│  │ • Excel文件读取                       │               │
│  │ • 工作表遍历                           │               │
│  │ • 数据提取                             │               │
│  │ • 数据验证                             │               │
│  └───────────────┬───────────────────────┘               │
│                  │                                        │
│  ┌───────────────▼───────────────────────┐               │
│  │   convert_to_api_format               │               │
│  │                                       │               │
│  │ • 数据结构转换                         │               │
│  │ • JSON序列化                          │               │
│  │ • API格式封装                         │               │
│  └───────────────────────────────────────┘               │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  Backend API  │
                  │               │
                  │ • 用户认证    │
                  │ • 批量导入    │
                  └───────────────┘
```

### 2.2 模块职责

#### 2.2.1 UI 层（ui/）

- **MainWindow**：主窗口管理器
  - 管理应用程序的整体布局
  - 处理页面切换逻辑
  - 协调各个 Widget 之间的通信
- **LoginWidget**：登录界面
  - 用户输入验证
  - 异步登录处理
  - 登录状态反馈
- **UploadWidget**：上传界面
  - 文件选择和管理
  - 上传进度显示
  - 结果展示

#### 2.2.2 服务层（services/）

- **AuthService**：认证服务
  - JWT Token 获取和管理
  - API 认证头构建
  - 登录状态维护
- **UploadService**：上传服务
  - 文件解析协调
  - 数据转换处理
  - API 调用封装
  - 错误处理

#### 2.2.3 数据处理层

- **parse_daily_report_excel.py**：Excel 解析器
  - 读取 Excel 工作表
  - 提取各类数据（任务、人员、设备等）
  - 数据结构化
- **convert_to_api_format.py**：格式转换器
  - 将解析结果转换为 API 格式
  - JSON 序列化处理

## 3. 核心流程

### 3.1 登录流程

```
用户输入 → 表单验证 → 创建登录线程 → 发送登录请求
                ↓
           服务器验证
                ↓
        ┌───────┴───────┐
        │               │
     成功            失败
        │               │
   保存Token      显示错误
        │
   切换到上传页面
```

**代码实现**（遵循单一职责原则）：

```python
# LoginWidget负责UI交互
def on_login_clicked(self):
    # 1. 验证输入（UI层职责）
    if not self.validate_input():
        return

    # 2. 创建后台线程（避免阻塞UI）
    self.login_thread = LoginThread(...)
    self.login_thread.start()

# LoginThread负责网络请求
class LoginThread(QThread):
    def run(self):
        # 3. 调用服务层（业务逻辑）
        user_info = self.auth_service.login(...)
        self.login_success.emit(user_info)

# AuthService负责认证逻辑
def login(self, username, password, api_base_url):
    # 4. 发送HTTP请求
    response = requests.post(login_url, json=data)
    # 5. 处理响应，保存Token
    self.token = response.json()['data']['token']
```

### 3.2 文件上传流程

```
选择文件 → 添加到列表 → 点击上传
                ↓
        创建上传线程（避免阻塞UI）
                ↓
        ┌───────┴────────┐
        │ 1. 解析Excel   │ (30%)
        └───────┬────────┘
                │
        ┌───────▼────────┐
        │ 2. 转换格式    │ (40%)
        └───────┬────────┘
                │
        ┌───────▼────────┐
        │ 3. 调用API     │ (100%)
        └───────┬────────┘
                │
        ┌───────┴────────┐
        │      │         │
     成功    失败     部分成功
        │      │         │
    显示统计  错误提示  显示详情
```

**代码实现**（SOLID 原则）：

```python
# UploadWidget：单一职责 - UI控制
def start_upload(self):
    # 验证输入
    if not self.validate_upload():
        return
    # 创建上传线程
    self.upload_thread = UploadThread(...)
    self.upload_thread.start()

# UploadThread：单一职责 - 异步执行
class UploadThread(QThread):
    def run(self):
        result = self.upload_service.upload_daily_report_excel(...)
        self.upload_success.emit(result)

# UploadService：单一职责 - 业务编排
def upload_daily_report_excel(self, excel_path, ...):
    # 1. 解析
    all_reports = parser.parse_all_sheets()
    # 2. 转换
    api_data = convert_to_api_format(all_reports, ...)
    # 3. 上传
    result = self._call_batch_import_api(api_data)
    return result
```

## 4. 设计原则应用

### 4.1 SOLID 原则

#### S - 单一职责原则（Single Responsibility）

每个类只做一件事：

- `LoginWidget`：只负责登录 UI
- `AuthService`：只负责认证逻辑
- `DailyReportExcelParser`：只负责解析 Excel

#### O - 开闭原则（Open/Closed）

对扩展开放，对修改关闭：

```python
# 良好的扩展点
class UploadService:
    def upload_daily_report_excel(self, progress_callback=None):
        # 通过回调函数扩展进度通知功能
        if progress_callback:
            progress_callback(50)
```

#### L - 里氏替换原则（Liskov Substitution）

子类可以替换父类：

```python
# 所有Widget都继承自QWidget
class LoginWidget(QWidget):  # 可以在任何需要QWidget的地方使用
    pass
```

#### I - 接口隔离原则（Interface Segregation）

接口应该小而专：

```python
# 不同的信号用于不同的目的
class LoginWidget(QWidget):
    login_success = pyqtSignal(dict)  # 登录成功

class UploadWidget(QWidget):
    logout_requested = pyqtSignal()   # 退出登录
```

#### D - 依赖倒置原则（Dependency Inversion）

依赖抽象而非具体实现：

```python
# 通过构造函数注入依赖
class UploadService:
    def __init__(self):
        self.auth_service = AuthService()  # 依赖服务而非直接实现
```

### 4.2 KISS 原则（Keep It Simple, Stupid）

保持代码简单：

```python
# ❌ 复杂的实现
def validate_input(self):
    return (
        self.server_input.text().strip() != "" and
        self.username_input.text().strip() != "" and
        self.password_input.text().strip() != ""
    )

# ✅ 简单的实现
def validate_input(self):
    if not self.server_input.text().strip():
        return False
    if not self.username_input.text().strip():
        return False
    if not self.password_input.text().strip():
        return False
    return True
```

### 4.3 DRY 原则（Don't Repeat Yourself）

避免重复代码：

```python
# 提取公共样式方法
def get_button_style(self, color: str):
    return f"""
        QPushButton {{
            background-color: {color};
            ...
        }}
    """

# 复用样式
self.login_button.setStyleSheet(self.get_button_style("#4CAF50"))
self.cancel_button.setStyleSheet(self.get_button_style("#f44336"))
```

## 5. 异常处理策略

### 5.1 分层异常处理

```python
# 数据层：详细异常
try:
    workbook = openpyxl.load_workbook(excel_path)
except FileNotFoundError:
    raise Exception(f'文件不存在：{excel_path}')
except openpyxl.InvalidFileException:
    raise Exception('不是有效的Excel文件')

# 服务层：业务异常
try:
    all_reports = parser.parse_all_sheets()
except Exception as e:
    raise Exception(f'Excel解析失败：{str(e)}')

# UI层：用户友好提示
try:
    result = upload_service.upload(...)
except Exception as e:
    QMessageBox.critical(self, "上传失败", str(e))
```

### 5.2 网络异常处理

```python
try:
    response = requests.post(url, ...)
except requests.exceptions.Timeout:
    raise Exception('连接超时，请检查网络')
except requests.exceptions.ConnectionError:
    raise Exception('无法连接到服务器')
except requests.exceptions.RequestException as e:
    raise Exception(f'网络请求失败：{str(e)}')
```

## 6. 性能优化

### 6.1 异步处理

所有耗时操作都在后台线程执行：

- 登录请求 → `LoginThread`
- 文件上传 → `UploadThread`

### 6.2 进度反馈

```python
def upload_daily_report_excel(self, progress_callback=None):
    if progress_callback:
        progress_callback(10)   # 开始解析
    # ... 解析
    if progress_callback:
        progress_callback(40)   # 解析完成
    # ... 转换
    if progress_callback:
        progress_callback(100)  # 全部完成
```

## 7. 安全考虑

### 7.1 密码安全

- 密码输入框使用`EchoMode.Password`模式
- 密码不记录日志
- 密码通过 HTTPS 传输（需服务端支持）

### 7.2 Token 管理

- Token 存储在内存中
- 退出登录清除 Token
- Token 包含在请求头中（Bearer 方式）

### 7.3 输入验证

```python
# 所有用户输入都进行验证
def validate_input(self):
    if not server:
        QMessageBox.warning(self, "输入错误", "请输入服务器地址")
        return False
    # ...
```

## 8. 可维护性

### 8.1 代码组织

```
项目根目录/
├── ui/              # UI层（界面相关）
├── services/        # 服务层（业务逻辑）
├── *.py            # 数据处理层（工具脚本）
└── api/            # API文档
```

### 8.2 命名规范

- 类名：大驼峰（`MainWindow`）
- 方法名：小驼峰（`onLoginClicked`）或下划线（`on_login_clicked`）
- 常量：全大写（`API_BASE_URL`）
- 私有方法：下划线前缀（`_extract_error_message`）

### 8.3 注释规范

```python
def login(self, username: str, password: str, api_base_url: str) -> Dict:
    """
    用户登录

    :param username: 用户名
    :param password: 密码
    :param api_base_url: API基础URL
    :return: 用户信息字典
    :raises Exception: 登录失败时抛出异常
    """
```

## 9. 扩展性设计

### 9.1 支持多种文件类型

当前只支持 Excel，可扩展：

```python
class FileParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> List[Dict]:
        pass

class ExcelParser(FileParser):
    def parse(self, file_path: str):
        # Excel解析逻辑
        pass

class CSVParser(FileParser):
    def parse(self, file_path: str):
        # CSV解析逻辑
        pass
```

### 9.2 支持多种上传方式

当前是批量导入，可扩展：

```python
class UploadStrategy(ABC):
    @abstractmethod
    def upload(self, data: Dict) -> Dict:
        pass

class BatchImportStrategy(UploadStrategy):
    def upload(self, data: Dict):
        # 批量导入
        pass

class SingleUploadStrategy(UploadStrategy):
    def upload(self, data: Dict):
        # 单个上传
        pass
```

## 10. 总结

本项目采用了现代软件工程的最佳实践：

✅ **清晰的分层架构**：UI、业务、数据三层分离  
✅ **SOLID 设计原则**：每个类职责单一、易于扩展  
✅ **异步处理机制**：避免 UI 阻塞，提升用户体验  
✅ **完善的异常处理**：从底层到 UI 层的分层处理  
✅ **良好的可维护性**：代码组织清晰、命名规范、注释完整  
✅ **优秀的可扩展性**：预留扩展点，支持未来功能增强

这是一个**生产级别**的桌面应用程序实现。
