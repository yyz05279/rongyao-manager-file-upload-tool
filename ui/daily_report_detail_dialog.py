#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日报详情对话框
展示日报的完整详细信息
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QGroupBox, QScrollArea, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from services.app_state import AppState


class DailyReportDetailDialog(QDialog):
    """日报详情对话框"""
    
    def __init__(self, report_data: dict, parent=None):
        super().__init__(parent)
        self.report_data = report_data
        self.app_state = AppState()  # 获取全局状态
        self.project_info = self.app_state.get_project_info()  # 获取项目信息
        self.setup_ui()
    
    def setup_ui(self):
        """初始化UI"""
        self.setWindowTitle("日报详细信息")
        self.setMinimumSize(900, 700)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_layout = QHBoxLayout()
        title_label = QLabel("📋 日报详细信息")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2196F3;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # 基本信息卡片
        basic_info = self.create_basic_info_panel()
        layout.addWidget(basic_info)
        
        # 选项卡
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background: white;
            }
            QTabBar::tab {
                background: #f5f5f5;
                color: #333333;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #2196F3;
                color: white;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #e3f2fd;
            }
        """)
        
        # 添加各个选项卡 - 按照Excel序号结构组织
        tab_widget.addTab(self.create_task_progress_tab(), "📋 逐项进度汇报（序号2）")
        tab_widget.addTab(self.create_tomorrow_plans_tab(), "📅 明日工作计划（序号3）")
        tab_widget.addTab(self.create_worker_reports_tab(), "👷 各工种工作汇报（二）")
        tab_widget.addTab(self.create_machinery_tab(), "🚜 机械租赁情况（三）")
        tab_widget.addTab(self.create_problems_and_requirements_tab(), "⚠️ 问题反馈（四）")
        
        layout.addWidget(tab_widget)
        
        # 关闭按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_button = QPushButton("关闭")
        close_button.setMinimumSize(100, 40)
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # 设置整体样式
        self.setStyleSheet("""
            QDialog {
                background-color: #fafafa;
            }
        """)
    
    def create_basic_info_panel(self):
        """创建基本信息面板"""
        group = QGroupBox("基本信息")
        group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                font-weight: bold;
                font-size: 14px;
                color: #2196F3;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(10)
        
        # 创建信息行
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)
        
        # 日期和项目名称
        row1 = QHBoxLayout()
        row1.addWidget(self._create_info_label("📅 日期:", self.report_data.get('reportDate', '-')))
        
        # 项目信息（优先从全局状态获取）
        project_name = self.report_data.get('projectName', '-')
        if self.project_info:
            project_name = self.project_info.get('name', project_name)
        row1.addWidget(self._create_info_label("📁 项目:", project_name))
        info_layout.addLayout(row1)
        
        # 项目详细信息（如果有）
        if self.project_info:
            row1_extra = QHBoxLayout()
            project_type = self.project_info.get('typeDisplayName', '-')
            project_status = self.project_info.get('statusDisplayName', '-')
            row1_extra.addWidget(self._create_info_label("🏷️ 类型:", project_type))
            row1_extra.addWidget(self._create_info_label("📊 状态:", project_status))
            info_layout.addLayout(row1_extra)
        
        # 进度状态和描述
        row2 = QHBoxLayout()
        progress = self.report_data.get('overallProgress', 'normal')
        progress_map = {'normal': '正常🟢', 'delayed': '滞后🔴', 'ahead': '超前🔵'}
        progress_text = progress_map.get(progress, '正常🟢')
        row2.addWidget(self._create_info_label("🎯 进度状态:", progress_text))
        info_layout.addLayout(row2)
        
        # 进度描述
        progress_desc = self.report_data.get('progressDescription', '-')
        if progress_desc and progress_desc != '-':
            desc_label = QLabel(f"📝 进度描述: {progress_desc}")
            desc_label.setStyleSheet("color: #666666; font-size: 13px; padding: 5px;")
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)
        
        # 统计信息
        row3 = QHBoxLayout()
        task_count = len(self.report_data.get('taskProgressList', []))
        worker_count = self.report_data.get('onSitePersonnelCount', 0)
        machinery_count = len(self.report_data.get('machineryRentals', []))
        problem_count = len(self.report_data.get('problemFeedbacks', []))
        
        row3.addWidget(self._create_info_label("📋 任务数:", str(task_count)))
        row3.addWidget(self._create_info_label("👷 人员数:", str(worker_count)))
        row3.addWidget(self._create_info_label("🚜 机械数:", str(machinery_count)))
        row3.addWidget(self._create_info_label("⚠️ 问题数:", str(problem_count)))
        info_layout.addLayout(row3)
        
        # 天气信息
        weather = self.report_data.get('weather', '-')
        temperature = self.report_data.get('temperature', '-')
        if weather and weather != '-':
            row4 = QHBoxLayout()
            row4.addWidget(self._create_info_label("☀️ 天气:", weather))
            if temperature and temperature != '-':
                row4.addWidget(self._create_info_label("🌡️ 温度:", temperature))
            info_layout.addLayout(row4)
        
        # 项目管理信息（从全局状态获取）
        if self.project_info:
            row5 = QHBoxLayout()
            manager = self.project_info.get('manager', '-')
            completion_progress = self.project_info.get('completionProgress', 0)
            row5.addWidget(self._create_info_label("👨‍💼 项目经理:", manager))
            row5.addWidget(self._create_info_label("📈 项目完成度:", f"{completion_progress}%"))
            info_layout.addLayout(row5)
            
            # 熔盐量信息
            estimated_salt = self.project_info.get('estimatedSaltAmount', 0)
            actual_salt = self.project_info.get('actualSaltAmount', 0)
            if estimated_salt or actual_salt:
                row6 = QHBoxLayout()
                row6.addWidget(self._create_info_label("🎯 计划熔盐量:", f"{estimated_salt} 吨"))
                row6.addWidget(self._create_info_label("✅ 实际熔盐量:", f"{actual_salt} 吨"))
                info_layout.addLayout(row6)
        
        layout.addLayout(info_layout)
        
        return group
    
    def _create_info_label(self, title: str, value: str):
        """创建信息标签"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5, 2, 5, 2)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #333333; font-weight: bold; font-size: 13px;")
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: #666666; font-size: 13px;")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        return container
    
    def create_task_progress_tab(self):
        """创建任务进度选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        tasks = self.report_data.get('taskProgressList', [])
        
        if not tasks:
            no_data_label = QLabel("暂无任务进度数据")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet("color: #999999; font-size: 14px; padding: 50px;")
            layout.addWidget(no_data_label)
            return widget
        
        table = QTableWidget()
        table.setRowCount(len(tasks))
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "序号", "任务名称", "计划进度", "实际进度", "偏差原因", "影响及措施"
        ])
        
        # 设置表格样式
        self._setup_table_style(table)
        
        # 填充数据
        for row, task in enumerate(tasks):
            table.setItem(row, 0, QTableWidgetItem(task.get('taskNo', '-')))
            table.setItem(row, 1, QTableWidgetItem(task.get('taskName', '-')))
            table.setItem(row, 2, QTableWidgetItem(task.get('plannedProgress', '-')))
            table.setItem(row, 3, QTableWidgetItem(task.get('actualProgress', '-')))
            table.setItem(row, 4, QTableWidgetItem(task.get('deviationReason', '-')))
            table.setItem(row, 5, QTableWidgetItem(task.get('impactMeasures', '-')))
        
        layout.addWidget(table)
        return widget
    
    def create_tomorrow_plans_tab(self):
        """创建明日计划选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        plans = self.report_data.get('tomorrowPlans', [])
        
        if not plans:
            no_data_label = QLabel("暂无明日计划数据")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet("color: #999999; font-size: 14px; padding: 50px;")
            layout.addWidget(no_data_label)
            return widget
        
        table = QTableWidget()
        table.setRowCount(len(plans))
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "序号", "任务名称", "目标", "负责人", "所需资源", "备注"
        ])
        
        self._setup_table_style(table)
        
        for row, plan in enumerate(plans):
            table.setItem(row, 0, QTableWidgetItem(plan.get('planNo', '-')))
            table.setItem(row, 1, QTableWidgetItem(plan.get('taskName', '-')))
            table.setItem(row, 2, QTableWidgetItem(plan.get('goal', '-')))
            table.setItem(row, 3, QTableWidgetItem(plan.get('responsiblePerson', '-')))
            table.setItem(row, 4, QTableWidgetItem(plan.get('requiredResources', '-')))
            table.setItem(row, 5, QTableWidgetItem(plan.get('remarks', '-')))
        
        layout.addWidget(table)
        return widget
    
    def create_worker_reports_tab(self):
        """创建人员报告选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        workers = self.report_data.get('workerReports', [])
        
        if not workers:
            no_data_label = QLabel("暂无人员报告数据")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet("color: #999999; font-size: 14px; padding: 50px;")
            layout.addWidget(no_data_label)
            return widget
        
        table = QTableWidget()
        table.setRowCount(len(workers))
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "序号", "姓名", "工种", "类型", "工作内容", "工时"
        ])
        
        self._setup_table_style(table)
        
        for row, worker in enumerate(workers):
            table.setItem(row, 0, QTableWidgetItem(worker.get('seqNo', '-')))
            table.setItem(row, 1, QTableWidgetItem(worker.get('name', '-')))
            table.setItem(row, 2, QTableWidgetItem(worker.get('jobType', '-')))
            table.setItem(row, 3, QTableWidgetItem(worker.get('workerType', '-')))
            table.setItem(row, 4, QTableWidgetItem(worker.get('workContent', '-')))
            table.setItem(row, 5, QTableWidgetItem(worker.get('workHours', '-')))
        
        layout.addWidget(table)
        return widget
    
    def create_machinery_tab(self):
        """创建机械租赁选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        machinery = self.report_data.get('machineryRentals', [])
        
        if not machinery:
            no_data_label = QLabel("暂无机械租赁数据")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet("color: #999999; font-size: 14px; padding: 50px;")
            layout.addWidget(no_data_label)
            return widget
        
        table = QTableWidget()
        table.setRowCount(len(machinery))
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "序号", "机械名称", "数量", "吨位", "用途", "合班", "备注"
        ])
        
        self._setup_table_style(table)
        
        for row, item in enumerate(machinery):
            table.setItem(row, 0, QTableWidgetItem(item.get('seqNo', '-')))
            table.setItem(row, 1, QTableWidgetItem(item.get('machineName', '-')))
            table.setItem(row, 2, QTableWidgetItem(item.get('quantity', '-')))
            table.setItem(row, 3, QTableWidgetItem(item.get('tonnage', '-')))
            table.setItem(row, 4, QTableWidgetItem(item.get('usage', '-')))
            table.setItem(row, 5, QTableWidgetItem(item.get('shift', '-')))
            table.setItem(row, 6, QTableWidgetItem(item.get('remarks', '-')))
        
        layout.addWidget(table)
        return widget
    
    def create_problems_and_requirements_tab(self):
        """创建问题反馈选项卡（包含问题反馈和需求描述）"""
        widget = QWidget()
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        # 容器widget
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 1. 问题反馈分组
        problems_group = self._create_problems_group()
        main_layout.addWidget(problems_group)
        
        # 2. 需求描述分组
        requirements_group = self._create_requirements_group()
        main_layout.addWidget(requirements_group)
        
        main_layout.addStretch()
        
        scroll.setWidget(container)
        
        # 外层布局
        outer_layout = QVBoxLayout(widget)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll)
        
        return widget
    
    def _create_problems_group(self):
        """创建问题反馈分组"""
        group = QGroupBox("1. 问题反馈")
        group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                font-weight: bold;
                font-size: 14px;
                color: #F44336;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        layout.setContentsMargins(10, 20, 10, 10)
        
        problems = self.report_data.get('problemFeedbacks', [])
        
        if not problems:
            no_data_label = QLabel("✅ 暂无问题反馈")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet("color: #4CAF50; font-size: 14px; font-weight: bold; padding: 30px;")
            layout.addWidget(no_data_label)
        else:
            table = QTableWidget()
            table.setRowCount(len(problems))
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels([
                "序号", "问题描述", "原因", "影响", "处理进度"
            ])
            
            self._setup_table_style(table)
            
            for row, problem in enumerate(problems):
                table.setItem(row, 0, QTableWidgetItem(problem.get('problemNo', '-')))
                
                # 问题描述标红
                desc_item = QTableWidgetItem(problem.get('description', '-'))
                desc_item.setForeground(QColor(244, 67, 54))
                table.setItem(row, 1, desc_item)
                
                table.setItem(row, 2, QTableWidgetItem(problem.get('reason', '-')))
                table.setItem(row, 3, QTableWidgetItem(problem.get('impact', '-')))
                table.setItem(row, 4, QTableWidgetItem(problem.get('progress', '-')))
            
            layout.addWidget(table)
        
        return group
    
    def _create_requirements_group(self):
        """创建需求描述分组"""
        group = QGroupBox("2. 需求描述")
        group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                font-weight: bold;
                font-size: 14px;
                color: #2196F3;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        layout.setContentsMargins(10, 20, 10, 10)
        
        requirements = self.report_data.get('requirements', [])
        
        if not requirements:
            no_data_label = QLabel("暂无需求描述")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet("color: #999999; font-size: 14px; padding: 30px;")
            layout.addWidget(no_data_label)
        else:
            table = QTableWidget()
            table.setRowCount(len(requirements))
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels([
                "序号", "需求描述", "紧急程度", "期望时间"
            ])
            
            self._setup_table_style(table)
            
            for row, req in enumerate(requirements):
                table.setItem(row, 0, QTableWidgetItem(req.get('requirementNo', '-')))
                table.setItem(row, 1, QTableWidgetItem(req.get('description', '-')))
                table.setItem(row, 2, QTableWidgetItem(req.get('urgencyLevel', '-')))
                table.setItem(row, 3, QTableWidgetItem(req.get('expectedTime', '-')))
            
            layout.addWidget(table)
        
        return group
    
    def _setup_table_style(self, table: QTableWidget):
        """设置表格样式"""
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e0e0e0;
                background-color: white;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
                color: #333333;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                color: #333333;
                padding: 10px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
            }
        """)
        
        # 设置表格属性
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        table.verticalHeader().setVisible(False)
        
        # 启用自动换行
        table.setWordWrap(True)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        # 设置列宽
        for i in range(table.columnCount()):
            table.setColumnWidth(i, 150)

