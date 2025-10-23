#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
登录界面
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont

from services.auth_service import AuthService


class LoginThread(QThread):
    """登录线程"""
    
    login_success = pyqtSignal(dict)  # 登录成功信号，传递用户信息
    login_failed = pyqtSignal(str)     # 登录失败信号，传递错误信息
    
    def __init__(self, username: str, password: str, api_base_url: str):
        super().__init__()
        self.username = username
        self.password = password
        self.api_base_url = api_base_url
        self.auth_service = AuthService()
    
    def run(self):
        """执行登录"""
        try:
            user_info = self.auth_service.login(
                self.username,
                self.password,
                self.api_base_url
            )
            self.login_success.emit(user_info)
        except Exception as e:
            self.login_failed.emit(str(e))


class LoginWidget(QWidget):
    """登录界面类"""
    
    login_success = pyqtSignal(dict)  # 登录成功信号
    
    def __init__(self):
        super().__init__()
        self.login_thread = None
        self.setup_ui()
    
    def setup_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 添加垂直间距
        layout.addStretch()
        
        # 创建登录表单容器
        form_container = QFrame()
        form_container.setMaximumWidth(400)
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        
        # 标题
        title_label = QLabel("熔盐管理系统")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(title_label)
        
        # 副标题
        subtitle_label = QLabel("文件上传工具")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #666;")
        form_layout.addWidget(subtitle_label)
        
        form_layout.addSpacing(30)
        
        # 服务器地址
        server_label = QLabel("服务器地址:")
        form_layout.addWidget(server_label)
        
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("http://42.192.76.234:8081")
        self.server_input.setText("http://42.192.76.234:8081")
        self.server_input.setMinimumHeight(40)
        self.server_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        form_layout.addWidget(self.server_input)
        
        # 用户名
        username_label = QLabel("用户名:")
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")
        self.username_input.setMinimumHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        form_layout.addWidget(self.username_input)
        
        # 密码
        password_label = QLabel("密码:")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        form_layout.addWidget(self.password_input)
        
        # 回车键登录
        self.password_input.returnPressed.connect(self.on_login_clicked)
        
        form_layout.addSpacing(20)
        
        # 登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.setMinimumHeight(45)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.login_button.clicked.connect(self.on_login_clicked)
        form_layout.addWidget(self.login_button)
        
        # 将表单容器添加到主布局
        layout.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 添加垂直间距
        layout.addStretch()
        
        # 设置整体背景
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
        """)
    
    def on_login_clicked(self):
        """登录按钮点击处理"""
        server = self.server_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # 验证输入
        if not server:
            QMessageBox.warning(self, "输入错误", "请输入服务器地址")
            self.server_input.setFocus()
            return
        
        if not username:
            QMessageBox.warning(self, "输入错误", "请输入用户名")
            self.username_input.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "输入错误", "请输入密码")
            self.password_input.setFocus()
            return
        
        # 禁用登录按钮
        self.login_button.setEnabled(False)
        self.login_button.setText("登录中...")
        
        # 创建并启动登录线程
        self.login_thread = LoginThread(username, password, server)
        self.login_thread.login_success.connect(self.on_login_success)
        self.login_thread.login_failed.connect(self.on_login_failed)
        self.login_thread.finished.connect(self.on_login_finished)
        self.login_thread.start()
    
    def on_login_success(self, user_info: dict):
        """登录成功处理"""
        self.login_success.emit(user_info)
    
    def on_login_failed(self, error_message: str):
        """登录失败处理"""
        QMessageBox.critical(self, "登录失败", f"登录失败：{error_message}")
    
    def on_login_finished(self):
        """登录完成处理"""
        self.login_button.setEnabled(True)
        self.login_button.setText("登录")
    
    def clear_form(self):
        """清空表单"""
        self.password_input.clear()
        self.username_input.setFocus()

