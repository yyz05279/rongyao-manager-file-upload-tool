#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件上传界面
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QFrame,
    QComboBox, QProgressBar, QGroupBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QFileInfo
from PyQt6.QtGui import QFont, QIcon, QColor

from services.upload_service import UploadService
from services.auth_service import AuthService
from services.config_service import ConfigService
from services.base_service import BaseService
from parse_daily_report_excel import DailyReportExcelParser
from convert_to_api_format import convert_to_api_format


class UploadThread(QThread):
    """上传线程"""
    
    progress_updated = pyqtSignal(int)  # 进度更新信号
    upload_success = pyqtSignal(dict)   # 上传成功信号
    upload_failed = pyqtSignal(str)     # 上传失败信号
    
    def __init__(self, parsed_reports: list, project_id: int, reporter_id: int, 
                 api_base_url: str, token: str):
        super().__init__()
        self.parsed_reports = parsed_reports
        self.project_id = project_id
        self.reporter_id = reporter_id
        self.api_base_url = api_base_url
        self.token = token
    
    def run(self):
        """执行上传"""
        try:
            # 发送进度
            self.progress_updated.emit(10)
            
            # 转换为API格式
            api_data = convert_to_api_format(
                self.parsed_reports, 
                self.project_id, 
                self.reporter_id
            )
            
            self.progress_updated.emit(30)
            
            # 创建基础服务实例，自动添加token
            base_service = BaseService(self.api_base_url, self.token)
            
            self.progress_updated.emit(50)
            
            # 调用批量导入API，使用基础服务的POST方法（自动添加token）
            response = base_service.post(
                '/api/v1/daily-reports/batch-import',
                json_data=api_data,
                include_token=True,
                timeout=60
            )
            
            self.progress_updated.emit(80)
            
            # 使用基础服务解析响应
            data = base_service.parse_response(response, expected_code=1)
            
            # 返回导入结果
            upload_result = {
                'totalCount': data.get('totalCount', 0),
                'successCount': data.get('successCount', 0),
                'failedCount': data.get('failedCount', 0),
                'skippedCount': data.get('skippedCount', 0),
                'successReports': data.get('successReports', []),
                'failedReports': data.get('failedReports', [])
            }
            
            self.progress_updated.emit(100)
            self.upload_success.emit(upload_result)
            
        except Exception as e:
            self.upload_failed.emit(str(e))


