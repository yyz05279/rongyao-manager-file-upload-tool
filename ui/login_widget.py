#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
登录界面
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame, QSpacerItem, QSizePolicy, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont

from services.auth_service import AuthService
from services.config_service import ConfigService


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
        print("\n" + "="*60)
        print("【登录线程】开始执行")
        print("="*60 + "\n")
        
        try:
            user_info = self.auth_service.login(
                self.username,
                self.password,
                self.api_base_url
            )
            print("\n✅ 登录线程成功，发送成功信号\n")
            self.login_success.emit(user_info)
        except Exception as e:
            print(f"\n❌ 登录线程失败: {str(e)}")
            print(f"异常类型: {type(e).__name__}\n")
            self.login_failed.emit(str(e))


class LoginWidget(QWidget):
    """登录界面类"""
    
    login_success = pyqtSignal(dict)  # 登录成功信号
    
    def __init__(self):
        super().__init__()
        self.login_thread = None
        self.config_service = ConfigService()
        self.setup_ui()
        self.load_saved_login_info()
    
    def setup_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 添加垂直间距
        layout.addStretch()
        
        # 创建登录表单容器
        form_container = QFrame()
        form_container.setMinimumWidth(500)
        form_container.setMaximumWidth(600)
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 30px;
            }
            QLabel {
                color: #000000;
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
        title_label.setStyleSheet("color: #000000;")
        form_layout.addWidget(title_label)
        
        # 副标题
        subtitle_label = QLabel("文件上传工具")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #333333;")
        form_layout.addWidget(subtitle_label)
        
        form_layout.addSpacing(30)
        
        # 服务器地址
        server_label = QLabel("服务器地址:")
        server_label.setStyleSheet("color: #000000; font-weight: bold; font-size: 14px;")
        form_layout.addWidget(server_label)
        
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("请输入服务器地址")
        self.server_input.setText("http://42.192.76.234:8081")
        self.server_input.setMinimumHeight(45)
        self.server_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                color: #000000;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        form_layout.addWidget(self.server_input)
        
        # 用户名（支持手机号）
        username_label = QLabel("用户名/手机号:")
        username_label.setStyleSheet("color: #000000; font-weight: bold; font-size: 14px;")
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名或手机号")
        self.username_input.setMinimumHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                color: #000000;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        form_layout.addWidget(self.username_input)
        
        # 密码
        password_label = QLabel("密码:")
        password_label.setStyleSheet("color: #000000; font-weight: bold; font-size: 14px;")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                color: #000000;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        form_layout.addWidget(self.password_input)
        
        # 回车键登录
        self.password_input.returnPressed.connect(self.on_login_clicked)
        
        form_layout.addSpacing(10)
        
        # 记住密码复选框
        checkbox_layout = QHBoxLayout()
        self.remember_password_checkbox = QCheckBox("记住密码")
        self.remember_password_checkbox.setStyleSheet("""
            QCheckBox {
                color: #000000;
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        checkbox_layout.addWidget(self.remember_password_checkbox)
        checkbox_layout.addStretch()
        form_layout.addLayout(checkbox_layout)
        
        form_layout.addSpacing(10)
        
        # 登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.setMinimumHeight(50)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                font-size: 18px;
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
        
        print("\n" + "="*60)
        print("【UI层】登录按钮点击")
        print(f"服务器: {server}")
        print(f"用户名: {username}")
        print(f"密码长度: {len(password)}")
        print("="*60 + "\n")
        
        # 验证输入
        if not server:
            print("⚠️  服务器地址为空\n")
            self._show_warning("输入错误", "请输入服务器地址")
            self.server_input.setFocus()
            return
        
        if not username:
            print("⚠️  用户名/手机号为空\n")
            self._show_warning("输入错误", "请输入用户名或手机号")
            self.username_input.setFocus()
            return
        
        if not password:
            print("⚠️  密码为空\n")
            self._show_warning("输入错误", "请输入密码")
            self.password_input.setFocus()
            return
        
        # 禁用登录按钮
        self.login_button.setEnabled(False)
        self.login_button.setText("登录中...")
        
        print("🚀 开始登录流程...\n")
        
        # 创建并启动登录线程
        self.login_thread = LoginThread(username, password, server)
        self.login_thread.login_success.connect(self.on_login_success)
        self.login_thread.login_failed.connect(self.on_login_failed)
        self.login_thread.finished.connect(self.on_login_finished)
        self.login_thread.start()
    
    def on_login_success(self, user_info: dict):
        """登录成功处理"""
        print("\n" + "="*60)
        print("【UI层】登录成功")
        print(f"用户信息: {user_info}")
        print("="*60 + "\n")
        
        # 保存登录信息
        server = self.server_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        remember_password = self.remember_password_checkbox.isChecked()
        
        self.config_service.save_login_info(
            server, username, 
            password if remember_password else None,
            remember_password
        )
        
        # 保存Token
        self.config_service.save_token(
            user_info.get('token'),
            user_info.get('refreshToken'),
            user_info.get('expiresAt')
        )
        
        self.login_success.emit(user_info)
    
    def on_login_failed(self, error_message: str):
        """登录失败处理"""
        print("\n" + "="*60)
        print("【UI层】登录失败")
        print(f"后端返回错误: {error_message}")
        print("="*60 + "\n")
        
        # 创建错误对话框，直接显示后端返回的错误消息
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("登录失败")
        
        # 直接显示后端返回的msg，不添加额外前缀
        # 如果错误消息本身已包含关键词，就直接显示
        # 否则添加"登录失败："前缀
        keywords = [
            '登录', '失败', '错误', '密码', '用户', '账号', 
            '锁定', '过期', '禁用', '验证', '连接', '超时',
            '网络', '服务器', '未找到', '不存在'
        ]
        if any(keyword in error_message for keyword in keywords):
            msg_box.setText(error_message)
        else:
            msg_box.setText(f"登录失败：{error_message}")
        
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #000000;
                font-size: 14px;
                min-width: 350px;
                padding: 10px;
            }
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 16px;
                font-size: 13px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        msg_box.exec()
    
    def on_login_finished(self):
        """登录完成处理"""
        print("🔄 登录流程结束，恢复按钮状态\n")
        self.login_button.setEnabled(True)
        self.login_button.setText("登录")
    
    def clear_form(self):
        """清空表单"""
        self.password_input.clear()
        self.username_input.setFocus()
    
    def _show_warning(self, title: str, message: str):
        """显示警告对话框（黑色字体）"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #000000;
                font-size: 14px;
                min-width: 250px;
            }
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 16px;
                font-size: 13px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
        """)
        msg_box.exec()
    
    def load_saved_login_info(self):
        """加载保存的登录信息"""
        login_info = self.config_service.get_login_info()
        
        if login_info.get('server_url'):
            self.server_input.setText(login_info['server_url'])
        
        if login_info.get('username'):
            self.username_input.setText(login_info['username'])
        
        if login_info.get('remember_password'):
            self.remember_password_checkbox.setChecked(True)
            if login_info.get('password'):
                self.password_input.setText(login_info['password'])

