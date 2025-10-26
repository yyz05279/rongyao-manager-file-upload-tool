# Python 版本 - 项目结构详解

> 基于 PyQt5 的传统桌面应用

---

## 📁 完整目录树

```
熔盐管理文件上传工具/
│
├── 📄 main.py                         # 应用程序入口
├── 📄 requirements.txt                # Python依赖配置
├── 📄 熔盐管理文件上传工具.spec        # PyInstaller打包配置
│
├── 📂 ui/                             # 用户界面层（PyQt5）
│   ├── 📄 __init__.py                 # 包初始化
│   ├── 📄 main_window.py              # 主窗口
│   ├── 📄 login_widget.py             # 登录界面组件
│   ├── 📄 upload_widget.py            # 上传界面组件
│   ├── 📄 daily_report_detail_dialog.py  # 日报详情对话框
│   └── 📂 image/                      # 界面图片资源
│       └── 📂 daily_report_detail_dialog/
│
├── 📂 services/                       # 服务层（业务逻辑）
│   ├── 📄 __init__.py                 # 包初始化
│   ├── 📄 app_state.py                # 全局应用状态
│   ├── 📄 base_service.py             # 基础服务类
│   ├── 📄 auth_service.py             # 认证服务
│   ├── 📄 config_service.py           # 配置服务
│   ├── 📄 project_service.py          # 项目服务
│   └── 📄 upload_service.py           # 上传服务
│
├── 📄 parse_daily_report_excel.py     # Excel解析工具
├── 📄 convert_to_api_format.py        # 数据格式转换工具
│
├── 📂 build/                          # 构建临时文件（自动生成，忽略）
│   └── 📂 熔盐管理文件上传工具/
│       ├── Analysis-00.toc
│       ├── base_library.zip
│       ├── BUNDLE-00.toc
│       ├── EXE-00.toc
│       ├── PKG-00.toc
│       ├── PYZ-00.pyz
│       └── ...
│
└── 📂 dist/                           # 打包输出目录（自动生成）
    ├── 熔盐管理文件上传工具             # macOS可执行文件
    └── 📂 熔盐管理文件上传工具.app/    # macOS应用包
        └── Contents/
            ├── Info.plist
            ├── MacOS/
            └── Resources/
```

---

## 🔧 核心文件说明

### 应用入口

#### `main.py`

应用程序主入口文件

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    """应用程序入口"""
    app = QApplication(sys.argv)
    app.setApplicationName("熔盐管理文件上传工具")

    # 创建主窗口
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```

功能：

- 初始化 Qt 应用
- 创建并显示主窗口
- 启动事件循环

---

### 界面层（ui/）

#### `ui/main_window.py`

主窗口类

```python
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from ui.login_widget import LoginWidget
from ui.upload_widget import UploadWidget

class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("熔盐管理文件上传工具")
        self.setFixedSize(1000, 700)

        # 创建堆叠窗口部件
        self.stack = QStackedWidget()

        # 创建登录和上传界面
        self.login_widget = LoginWidget()
        self.upload_widget = UploadWidget()

        # 添加到堆叠窗口
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.upload_widget)

        # 设置为中心部件
        self.setCentralWidget(self.stack)

        # 连接信号
        self.login_widget.login_success.connect(self.on_login_success)
        self.upload_widget.logout_requested.connect(self.on_logout)

    def on_login_success(self):
        """登录成功处理"""
        self.stack.setCurrentWidget(self.upload_widget)
        self.upload_widget.load_projects()

    def on_logout(self):
        """退出登录处理"""
        self.stack.setCurrentWidget(self.login_widget)
```

功能：

- 管理登录和上传两个界面的切换
- 处理登录成功和退出事件
- 设置窗口标题和大小

#### `ui/login_widget.py`

登录界面组件

```python
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QMessageBox
)
from services.auth_service import AuthService
from services.config_service import ConfigService