class UploadWidget(QWidget):
    """文件上传界面类"""
    
    logout_requested = pyqtSignal()  # 退出登录信号
    
    def __init__(self):
        super().__init__()
        self.user_info = None
        self.project_info = None
        self.upload_thread = None
        self.selected_files = []
        self.parsed_reports = []  # 存储解析后的日报数据
        self.auth_service = AuthService()
        self.config_service = ConfigService()
        self.setup_ui()
    
    def setup_ui(self):
        """初始化UI"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
        """)
        
        # 创建滚动内容容器
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        scroll_layout.setContentsMargins(30, 30, 30, 30)
        
        # 顶部工具栏
        toolbar = self.create_toolbar()
        scroll_layout.addWidget(toolbar)
        
        # 用户信息面板
        user_info_group = self.create_user_info_panel()
        scroll_layout.addWidget(user_info_group)
        
        # 文件选择面板
        file_selection_group = self.create_file_selection_panel()
        scroll_layout.addWidget(file_selection_group)
        
        # 文件列表
        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(100)
        self.file_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 10px;
                background-color: white;
                color: #000000;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
                color: #000000;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #000000;
            }
        """)
        scroll_layout.addWidget(self.file_list)
        
        # 数据预览面板
        preview_group = self.create_preview_panel()
        scroll_layout.addWidget(preview_group)
        
        # 上传进度
        progress_group = self.create_progress_panel()
        scroll_layout.addWidget(progress_group)
        
        # 底部按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.clear_button = QPushButton("清空列表")
        self.clear_button.setMinimumSize(130, 45)
        self.clear_button.clicked.connect(self.clear_file_list)
        self.clear_button.setStyleSheet(self.get_button_style("#9E9E9E", "#757575"))
        button_layout.addWidget(self.clear_button)
        
        self.upload_button = QPushButton("开始上传")
        self.upload_button.setMinimumSize(130, 45)
        self.upload_button.clicked.connect(self.start_upload)
        self.upload_button.setStyleSheet(self.get_button_style("#4CAF50", "#388E3C"))
        button_layout.addWidget(self.upload_button)
        
        scroll_layout.addLayout(button_layout)
        
        # 添加底部弹性空间，确保内容不会过度拉伸
        scroll_layout.addStretch()
        
        # 将内容设置到滚动区域
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # 设置整体背景和文字颜色
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: #333333;
            }
        """)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QFrame()
        toolbar.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
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
        title.setStyleSheet("color: #000000;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # 退出登录按钮
        self.logout_button = QPushButton("退出登录")
        self.logout_button.setMinimumSize(110, 40)
        self.logout_button.clicked.connect(self.logout_requested.emit)
        self.logout_button.setStyleSheet(self.get_button_style("#757575", "#616161"))
        layout.addWidget(self.logout_button)
        
        return toolbar
    
    def create_user_info_panel(self):
        """创建用户信息面板"""
        group = QGroupBox("用户和项目信息")
        group.setStyleSheet("""
            QGroupBox {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                font-weight: bold;
                color: #000000;
            }
            QGroupBox::title {
                color: #000000;
            }
        """)
        
        # 使用水平布局，将用户信息和项目信息放在同一行
        layout = QHBoxLayout(group)
        
        # 用户信息
        self.user_label = QLabel("用户：未登录")
        self.user_label.setStyleSheet("color: #000000; font-size: 14px;")
        layout.addWidget(self.user_label)
        
        # 分隔符
        separator = QLabel("|")
        separator.setStyleSheet("color: #cccccc; font-size: 14px; margin: 0 10px;")
        layout.addWidget(separator)
        
        # 当前项目标签
        project_label = QLabel("当前项目:")
        project_label.setStyleSheet("color: #000000; font-weight: bold; font-size: 14px;")
        layout.addWidget(project_label)
        
        # 项目名称
        self.project_name_value = QLabel("未加载")
        self.project_name_value.setStyleSheet("color: #2196F3; font-size: 14px; font-weight: bold;")
        layout.addWidget(self.project_name_value)
        
        layout.addStretch()
        
        return group
    
    def create_file_selection_panel(self):
        """创建文件选择面板"""
        group = QGroupBox("添加文件")
        group.setStyleSheet("""
            QGroupBox {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                font-weight: bold;
                color: #000000;
            }
            QGroupBox::title {
                color: #000000;
            }
        """)
        
        layout = QHBoxLayout(group)
        
        info_label = QLabel("支持格式：Excel (.xlsx, .xls)")
        info_label.setStyleSheet("color: #666666; font-size: 14px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        self.add_file_button = QPushButton("➕ 添加文件")
        self.add_file_button.setMinimumSize(130, 40)
        self.add_file_button.clicked.connect(self.add_files)
        self.add_file_button.setStyleSheet(self.get_button_style("#2196F3", "#1976D2"))
        layout.addWidget(self.add_file_button)
        
        return group
    
    def create_progress_panel(self):
        """创建进度面板"""
        group = QGroupBox("上传进度")
        group.setStyleSheet("""
            QGroupBox {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                font-weight: bold;
                color: #000000;
            }
            QGroupBox::title {
                color: #000000;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(35)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
                background-color: white;
                color: #000000;
                font-size: 14px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("等待上传...")
        self.status_label.setStyleSheet("color: #666666; font-size: 14px; margin-top: 5px;")
        layout.addWidget(self.status_label)
        
        return group
    
    def create_preview_panel(self):
        """创建数据预览面板"""
        group = QGroupBox("数据预览")
        group.setStyleSheet("""
            QGroupBox {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                font-weight: bold;
                color: #000000;
            }
            QGroupBox::title {
                color: #000000;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # 预览按钮行
        button_layout = QHBoxLayout()
        
        info_label = QLabel('添加文件后，点击"预览数据"查看解析结果')
        info_label.setStyleSheet("color: #666666; font-size: 13px;")
        button_layout.addWidget(info_label)
        
        button_layout.addStretch()
        
        self.preview_button = QPushButton("🔍 预览数据")
        self.preview_button.setMinimumSize(130, 40)
        self.preview_button.clicked.connect(self.preview_data)
        self.preview_button.setEnabled(False)
        self.preview_button.setStyleSheet(self.get_button_style("#2196F3", "#1976D2"))
        button_layout.addWidget(self.preview_button)
        
        layout.addLayout(button_layout)
        
        # 数据表格
        self.data_table = QTableWidget()
        self.data_table.setMinimumHeight(250)
        self.data_table.setMaximumHeight(400)
        self.data_table.setColumnCount(8)
        self.data_table.setHorizontalHeaderLabels([
            "日期", "项目名称", "进度状态", "任务数", "人员数", 
            "机械数", "问题数", "天气"
        ])
        
        # 设置表格样式
        self.data_table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background-color: white;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
                color: #000000;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: #000000;
                padding: 8px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
            }
        """)
        
        # 设置表格属性
        self.data_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.data_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.data_table.horizontalHeader().setStretchLastSection(True)
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.data_table)
        
        return group
    
    def get_button_style(self, color: str, hover_color: str = None):
        """获取按钮样式"""
        if hover_color is None:
            hover_color = color
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {hover_color};
                padding-top: 12px;
                padding-bottom: 8px;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #999999;
            }}
        """
    
    def set_user_info(self, user_info: dict, project_info: dict = None):
        """设置用户信息和项目信息"""
        print("\n" + "="*60)
        print("【UI层】进入上传页面")
        print(f"用户信息: {user_info}")
        print(f"项目信息: {project_info}")
        print("="*60 + "\n")
        
        self.user_info = user_info
        self.project_info = project_info
        
        # 显示用户信息
        # 优先显示姓名，如果没有则显示用户名
        name = user_info.get('name')
        username = user_info.get('username', '未知用户')
        role = user_info.get('role', '')
        
        # 构建显示文本
        if name and name != username:
            display_text = f"用户：{name} ({username})"
        else:
            display_text = f"用户：{username}"
        
        # 添加角色信息
        role_map = {
            'ADMIN': '管理员',
            'MANAGER': '项目经理',
            'OPERATOR': '运维人员'
        }
        role_text = role_map.get(role, role)
        if role_text:
            display_text += f" | 角色：{role_text}"
        
        self.user_label.setText(display_text)
        
        print(f"✅ 用户信息已设置: {display_text}\n")
        
        # 显示项目信息
        if project_info:
            # 只显示项目名称
            project_name = project_info.get('name', '未知项目')
            self.project_name_value.setText(project_name)
            print(f"✅ 项目信息已设置: {project_name}\n")
        else:
            self.project_name_value.setText("未加载")
            print("⚠️  没有项目信息\n")
    
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
            
            self.status_label.setText(f'已添加 {len(self.selected_files)} 个文件，请点击"预览数据"查看')
            # 启用预览按钮
            self.preview_button.setEnabled(True)
            # 清空之前的预览数据
            self.parsed_reports.clear()
            self.data_table.setRowCount(0)
            # 禁用上传按钮，直到预览后才能上传
            self.upload_button.setEnabled(False)
    
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
                self.parsed_reports.clear()
                self.file_list.clear()
                self.data_table.setRowCount(0)
                self.progress_bar.setValue(0)
                self.status_label.setText("已清空文件列表")
                self.preview_button.setEnabled(False)
                self.upload_button.setEnabled(False)
    
    def preview_data(self):
        """预览数据"""
        if not self.selected_files:
            QMessageBox.warning(self, "提示", "请先添加文件")
            return
        
        # 禁用预览按钮
        self.preview_button.setEnabled(False)
        self.preview_button.setText("解析中...")
        self.status_label.setText("正在解析Excel文件...")
        
        try:
            self.parsed_reports.clear()
            
            # 解析所有文件
            for file_path in self.selected_files:
                try:
                    parser = DailyReportExcelParser(file_path)
                    all_reports = parser.parse_all_sheets()
                    self.parsed_reports.extend(all_reports)
                except Exception as e:
                    QMessageBox.warning(self, "解析错误", f"文件 {file_path} 解析失败：{str(e)}")
                    continue
            
            if not self.parsed_reports:
                QMessageBox.warning(self, "提示", "没有解析到有效数据")
                return
            
            # 显示在表格中
            self.display_parsed_data()
            
            # 启用上传按钮
            self.upload_button.setEnabled(True)
            self.status_label.setText(f"解析完成，共 {len(self.parsed_reports)} 条日报记录")
            
            QMessageBox.information(
                self, 
                "解析成功", 
                f'成功解析 {len(self.parsed_reports)} 条日报记录\n请检查数据无误后点击"开始上传"'
            )
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"解析失败：{str(e)}")
            self.status_label.setText(f"解析失败：{str(e)}")
        
        finally:
            # 恢复预览按钮
            self.preview_button.setEnabled(True)
            self.preview_button.setText("🔍 预览数据")
    
    def display_parsed_data(self):
        """在表格中显示解析后的数据"""
        self.data_table.setRowCount(len(self.parsed_reports))
        
        # 进度状态映射
        progress_map = {
            'normal': '正常',
            'delayed': '滞后',
            'ahead': '超前'
        }
        
        # 进度状态颜色
        progress_colors = {
            'normal': QColor(76, 175, 80),    # 绿色
            'delayed': QColor(244, 67, 54),   # 红色
            'ahead': QColor(33, 150, 243)     # 蓝色
        }
        
        for row, report in enumerate(self.parsed_reports):
            # 日期
            date_item = QTableWidgetItem(report.get('reportDate', '-'))
            self.data_table.setItem(row, 0, date_item)
            
            # 项目名称
            project_item = QTableWidgetItem(report.get('projectName', '-'))
            self.data_table.setItem(row, 1, project_item)
            
            # 进度状态
            progress = report.get('overallProgress', 'normal')
            progress_text = progress_map.get(progress, '正常')
            progress_item = QTableWidgetItem(progress_text)
            progress_item.setForeground(progress_colors.get(progress, QColor(0, 0, 0)))
            progress_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            self.data_table.setItem(row, 2, progress_item)
            
            # 任务数
            task_count = len(report.get('taskProgressList', []))
            task_item = QTableWidgetItem(str(task_count))
            task_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.data_table.setItem(row, 3, task_item)
            
            # 人员数
            worker_count = report.get('onSitePersonnelCount', 0)
            worker_item = QTableWidgetItem(str(worker_count))
            worker_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.data_table.setItem(row, 4, worker_item)
            
            # 机械数
            machinery_count = len(report.get('machineryRentals', []))
            machinery_item = QTableWidgetItem(str(machinery_count))
            machinery_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.data_table.setItem(row, 5, machinery_item)
            
            # 问题数
            problem_count = len(report.get('problemFeedbacks', []))
            problem_item = QTableWidgetItem(str(problem_count))
            problem_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # 如果有问题，标红
            if problem_count > 0:
                problem_item.setForeground(QColor(244, 67, 54))
                problem_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            self.data_table.setItem(row, 6, problem_item)
            
            # 天气
            weather = report.get('weather', '-')
            weather_item = QTableWidgetItem(weather)
            weather_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.data_table.setItem(row, 7, weather_item)
    
    def start_upload(self):
        """开始上传"""
        # 检查是否已预览数据
        if not self.parsed_reports:
            QMessageBox.warning(self, "提示", '请先点击"预览数据"查看解析结果')
            return
        
        # 使用当前项目ID
        if not self.project_info:
            QMessageBox.warning(self, "提示", "没有项目信息，请重新登录")
            return
        
        project_id = self.project_info.get('id')
        if not project_id:
            QMessageBox.warning(self, "提示", "项目ID无效")
            return
        
        # 获取当前用户ID（应从user_info中获取）
        reporter_id = self.user_info.get('id', 1)
        
        # 获取认证信息
        token = self.user_info.get('token') or self.config_service.get_token()
        api_base_url = self.config_service.get_login_info().get('server_url', 'http://42.192.76.234:8081')
        
        if not token:
            QMessageBox.warning(self, "提示", "登录状态已失效，请重新登录")
            return
        
        # 确认上传
        reply = QMessageBox.question(
            self,
            "确认上传",
            f"确定要上传 {len(self.parsed_reports)} 条日报记录吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # 禁用按钮
        self.upload_button.setEnabled(False)
        self.add_file_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.preview_button.setEnabled(False)
        
        self.status_label.setText("正在上传...")
        
        # 创建并启动上传线程，使用已解析的数据
        self.upload_thread = UploadThread(
            self.parsed_reports, 
            project_id, 
            reporter_id, 
            api_base_url, 
            token
        )
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
        
        # 清空已上传的文件和数据
        self.selected_files.clear()
        self.parsed_reports.clear()
        self.file_list.clear()
        self.data_table.setRowCount(0)
        self.progress_bar.setValue(0)
    
    def on_upload_failed(self, error_message: str):
        """上传失败"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("上传失败")
        msg_box.setText(f"上传失败：{error_message}")
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #000000;
                font-size: 14px;
                min-width: 300px;
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
        """)
        msg_box.exec()
        self.status_label.setText(f"上传失败：{error_message}")
    
    def on_upload_finished(self):
        """上传完成"""
        self.upload_button.setEnabled(True)
        self.add_file_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.preview_button.setEnabled(True)
    
    def has_pending_uploads(self):
        """是否有待上传的文件"""
        return bool(self.selected_files)

