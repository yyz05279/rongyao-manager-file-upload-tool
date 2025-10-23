#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用全局状态管理
单例模式，存储全局共享的数据
"""


class AppState:
    """应用全局状态管理类（单例）"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化"""
        if self._initialized:
            return
        
        self._initialized = True
        self._project_info = None
        self._user_info = None
    
    def set_project_info(self, project_info: dict):
        """设置项目信息"""
        self._project_info = project_info
        print(f"📦 全局状态：项目信息已更新 - {project_info.get('name', '未知项目') if project_info else 'None'}")
    
    def get_project_info(self) -> dict:
        """获取项目信息"""
        return self._project_info
    
    def set_user_info(self, user_info: dict):
        """设置用户信息"""
        self._user_info = user_info
        print(f"👤 全局状态：用户信息已更新 - {user_info.get('username', '未知用户') if user_info else 'None'}")
    
    def get_user_info(self) -> dict:
        """获取用户信息"""
        return self._user_info
    
    def clear(self):
        """清空所有状态"""
        self._project_info = None
        self._user_info = None
        print("🧹 全局状态：已清空")
    
    def has_project_info(self) -> bool:
        """是否有项目信息"""
        return self._project_info is not None
    
    def has_user_info(self) -> bool:
        """是否有用户信息"""
        return self._user_info is not None

