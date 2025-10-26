#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证服务
处理用户登录和JWT Token管理
"""

import warnings
# 忽略urllib3的OpenSSL警告
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')

import re
import requests
from typing import Optional, Dict


class AuthService:
    """认证服务类"""
    
    def __init__(self):
        self.token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.api_base_url: Optional[str] = None
    
    @staticmethod
    def _is_phone_number(value: str) -> bool:
        """
        判断输入是否是手机号
        
        :param value: 输入值
        :return: True 表示是手机号，False 表示是用户名
        """
        # 去除空格和特殊字符
        cleaned = re.sub(r'[\s\-()]', '', value)
        
        # 中国手机号：11位数字，以1开头
        if re.match(r'^1\d{10}$', cleaned):
            return True
        
        # 国际手机号：可能包含国家代码，如 +86
        if re.match(r'^\+?\d{10,15}$', cleaned):
            return True
        
        return False
    
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
        
        # 判断是手机号还是用户名
        is_phone = self._is_phone_number(username)
        
        # 构建请求数据
        if is_phone:
            data = {
                "phone": username,
                "password": password
            }
            login_type = "手机号"
        else:
            data = {
                "username": username,
                "password": password
            }
            login_type = "用户名"
        
        # 打印日志
        print("\n" + "="*60)
        print("【登录请求】")
        print(f"URL: {login_url}")
        print(f"登录类型: {login_type}")
        print(f"登录账号: {username}")
        print(f"密码: {'*' * len(password)}")
        print(f"请求数据: {data}")
        print("="*60 + "\n")
        
        try:
            # 发送登录请求
            response = requests.post(
                login_url,
                json=data,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            
            # 打印响应日志
            print("\n" + "="*60)
            print("【登录响应】")
            print(f"状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            print(f"响应内容: {response.text[:500]}")  # 只打印前500字符
            print("="*60 + "\n")
            
            # 检查响应状态
            if response.status_code != 200:
                error_msg = self._extract_error_message(response)
                print(f"\n❌ HTTP状态码错误: {response.status_code}")
                print(f"错误信息: {error_msg}\n")
                raise Exception(error_msg)
            
            # 解析响应
            try:
                result = response.json()
                print(f"\n✅ JSON解析成功")
                print(f"响应结构: {result}\n")
            except ValueError as e:
                print(f"\n❌ JSON解析失败")
                print(f"原始响应: {response.text}\n")
                raise ValueError(f'服务器响应格式错误：{str(e)}')
            
            # 检查响应码（后端成功码为1）
            if result.get('code') != 1:
                error_msg = result.get('msg', result.get('message', '登录失败'))
                print(f"\n❌ 业务状态码错误: {result.get('code')}")
                print(f"错误信息: {error_msg}\n")
                raise Exception(error_msg)
            
            # 提取数据
            data = result.get('data', {})
            user_data = data.get('user', {})
            self.token = data.get('token')
            self.refresh_token = data.get('refreshToken')
            
            print(f"\n✅ 登录成功")
            print(f"用户ID: {user_data.get('id')}")
            print(f"用户名: {user_data.get('username')}")
            print(f"姓名: {user_data.get('name')}")
            print(f"角色: {user_data.get('role')}")
            print(f"Token: {self.token[:30] if self.token else 'None'}...")
            print(f"RefreshToken: {self.refresh_token[:30] if self.refresh_token else 'None'}...\n")
            
            if not self.token:
                print(f"\n❌ Token缺失")
                print(f"返回数据: {data}\n")
                raise Exception('服务器未返回Token')
            
            # 返回用户信息（包含完整的用户数据）
            return {
                'id': user_data.get('id'),
                'username': user_data.get('username'),
                'name': user_data.get('name'),
                'email': user_data.get('email'),
                'role': user_data.get('role'),
                'token': self.token,
                'refreshToken': data.get('refreshToken'),
                'expiresIn': data.get('expiresIn'),
                'expiresAt': data.get('expiresAt')
            }
            
        except requests.exceptions.Timeout as e:
            print(f"\n❌ 连接超时")
            print(f"详细信息: {str(e)}\n")
            raise Exception('连接超时，请检查服务器地址')
        except requests.exceptions.ConnectionError as e:
            print(f"\n❌ 连接错误")
            print(f"详细信息: {str(e)}\n")
            raise Exception('无法连接到服务器，请检查服务器地址和网络')
        except requests.exceptions.RequestException as e:
            print(f"\n❌ 网络请求异常")
            print(f"详细信息: {str(e)}\n")
            raise Exception(f'网络请求失败：{str(e)}')
        except ValueError as e:
            # JSON解析错误（已在上面处理）
            raise Exception(f'服务器响应格式错误：{str(e)}')
        except Exception as e:
            print(f"\n❌ 未知错误")
            print(f"异常类型: {type(e).__name__}")
            print(f"异常信息: {str(e)}\n")
            # 如果异常信息为空，提供默认信息
            error_msg = str(e) if str(e) else '登录失败，请检查用户名和密码'
            raise Exception(error_msg)
    
    def _extract_error_message(self, response) -> str:
        """
        从响应中提取错误信息
        
        :param response: requests响应对象
        :return: 错误信息
        """
        try:
            result = response.json()
            # 优先使用 msg 字段，兼容 message 字段
            error_msg = result.get('msg', result.get('message', ''))
            if error_msg:
                return error_msg
            # 如果没有错误消息，返回状态码
            return f'HTTP {response.status_code}'
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
        self.refresh_token = None
        self.api_base_url = None
    
    def is_logged_in(self) -> bool:
        """
        检查是否已登录
        
        :return: 是否已登录
        """
        return self.token is not None
    
    def set_token(self, token: str, api_base_url: str, refresh_token: str = None):
        """
        设置Token（用于从配置恢复登录状态）
        
        :param token: Token字符串
        :param api_base_url: API基础URL
        :param refresh_token: 刷新Token（可选）
        """
        self.token = token
        self.api_base_url = api_base_url.rstrip('/')
        self.refresh_token = refresh_token
    
    def refresh_access_token(self) -> Dict:
        """
        刷新访问Token
        
        :return: 新的用户信息字典
        :raises Exception: 刷新失败时抛出异常
        """
        if not self.refresh_token:
            raise Exception('没有刷新Token')
        
        if not self.api_base_url:
            raise Exception('API基础URL未设置')
        
        # 构建刷新URL
        refresh_url = f"{self.api_base_url}/api/v1/auth/refresh"
        
        print("\n" + "="*60)
        print("【Token刷新请求】")
        print(f"URL: {refresh_url}")
        print(f"RefreshToken: {self.refresh_token[:30] if self.refresh_token else 'None'}...")
        print("="*60 + "\n")
        
        try:
            # 发送刷新请求
            response = requests.post(
                refresh_url,
                json={"refreshToken": self.refresh_token},
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            
            print("\n" + "="*60)
            print("【Token刷新响应】")
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text[:500]}")
            print("="*60 + "\n")
            
            # 检查响应状态
            if response.status_code != 200:
                error_msg = self._extract_error_message(response)
                raise Exception(error_msg)
            
            # 解析响应
            try:
                result = response.json()
            except ValueError as e:
                raise ValueError(f'服务器响应格式错误：{str(e)}')
            
            # 检查响应码
            if result.get('code') != 1:
                error_msg = result.get('msg', result.get('message', 'Token刷新失败'))
                raise Exception(error_msg)
            
            # 提取新Token
            data = result.get('data', {})
            user_data = data.get('user', {})
            self.token = data.get('token')
            new_refresh_token = data.get('refreshToken')
            
            if new_refresh_token:
                self.refresh_token = new_refresh_token
            
            print(f"\n✅ Token刷新成功")
            print(f"新Token: {self.token[:30] if self.token else 'None'}...\n")
            
            if not self.token:
                raise Exception('服务器未返回新Token')
            
            # 返回用户信息
            return {
                'id': user_data.get('id'),
                'username': user_data.get('username'),
                'name': user_data.get('name'),
                'email': user_data.get('email'),
                'role': user_data.get('role'),
                'token': self.token,
                'refreshToken': self.refresh_token,
                'expiresIn': data.get('expiresIn'),
                'expiresAt': data.get('expiresAt')
            }
            
        except requests.exceptions.Timeout:
            raise Exception('连接超时')
        except requests.exceptions.ConnectionError:
            raise Exception('无法连接到服务器')
        except requests.exceptions.RequestException as e:
            raise Exception(f'网络请求失败：{str(e)}')
        except ValueError as e:
            raise Exception(f'服务器响应格式错误：{str(e)}')
    
    def get_refresh_token(self) -> Optional[str]:
        """
        获取刷新Token
        
        :return: 刷新Token字符串或None
        """
        return self.refresh_token