class LoginWidget(QWidget):
    """登录界面"""

    # 定义信号
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()
        self.config_service = ConfigService()
        self.init_ui()
        self.load_saved_credentials()

    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout()

        # 标题
        title = QLabel("熔盐管理系统")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        # 用户名输入
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")

        # 密码输入
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.Password)

        # 记住密码复选框
        self.remember_checkbox = QCheckBox("记住密码")

        # 登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.on_login)

        # 添加到布局
        layout.addWidget(title)
        layout.addWidget(QLabel("用户名:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("密码:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.remember_checkbox)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def on_login(self):
        """登录处理"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "错误", "请输入用户名和密码")
            return

        try:
            # 调用登录服务
            result = self.auth_service.login(username, password)

            if result['success']:
                # 保存凭据（如果勾选记住密码）
                if self.remember_checkbox.isChecked():
                    self.config_service.save_credentials(username, password)
                else:
                    self.config_service.clear_credentials()

                # 发送登录成功信号
                self.login_success.emit()
            else:
                QMessageBox.warning(self, "登录失败", result.get('message', '未知错误'))

        except Exception as e:
            QMessageBox.critical(self, "错误", f"登录异常: {str(e)}")

    def load_saved_credentials(self):
        """加载保存的凭据"""
        credentials = self.config_service.load_credentials()
        if credentials:
            self.username_input.setText(credentials['username'])
            self.password_input.setText(credentials['password'])
            self.remember_checkbox.setChecked(True)
```

功能：

- 用户名和密码输入
- 记住密码功能
- 登录验证
- 凭据保存和加载

#### `ui/upload_widget.py`

上传界面组件

```python
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QTableWidget, QProgressBar, QLabel,
    QFileDialog, QMessageBox, QCheckBox
)
from services.project_service import ProjectService
from services.upload_service import UploadService
from parse_daily_report_excel import parse_daily_report_excel

class UploadWidget(QWidget):
    """上传界面"""

    # 定义信号
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.project_service = ProjectService()
        self.upload_service = UploadService()
        self.parsed_data = []
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout()

        # 顶部工具栏
        toolbar = QHBoxLayout()

        # 项目选择
        self.project_combo = QComboBox()
        toolbar.addWidget(QLabel("选择项目:"))
        toolbar.addWidget(self.project_combo)

        # 选择文件按钮
        self.file_button = QPushButton("选择文件")
        self.file_button.clicked.connect(self.on_select_file)
        toolbar.addWidget(self.file_button)

        # 上传按钮
        self.upload_button = QPushButton("批量上传")
        self.upload_button.clicked.connect(self.on_upload)
        self.upload_button.setEnabled(False)
        toolbar.addWidget(self.upload_button)

        # 退出按钮
        logout_button = QPushButton("退出登录")
        logout_button.clicked.connect(self.logout_requested.emit)
        toolbar.addWidget(logout_button)

        layout.addLayout(toolbar)

        # 数据预览表格
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "选择", "序号", "施工区域", "日期", "任务内容",
            "工作内容", "人数", "工时"
        ])
        layout.addWidget(self.table)

        # 底部状态栏
        status_layout = QHBoxLayout()

        # 覆盖旧记录选项
        self.overwrite_checkbox = QCheckBox("覆盖旧记录")
        status_layout.addWidget(self.overwrite_checkbox)

        # 进度条
        self.progress_bar = QProgressBar()
        status_layout.addWidget(self.progress_bar)

        # 状态标签
        self.status_label = QLabel("就绪")
        status_layout.addWidget(self.status_label)

        layout.addLayout(status_layout)

        self.setLayout(layout)

    def load_projects(self):
        """加载项目列表"""
        try:
            projects = self.project_service.get_projects()
            self.project_combo.clear()
            for project in projects:
                self.project_combo.addItem(project['name'], project['id'])
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载项目失败: {str(e)}")

    def on_select_file(self):
        """选择文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择Excel文件",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if file_path:
            try:
                # 解析Excel文件
                self.parsed_data = parse_daily_report_excel(file_path)
                self.display_data(self.parsed_data)
                self.upload_button.setEnabled(True)
                self.status_label.setText(f"已加载 {len(self.parsed_data)} 条记录")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"解析文件失败: {str(e)}")

    def display_data(self, data):
        """显示数据"""
        self.table.setRowCount(len(data))

        for row, item in enumerate(data):
            # 勾选框
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            self.table.setCellWidget(row, 0, checkbox)

            # 其他列
            self.table.setItem(row, 1, QTableWidgetItem(str(item.get('序号', ''))))
            self.table.setItem(row, 2, QTableWidgetItem(item.get('施工区域', '')))
            # ... 其他列

    def on_upload(self):
        """上传数据"""
        # 获取选中的项目
        project_id = self.project_combo.currentData()
        if not project_id:
            QMessageBox.warning(self, "警告", "请选择项目")
            return

        # 获取勾选的数据
        selected_data = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox.isChecked():
                selected_data.append(self.parsed_data[row])

        if not selected_data:
            QMessageBox.warning(self, "警告", "请至少选择一条数据")
            return

        # 创建上传线程
        self.upload_thread = UploadThread(
            self.upload_service,
            project_id,
            selected_data,
            self.overwrite_checkbox.isChecked()
        )

        self.upload_thread.progress_updated.connect(self.on_progress_updated)
        self.upload_thread.upload_finished.connect(self.on_upload_finished)

        # 禁用按钮
        self.upload_button.setEnabled(False)
        self.file_button.setEnabled(False)

        # 开始上传
        self.upload_thread.start()

    def on_progress_updated(self, current, total):
        """更新进度"""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.status_label.setText(f"正在上传 {current}/{total}")

    def on_upload_finished(self, success, message):
        """上传完成"""
        self.upload_button.setEnabled(True)
        self.file_button.setEnabled(True)

        if success:
            QMessageBox.information(self, "成功", message)
            self.status_label.setText("上传完成")
        else:
            QMessageBox.critical(self, "失败", message)
            self.status_label.setText("上传失败")


