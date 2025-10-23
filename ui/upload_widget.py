#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件上传界面
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QFrame,
    QComboBox, QProgressBar, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QFileInfo
from PyQt6.QtGui import QFont, QIcon

from services.upload_service import UploadService
from services.auth_service import AuthService


class UploadThread(QThread):
    """上传线程"""
    
    progress_updated = pyqtSignal(int)  # 进度更新信号
    upload_success = pyqtSignal(dict)   # 上传成功信号
    upload_failed = pyqtSignal(str)     # 上传失败信号
    
    def __init__(self, file_path: str, project_id: int, reporter_id: int):
        super().__init__()
        self.file_path = file_path
        self.project_id = project_id
        self.reporter_id = reporter_id
        self.upload_service = UploadService()
    
    def run(self):
        """执行上传"""
        try:
            result = self.upload_service.upload_daily_report_excel(
                self.file_path,
                self.project_id,
                self.reporter_id,
                progress_callback=self.progress_updated.emit
            )
            self.upload_success.emit(result)
        except Exception as e:
            self.upload_failed.emit(str(e))


class UploadWidget(QWidget):
    """文件上传界面类"""
    
    logout_requested = pyqtSignal()  # 退出登录信号
    
    def __init__(self):
        super().__init__()
        self.user_info = None
        self.upload_thread = None
        self.selected_files = []
        self.setup_ui()
    
    def setup_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 顶部工具栏
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # 用户信息面板
        user_info_group = self.create_user_info_panel()
        layout.addWidget(user_info_group)
        
        # 文件选择面板
        file_selection_group = self.create_file_selection_panel()
        layout.addWidget(file_selection_group)
        
        # 文件列表
        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(200)
        self.file_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: black;
            }
        """)
        layout.addWidget(self.file_list)
        
        # 上传进度
        progress_group = self.create_progress_panel()
        layout.addWidget(progress_group)
        
        # 底部按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.clear_button = QPushButton("清空列表")
        self.clear_button.setMinimumSize(120, 40)
        self.clear_button.clicked.connect(self.clear_file_list)
        self.clear_button.setStyleSheet(self.get_button_style("#f44336"))
        button_layout.addWidget(self.clear_button)
        
        self.upload_button = QPushButton("开始上传")
        self.upload_button.setMinimumSize(120, 40)
        self.upload_button.clicked.connect(self.start_upload)
        self.upload_button.setStyleSheet(self.get_button_style("#4CAF50"))
        button_layout.addWidget(self.upload_button)
        
        layout.addLayout(button_layout)
        
        # 设置背景
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
        """)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QFrame()
        toolbar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        layout = QHBoxLayout(toolbar)
        
        # 标题
        title = QLabel("📁 日报文件上传")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # 退出登录按钮
        self.logout_button = QPushButton("退出登录")
        self.logout_button.setMinimumSize(100, 35)
        self.logout_button.clicked.connect(self.logout_requested.emit)
        self.logout_button.setStyleSheet(self.get_button_style("#757575"))
        layout.addWidget(self.logout_button)
        
        return toolbar
    
    def create_user_info_panel(self):
        """创建用户信息面板"""
        group = QGroupBox("用户信息")
        group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border-radius: 5px;
                padding: 15px;
                font-weight: bold;
            }
        """)
        
        layout = QHBoxLayout(group)
        
        self.user_label = QLabel("用户：未登录")
        layout.addWidget(self.user_label)
        
        layout.addStretch()
        
        # 项目选择
        project_label = QLabel("项目:")
        layout.addWidget(project_label)
        
        self.project_combo = QComboBox()
        self.project_combo.setMinimumWidth(200)
        self.project_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 2px solid #ddd;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.project_combo)
        
        return group
    
    def create_file_selection_panel(self):
        """创建文件选择面板"""
        group = QGroupBox("添加文件")
        group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border-radius: 5px;
                padding: 15px;
                font-weight: bold;
            }
        """)
        
        layout = QHBoxLayout(group)
        
        info_label = QLabel("支持格式：Excel (.xlsx, .xls)")
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        self.add_file_button = QPushButton("➕ 添加文件")
        self.add_file_button.setMinimumSize(120, 35)
        self.add_file_button.clicked.connect(self.add_files)
        self.add_file_button.setStyleSheet(self.get_button_style("#2196F3"))
        layout.addWidget(self.add_file_button)
        
        return group
    
    def create_progress_panel(self):
        """创建进度面板"""
        group = QGroupBox("上传进度")
        group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border-radius: 5px;
                padding: 15px;
                font-weight: bold;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(30)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("等待上传...")
        self.status_label.setStyleSheet("color: #666;")
        layout.addWidget(self.status_label)
        
        return group
    
    def get_button_style(self, color: str):
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
            QPushButton:pressed {{
                opacity: 0.8;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """
    
    def set_user_info(self, user_info: dict):
        """设置用户信息"""
        self.user_info = user_info
        username = user_info.get('username', '未知用户')
        self.user_label.setText(f"用户：{username}")
        
        # 加载项目列表（这里应该从API获取）
        # 临时使用模拟数据
        self.project_combo.clear()
        self.project_combo.addItem("淮安项目", 1)
        self.project_combo.addItem("测试项目", 2)
    
    def add_files(self):
        """添加文件"""
        from PyQt6.QtWidgets import QFileDialog
        
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择日报Excel文件",
            "",
            "Excel文件 (*.xlsx *.xls)"
        )
        
        if files:
            for file_path in files:
                if file_path not in self.selected_files:
                    self.selected_files.append(file_path)
                    file_info = QFileInfo(file_path)
                    item = QListWidgetItem(f"📄 {file_info.fileName()}")
                    item.setData(Qt.ItemDataRole.UserRole, file_path)
                    self.file_list.addItem(item)
            
            self.status_label.setText(f"已添加 {len(self.selected_files)} 个文件")
    
    def clear_file_list(self):
        """清空文件列表"""
        if self.selected_files:
            reply = QMessageBox.question(
                self,
                "确认清空",
                "确定要清空文件列表吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.selected_files.clear()
                self.file_list.clear()
                self.progress_bar.setValue(0)
                self.status_label.setText("已清空文件列表")
    
    def start_upload(self):
        """开始上传"""
        if not self.selected_files:
            QMessageBox.warning(self, "提示", "请先添加要上传的文件")
            return
        
        project_id = self.project_combo.currentData()
        if not project_id:
            QMessageBox.warning(self, "提示", "请选择项目")
            return
        
        # 获取当前用户ID（应从user_info中获取）
        reporter_id = self.user_info.get('id', 1)
        
        # 禁用按钮
        self.upload_button.setEnabled(False)
        self.add_file_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        
        self.status_label.setText("正在上传...")
        
        # 这里简化处理，只上传第一个文件
        # 实际应该循环处理所有文件
        file_path = self.selected_files[0]
        
        # 创建并启动上传线程
        self.upload_thread = UploadThread(file_path, project_id, reporter_id)
        self.upload_thread.progress_updated.connect(self.on_progress_updated)
        self.upload_thread.upload_success.connect(self.on_upload_success)
        self.upload_thread.upload_failed.connect(self.on_upload_failed)
        self.upload_thread.finished.connect(self.on_upload_finished)
        self.upload_thread.start()
    
    def on_progress_updated(self, progress: int):
        """进度更新"""
        self.progress_bar.setValue(progress)
    
    def on_upload_success(self, result: dict):
        """上传成功"""
        success_count = result.get('successCount', 0)
        failed_count = result.get('failedCount', 0)
        total_count = result.get('totalCount', 0)
        
        message = f"上传完成！\n\n"
        message += f"总计：{total_count} 条\n"
        message += f"成功：{success_count} 条\n"
        message += f"失败：{failed_count} 条"
        
        QMessageBox.information(self, "上传成功", message)
        self.status_label.setText(f"上传完成：成功 {success_count} 条，失败 {failed_count} 条")
        
        # 清空已上传的文件
        self.selected_files.clear()
        self.file_list.clear()
        self.progress_bar.setValue(0)
    
    def on_upload_failed(self, error_message: str):
        """上传失败"""
        QMessageBox.critical(self, "上传失败", f"上传失败：{error_message}")
        self.status_label.setText(f"上传失败：{error_message}")
    
    def on_upload_finished(self):
        """上传完成"""
        self.upload_button.setEnabled(True)
        self.add_file_button.setEnabled(True)
        self.clear_button.setEnabled(True)
    
    def has_pending_uploads(self):
        """是否有待上传的文件"""
        return bool(self.selected_files)

