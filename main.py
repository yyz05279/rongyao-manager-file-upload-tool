#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
熔盐管理文件上传工具
主程序入口
"""

import sys
import os
import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt


def main():
    """主函数"""
    try:
        # 启用高DPI缩放
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        
        # 创建应用程序实例
        app = QApplication(sys.argv)
        app.setApplicationName("熔盐管理文件上传工具")
        app.setOrganizationName("YourCompany")
        
        # 设置插件路径（解决打包后找不到Qt插件的问题）
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller打包后的临时目录
            plugin_path = os.path.join(sys._MEIPASS, 'PyQt6', 'Qt6', 'plugins')
            if os.path.exists(plugin_path):
                app.addLibraryPath(plugin_path)
        
        # 延迟导入主窗口（确保Qt已初始化）
        from ui.main_window import MainWindow
        
        # 创建并显示主窗口
        window = MainWindow()
        window.show()
        
        # 运行应用程序
        sys.exit(app.exec())
        
    except Exception as e:
        # 捕获所有异常并显示错误信息
        error_msg = f"程序启动失败：\n\n{str(e)}\n\n详细错误：\n{traceback.format_exc()}"
        print(error_msg)  # 打印到控制台
        
        # 尝试显示错误对话框
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            QMessageBox.critical(None, "启动错误", error_msg)
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()