class UploadThread(QThread):
    """上传线程"""

    progress_updated = pyqtSignal(int, int)
    upload_finished = pyqtSignal(bool, str)

    def __init__(self, service, project_id, data, overwrite):
        super().__init__()
        self.service = service
        self.project_id = project_id
        self.data = data
        self.overwrite = overwrite

    def run(self):
        """执行上传"""
        try:
            for i, item in enumerate(self.data):
                self.service.upload_report(self.project_id, item, self.overwrite)
                self.progress_updated.emit(i + 1, len(self.data))

            self.upload_finished.emit(True, f"成功上传 {len(self.data)} 条记录")
        except Exception as e:
            self.upload_finished.emit(False, str(e))
```

功能：

- 项目选择
- 文件选择和解析
- 数据预览表格
- 批量上传
- 进度显示
- 覆盖选项

#### `ui/daily_report_detail_dialog.py`

日报详情对话框

```python
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit,
    QPushButton, QFormLayout
)

class DailyReportDetailDialog(QDialog):
    """日报详情对话框"""

    def __init__(self, report_data, parent=None):
        super().__init__(parent)
        self.report_data = report_data
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("日报详情")
        self.setFixedSize(600, 500)

        layout = QVBoxLayout()

        # 表单布局
        form = QFormLayout()

        # 添加字段
        form.addRow("序号:", QLabel(str(self.report_data.get('序号', ''))))
        form.addRow("施工区域:", QLabel(self.report_data.get('施工区域', '')))
        form.addRow("日期:", QLabel(self.report_data.get('日期', '')))
        form.addRow("任务内容:", QLabel(self.report_data.get('任务内容', '')))

        # 工作内容（多行）
        work_content = QTextEdit()
        work_content.setPlainText(self.report_data.get('工作内容', ''))
        work_content.setReadOnly(True)
        form.addRow("工作内容:", work_content)

        form.addRow("人数:", QLabel(str(self.report_data.get('人数', ''))))
        form.addRow("工时:", QLabel(str(self.report_data.get('工时', ''))))

        layout.addLayout(form)

        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)
```

功能：

- 显示单条日报的详细信息
- 字段格式化展示
- 多行文本支持

---

### 服务层（services/）

#### `services/app_state.py`

全局应用状态管理

```python
class AppState:
    """应用全局状态"""

    _instance = None

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """初始化"""
        if self._initialized:
            return

        self._initialized = True
        self._token = None
        self._refresh_token = None
        self._user_info = None
        self._current_project = None

    @property
    def token(self):
        """访问令牌"""
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property
    def refresh_token(self):
        """刷新令牌"""
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, value):
        self._refresh_token = value

    @property
    def user_info(self):
        """用户信息"""
        return self._user_info

    @user_info.setter
    def user_info(self, value):
        self._user_info = value

    @property
    def current_project(self):
        """当前项目"""
        return self._current_project

    @current_project.setter
    def current_project(self, value):
        self._current_project = value

    def clear(self):
        """清空状态"""
        self._token = None
        self._refresh_token = None
        self._user_info = None
        self._current_project = None
```

功能：

- 单例模式实现
- 存储 Token、用户信息、当前项目
- 提供属性访问器

#### `services/base_service.py`

基础服务类

```python
import requests
from services.app_state import AppState

