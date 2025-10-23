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
from services.config_service import ConfigService
from services.project_service import ProjectService
from services.app_state import AppState


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()
        self.config_service = ConfigService()
        self.app_state = AppState()  # 全局状态管理
        self.user_info = None
        self.project_info = None
        self.setup_ui()
        self.try_auto_login()
        
    def setup_ui(self):
        """初始化UI"""
        self.setWindowTitle("熔盐管理文件上传工具")
        self.setMinimumSize(QSize(1000, 700))
        
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
        print("\n" + "="*60)
        print("【主窗口】登录成功，切换到上传界面")
        print(f"用户ID: {user_info.get('id')}")
        print(f"用户名: {user_info.get('username')}")
        print(f"姓名: {user_info.get('name')}")
        print("="*60 + "\n")
        
        self.user_info = user_info
        
        # 获取项目信息
        self.fetch_project_info()
        
        # 设置用户信息和项目信息
        self.upload_widget.set_user_info(user_info, self.project_info)
        self.stacked_widget.setCurrentWidget(self.upload_widget)
        
        print("✅ 界面切换完成\n")
    
    def on_logout(self):
        """退出登录处理"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle("确认退出")
        msg_box.setText("确定要退出登录吗？")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        
        # 设置按钮文本为中文
        yes_button = msg_box.button(QMessageBox.StandardButton.Yes)
        yes_button.setText("确定")
        no_button = msg_box.button(QMessageBox.StandardButton.No)
        no_button.setText("取消")
        
        reply = msg_box.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            self.user_info = None
            self.project_info = None
            self.auth_service.clear_token()
            self.config_service.clear_token()
            self.app_state.clear()  # 清空全局状态
            self.login_widget.clear_form()
            self.stacked_widget.setCurrentWidget(self.login_widget)
    
    def closeEvent(self, event):
        """关闭窗口事件"""
        if self.upload_widget.has_pending_uploads():
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("确认退出")
            msg_box.setText("还有文件正在上传，确定要退出吗？")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.No)
            
            # 设置按钮文本为中文
            yes_button = msg_box.button(QMessageBox.StandardButton.Yes)
            yes_button.setText("确定")
            no_button = msg_box.button(QMessageBox.StandardButton.No)
            no_button.setText("取消")
            
            reply = msg_box.exec()
            
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        
        event.accept()
    
    def try_auto_login(self):
        """尝试自动登录（使用保存的Token）"""
        # 获取保存的Token
        token = self.config_service.get_token()
        refresh_token = self.config_service.get_refresh_token()
        
        if not token:
            print("📌 没有保存的Token，显示登录界面")
            return
        
        # 获取保存的登录信息
        login_info = self.config_service.get_login_info()
        api_base_url = login_info.get('server_url', 'http://42.192.76.234:8081')
        
        print("\n" + "="*60)
        print("【主窗口】尝试自动登录")
        print(f"Token: {token[:30] if token else 'None'}...")
        print(f"API URL: {api_base_url}")
        print("="*60 + "\n")
        
        # 设置认证服务的Token
        self.auth_service.set_token(token, api_base_url, refresh_token)
        
        # 尝试获取项目信息（验证Token是否有效）
        try:
            project_service = ProjectService(api_base_url, token)
            self.project_info = project_service.get_my_project()
            
            # Token有效，构建用户信息（简化版）
            # 实际上应该调用用户信息接口获取完整用户信息
            # 这里暂时使用保存的用户名
            username = login_info.get('username', '用户')
            self.user_info = {
                'username': username,
                'token': token,
                'refreshToken': refresh_token
            }
            
            print("✅ 自动登录成功，跳转到上传界面\n")
            
            # 直接跳转到上传界面
            self.upload_widget.set_user_info(self.user_info, self.project_info)
            self.stacked_widget.setCurrentWidget(self.upload_widget)
            
        except Exception as e:
            print(f"❌ 自动登录失败: {e}")
            print("尝试刷新Token...\n")
            
            # 如果有刷新Token，尝试刷新
            if refresh_token:
                try:
                    user_info = self.auth_service.refresh_access_token()
                    
                    # 保存新的Token
                    self.config_service.save_token(
                        user_info.get('token'),
                        user_info.get('refreshToken'),
                        user_info.get('expiresAt')
                    )
                    
                    print("✅ Token刷新成功\n")
                    
                    # 重新获取项目信息
                    self.fetch_project_info()
                    
                    self.user_info = user_info
                    self.upload_widget.set_user_info(user_info, self.project_info)
                    self.stacked_widget.setCurrentWidget(self.upload_widget)
                    
                except Exception as refresh_error:
                    print(f"❌ Token刷新失败: {refresh_error}")
                    print("清除Token，显示登录界面\n")
                    self.config_service.clear_token()
            else:
                print("没有刷新Token，清除Token，显示登录界面\n")
                self.config_service.clear_token()
    
    def fetch_project_info(self):
        """获取项目信息"""
        try:
            if not self.auth_service.get_token():
                print("⚠️  没有Token，无法获取项目信息")
                return
            
            api_base_url = self.auth_service.get_api_base_url()
            token = self.auth_service.get_token()
            
            project_service = ProjectService(api_base_url, token)
            self.project_info = project_service.get_my_project()
            
            # 保存到全局状态
            self.app_state.set_project_info(self.project_info)
            
            print("✅ 项目信息获取成功\n")
            
        except Exception as e:
            print(f"❌ 获取项目信息失败: {e}\n")
            self.project_info = None

