#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证服务
处理用户登录和JWT Token管理
"""

import requests
from typing import Optional, Dict


class AuthService:
    """认证服务类"""
    
    def __init__(self):
        self.token: Optional[str] = None
        self.api_base_url: Optional[str] = None
    
    def login(self, username: str, password: str, api_base_url: str) -> Dict:
        """
        用户登录
        
        :param username: 用户名
        :param password: 密码
        :param api_base_url: API基础URL
        :return: 用户信息字典
        :raises Exception: 登录失败时抛出异常
        """
        self.api_base_url = api_base_url.rstrip('/')
        
        # 构建登录URL
        login_url = f"{self.api_base_url}/api/v1/auth/login"
        
        # 请求数据
        data = {
            "username": username,
            "password": password
        }
        
        try:
            # 发送登录请求
            response = requests.post(
                login_url,
                json=data,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            
            # 检查响应状态
            if response.status_code != 200:
                error_msg = self._extract_error_message(response)
                raise Exception(error_msg)
            
            # 解析响应
            result = response.json()
            
            # 检查响应码
            if result.get('code') != 200:
                raise Exception(result.get('message', '登录失败'))
            
            # 提取数据
            data = result.get('data', {})
            self.token = data.get('token')
            
            if not self.token:
                raise Exception('服务器未返回Token')
            
            # 返回用户信息
            return {
                'id': data.get('id', 1),
                'username': username,
                'token': self.token
            }
            
        except requests.exceptions.Timeout:
            raise Exception('连接超时，请检查服务器地址')
        except requests.exceptions.ConnectionError:
            raise Exception('无法连接到服务器，请检查服务器地址和网络')
        except requests.exceptions.RequestException as e:
            raise Exception(f'网络请求失败：{str(e)}')
        except Exception as e:
            raise Exception(str(e))
    
    def _extract_error_message(self, response) -> str:
        """
        从响应中提取错误信息
        
        :param response: requests响应对象
        :return: 错误信息
        """
        try:
            result = response.json()
            return result.get('message', f'HTTP {response.status_code}')
        except:
            return f'HTTP {response.status_code}'
    
    def get_token(self) -> Optional[str]:
        """
        获取当前Token
        
        :return: Token字符串或None
        """
        return self.token
    
    def get_api_base_url(self) -> Optional[str]:
        """
        获取API基础URL
        
        :return: URL字符串或None
        """
        return self.api_base_url
    
    def clear_token(self):
        """清除Token"""
        self.token = None
        self.api_base_url = None
    
    def is_logged_in(self) -> bool:
        """
        检查是否已登录
        
        :return: 是否已登录
        """
        return self.token is not None