class BaseService:
    """基础服务类"""

    BASE_URL = "https://api.example.com"

    def __init__(self):
        """初始化"""
        self.app_state = AppState()
        self.session = requests.Session()

    def _get_headers(self, need_token=True):
        """获取请求头"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        if need_token and self.app_state.token:
            headers['Authorization'] = f'Bearer {self.app_state.token}'

        return headers

    def _request(self, method, endpoint, **kwargs):
        """发送请求"""
        url = f"{self.BASE_URL}{endpoint}"

        # 添加请求头
        if 'headers' not in kwargs:
            kwargs['headers'] = self._get_headers()

        # 发送请求
        response = self.session.request(method, url, **kwargs)

        # 检查状态码
        if response.status_code == 401:
            # Token过期，尝试刷新
            if self._refresh_token():
                # 重试请求
                kwargs['headers'] = self._get_headers()
                response = self.session.request(method, url, **kwargs)
            else:
                raise Exception("认证失败，请重新登录")

        # 解析响应
        response.raise_for_status()
        return response.json()

    def _refresh_token(self):
        """刷新Token"""
        try:
            from services.auth_service import AuthService
            auth_service = AuthService()
            return auth_service.refresh_token()
        except:
            return False

    def get(self, endpoint, **kwargs):
        """GET请求"""
        return self._request('GET', endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        """POST请求"""
        return self._request('POST', endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        """PUT请求"""
        return self._request('PUT', endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        """DELETE请求"""
        return self._request('DELETE', endpoint, **kwargs)
```

功能：

- HTTP 请求封装
- Token 自动添加
- Token 过期自动刷新
- 错误处理

#### `services/auth_service.py`

认证服务

```python
from services.base_service import BaseService
from services.app_state import AppState

class AuthService(BaseService):
    """认证服务"""

    def login(self, username, password):
        """用户登录"""
        try:
            # 发送登录请求
            response = self.post('/auth/login', json={
                'username': username,
                'password': password
            }, headers={'Content-Type': 'application/json'})

            # 保存Token和用户信息
            if response.get('success'):
                data = response.get('data', {})
                self.app_state.token = data.get('access_token')
                self.app_state.refresh_token = data.get('refresh_token')
                self.app_state.user_info = data.get('user_info')

            return response

        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    def refresh_token(self):
        """刷新Token"""
        try:
            if not self.app_state.refresh_token:
                return False

            response = self.post('/auth/refresh', json={
                'refresh_token': self.app_state.refresh_token
            })

            if response.get('success'):
                data = response.get('data', {})
                self.app_state.token = data.get('access_token')
                return True
            else:
                return False

        except:
            return False

    def logout(self):
        """退出登录"""
        self.app_state.clear()
```

功能：

- 用户登录
- Token 刷新
- 退出登录

#### `services/config_service.py`

配置服务

```python
import json
import os
from pathlib import Path

class ConfigService:
    """配置服务"""

    def __init__(self):
        """初始化"""
        self.config_dir = Path.home() / '.molten_salt_manager'
        self.config_file = self.config_dir / 'config.json'
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        """确保配置目录存在"""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def save_credentials(self, username, password):
        """保存凭据"""
        config = self._load_config()
        config['credentials'] = {
            'username': username,
            'password': password  # 注意：实际应用中应该加密
        }
        self._save_config(config)

    def load_credentials(self):
        """加载凭据"""
        config = self._load_config()
        return config.get('credentials')

    def clear_credentials(self):
        """清除凭据"""
        config = self._load_config()
        if 'credentials' in config:
            del config['credentials']
        self._save_config(config)

    def _load_config(self):
        """加载配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_config(self, config):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
```

功能：

- 保存和加载用户凭据
- 配置文件管理
- 目录自动创建

#### `services/project_service.py`

项目服务

```python
from services.base_service import BaseService

class ProjectService(BaseService):
    """项目服务"""

    def get_projects(self):
        """获取项目列表"""
        response = self.get('/projects')
        if response.get('success'):
            return response.get('data', [])
        else:
            raise Exception(response.get('message', '获取项目列表失败'))

    def get_project_info(self, project_id):
        """获取项目信息"""
        response = self.get(f'/projects/{project_id}')
        if response.get('success'):
            return response.get('data')
        else:
            raise Exception(response.get('message', '获取项目信息失败'))
```

功能：

- 获取项目列表
- 获取项目详细信息

#### `services/upload_service.py`

上传服务

```python
from services.base_service import BaseService

class UploadService(BaseService):
    """上传服务"""

    def upload_report(self, project_id, report_data, overwrite=False):
        """上传单条日报"""
        response = self.post(f'/projects/{project_id}/reports', json={
            'data': report_data,
            'overwrite': overwrite
        })

        if not response.get('success'):
            raise Exception(response.get('message', '上传失败'))

        return response

    def batch_upload(self, project_id, reports, overwrite=False):
        """批量上传日报"""
        response = self.post(f'/projects/{project_id}/reports/batch', json={
            'data': reports,
            'overwrite': overwrite
        })

        if not response.get('success'):
            raise Exception(response.get('message', '批量上传失败'))

        return response
