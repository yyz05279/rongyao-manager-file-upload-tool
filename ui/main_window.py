#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QStackedWidget,
    QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from ui.login_widget import LoginWidget
from ui.upload_widget import UploadWidget
from services.auth_service import AuthService


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()
        self.user_info = None
        self.setup_ui()
        
    def setup_ui(self):
        """初始化UI"""
        self.setWindowTitle("熔盐管理文件上传工具")
        self.setMinimumSize(QSize(900, 600))
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建堆叠窗口部件
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # 创建登录页面
        self.login_widget = LoginWidget()
        self.login_widget.login_success.connect(self.on_login_success)
        self.stacked_widget.addWidget(self.login_widget)
        
        # 创建上传页面
        self.upload_widget = UploadWidget()
        self.upload_widget.logout_requested.connect(self.on_logout)
        self.stacked_widget.addWidget(self.upload_widget)
        
        # 显示登录页面
        self.stacked_widget.setCurrentWidget(self.login_widget)
        
        # 居中显示窗口
        self.center_window()
    
    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        window_rect = self.frameGeometry()
        center_point = screen.center()
        window_rect.moveCenter(center_point)
        self.move(window_rect.topLeft())
    
    def on_login_success(self, user_info: dict):
        """登录成功处理"""
        self.user_info = user_info
        self.upload_widget.set_user_info(user_info)
        self.stacked_widget.setCurrentWidget(self.upload_widget)
    
    def on_logout(self):
        """退出登录处理"""
        reply = QMessageBox.question(
            self,
            "确认退出",
            "确定要退出登录吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.user_info = None
            self.auth_service.clear_token()
            self.login_widget.clear_form()
            self.stacked_widget.setCurrentWidget(self.login_widget)
    
    def closeEvent(self, event):
        """关闭窗口事件"""
        if self.upload_widget.has_pending_uploads():
            reply = QMessageBox.question(
                self,
                "确认退出",
                "还有文件正在上传，确定要退出吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        
        event.accept()

