#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目服务
处理项目相关API请求
"""

from typing import Dict
from services.base_service import BaseService


class ProjectService(BaseService):
    """项目服务类"""
    
    def __init__(self, api_base_url: str, token: str):
        """
        初始化项目服务
        
        :param api_base_url: API基础URL
        :param token: 认证Token
        """
        super().__init__(api_base_url, token)
    
    def get_my_project(self) -> Dict:
        """
        获取当前用户的项目信息
        
        :return: 项目信息字典
        :raises Exception: 请求失败时抛出异常
        """
        print("\n" + "="*60)
        print("【获取项目信息】")
        print("="*60 + "\n")
        
        try:
            # 使用基础服务的GET方法，自动添加token
            response = self.get('/api/v1/projects/my-project', include_token=True)
            
            # 使用基础服务的响应解析方法
            project_data = self.parse_response(response, expected_code=1)
            
            print(f"\n✅ 获取项目信息成功")
            print(f"项目ID: {project_data.get('id')}")
            print(f"项目名称: {project_data.get('name')}")
            print(f"项目类型: {project_data.get('typeDisplayName')}")
            print(f"项目状态: {project_data.get('statusDisplayName')}")
            print(f"项目经理: {project_data.get('manager')}\n")
            
            return project_data
            
        except Exception as e:
            print(f"❌ 获取项目信息失败: {str(e)}\n")
            raise