```

功能：

- 单条日报上传
- 批量日报上传
- 覆盖选项支持

---

### 工具文件

#### `parse_daily_report_excel.py`

Excel 解析工具

```python
import pandas as pd
from datetime import datetime

def parse_daily_report_excel(file_path):
    """解析日报Excel文件"""

    # 读取Excel文件
    df = pd.read_excel(file_path, sheet_name=0)

    # 数据列表
    reports = []

    # 遍历行
    for index, row in df.iterrows():
        # 跳过空行
        if pd.isna(row.get('序号')):
            continue

        # 构建日报数据
        report = {
            '序号': str(row.get('序号', '')),
            '施工区域': str(row.get('施工区域', '')),
            '日期': format_date(row.get('日期')),
            '任务内容': str(row.get('任务内容', '')),
            '工作内容': str(row.get('工作内容', '')),
            '人数': int(row.get('人数', 0)),
            '工时': float(row.get('工时', 0.0))
        }

        reports.append(report)

    return reports


def format_date(date_value):
    """格式化日期"""
    if pd.isna(date_value):
        return ''

    if isinstance(date_value, datetime):
        return date_value.strftime('%Y-%m-%d')
    elif isinstance(date_value, str):
        return date_value
    else:
        return str(date_value)
```

功能：

- 解析 Excel 文件
- 数据验证和清理
- 日期格式化

#### `convert_to_api_format.py`

数据格式转换工具

```python
def convert_to_api_format(report_data):
    """将Excel数据转换为API格式"""

    return {
        'serial_number': report_data.get('序号'),
        'construction_area': report_data.get('施工区域'),
        'date': report_data.get('日期'),
        'task_content': report_data.get('任务内容'),
        'work_content': report_data.get('工作内容'),
        'people_count': report_data.get('人数'),
        'work_hours': report_data.get('工时')
    }
```

功能：

- 字段名称转换
- 数据格式适配

---

## 🚀 运行和打包

### 开发模式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py

# 或使用脚本
./run_macos.sh
```

### 打包应用

#### macOS 打包

```bash
# 使用打包脚本
./build_macos.sh

# 或手动打包
pyinstaller --onefile --windowed \
    --name "熔盐管理文件上传工具" \
    --add-data "ui:ui" \
    --add-data "services:services" \
    main.py
```

#### Windows 打包

```batch
# 使用打包脚本
build_windows.bat

# 或手动打包
pyinstaller --onefile --windowed ^
    --name "熔盐管理文件上传工具" ^
    --add-data "ui;ui" ^
    --add-data "services;services" ^
    main.py
```

### 打包配置（.spec 文件）

```python
# 熔盐管理文件上传工具.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ui', 'ui'),
        ('services', 'services'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'requests',
        'pandas',
        'openpyxl',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='熔盐管理文件上传工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='熔盐管理文件上传工具.app',
    icon=None,
    bundle_identifier='com.example.molten-salt-manager',
)
```

---

## 📦 依赖说明（requirements.txt）

```txt
# PyQt5 - GUI框架
PyQt5==5.15.9

# 网络请求
requests==2.31.0

# Excel处理
pandas==2.0.3
openpyxl==3.1.2

# 打包工具
PyInstaller==6.3.0

# 其他工具
python-dateutil==2.8.2
```

---

## 🐛 调试技巧

### 添加调试日志

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)

logger = logging.getLogger(__name__)
logger.debug('调试信息')
logger.info('普通信息')
logger.warning('警告信息')
logger.error('错误信息')
```

### 捕获异常

```python
import traceback

try:
    # 可能出错的代码
    pass
except Exception as e:
    # 打印完整堆栈信息
    traceback.print_exc()
    # 或记录到日志
    logger.error(f"异常: {str(e)}", exc_info=True)
```

---

## 📝 开发建议

1. **界面开发**: 使用 Qt Designer 设计界面，然后转换为 Python 代码
2. **服务层**: 遵循单一职责原则，每个服务类只负责一个业务模块
3. **错误处理**: 所有网络请求都应该有 try-except 包裹
4. **用户体验**: 长时间操作使用线程，避免界面卡死
5. **配置管理**: 敏感信息（如密码）应该加密存储

---

**文档版本**: 1.0.0
**最后更新**: 2025 年 10 月 26 日
