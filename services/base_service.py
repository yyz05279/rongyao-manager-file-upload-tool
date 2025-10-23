#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础服务类
提供统一的HTTP请求封装，自动处理token
"""

import warnings
# 忽略urllib3的OpenSSL警告
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')

import requests
from typing import Optional, Dict, Any


class BaseService:
    """基础服务类"""
    
    def __init__(self, api_base_url: str = None, token: str = None):
        """
        初始化基础服务
        
        :param api_base_url: API基础URL
        :param token: 认证Token
        """
        self.api_base_url = api_base_url.rstrip('/') if api_base_url else None
        self.token = token
    
    def _get_headers(self, custom_headers: Dict = None, include_token: bool = True) -> Dict:
        """
        获取请求头，自动添加token
        
        :param custom_headers: 自定义请求头
        :param include_token: 是否包含token
        :return: 完整的请求头
        """
        headers = {
            'Content-Type': 'application/json'
        }
        
        # 添加token到请求头
        if include_token and self.token:
            headers['token'] = self.token
        
        # 合并自定义请求头
        if custom_headers:
            headers.update(custom_headers)
        
        return headers
    
    def get(self, endpoint: str, params: Dict = None, 
            include_token: bool = True, timeout: int = 10) -> requests.Response:
        """
        发送GET请求
        
        :param endpoint: API端点（相对路径）
        :param params: 查询参数
        :param include_token: 是否包含token
        :param timeout: 超时时间（秒）
        :return: 响应对象
        """
        if not self.api_base_url:
            raise Exception('API基础URL未设置')
        
        url = f"{self.api_base_url}{endpoint}"
        headers = self._get_headers(include_token=include_token)
        
        print(f"\n[GET] {url}")
        print(f"Headers: {self._safe_log_headers(headers)}")
        if params:
            print(f"Params: {params}")
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout
            )
            print(f"Response: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise
    
    def post(self, endpoint: str, data: Dict = None, json_data: Dict = None,
             include_token: bool = True, timeout: int = 10, 
             custom_headers: Dict = None) -> requests.Response:
        """
        发送POST请求
        
        :param endpoint: API端点（相对路径）
        :param data: 表单数据
        :param json_data: JSON数据
        :param include_token: 是否包含token
        :param timeout: 超时时间（秒）
        :param custom_headers: 自定义请求头
        :return: 响应对象
        """
        if not self.api_base_url:
            raise Exception('API基础URL未设置')
        
        url = f"{self.api_base_url}{endpoint}"
        headers = self._get_headers(custom_headers=custom_headers, include_token=include_token)
        
        print(f"\n[POST] {url}")
        print(f"Headers: {self._safe_log_headers(headers)}")
        if json_data:
            print(f"JSON Data: {self._safe_log_data(json_data)}")
        
        try:
            response = requests.post(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=timeout
            )
            print(f"Response: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise
    
    def put(self, endpoint: str, data: Dict = None, json_data: Dict = None,
            include_token: bool = True, timeout: int = 10) -> requests.Response:
        """
        发送PUT请求
        
        :param endpoint: API端点（相对路径）
        :param data: 表单数据
        :param json_data: JSON数据
        :param include_token: 是否包含token
        :param timeout: 超时时间（秒）
        :return: 响应对象
        """
        if not self.api_base_url:
            raise Exception('API基础URL未设置')
        
        url = f"{self.api_base_url}{endpoint}"
        headers = self._get_headers(include_token=include_token)
        
        print(f"\n[PUT] {url}")
        print(f"Headers: {self._safe_log_headers(headers)}")
        
        try:
            response = requests.put(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=timeout
            )
            print(f"Response: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise
    
    def delete(self, endpoint: str, include_token: bool = True, 
               timeout: int = 10) -> requests.Response:
        """
        发送DELETE请求
        
        :param endpoint: API端点（相对路径）
        :param include_token: 是否包含token
        :param timeout: 超时时间（秒）
        :return: 响应对象
        """
        if not self.api_base_url:
            raise Exception('API基础URL未设置')
        
        url = f"{self.api_base_url}{endpoint}"
        headers = self._get_headers(include_token=include_token)
        
        print(f"\n[DELETE] {url}")
        print(f"Headers: {self._safe_log_headers(headers)}")
        
        try:
            response = requests.delete(
                url,
                headers=headers,
                timeout=timeout
            )
            print(f"Response: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise
    
    def _safe_log_headers(self, headers: Dict) -> Dict:
        """
        安全记录请求头（隐藏敏感信息）
        
        :param headers: 原始请求头
        :return: 安全的请求头（用于日志）
        """
        safe_headers = headers.copy()
        if 'token' in safe_headers and safe_headers['token']:
            safe_headers['token'] = f"{safe_headers['token'][:20]}..."
        return safe_headers
    
    def _safe_log_data(self, data: Dict) -> str:
        """
        安全记录数据（隐藏敏感信息）
        
        :param data: 原始数据
        :return: 安全的数据字符串（用于日志）
        """
        if isinstance(data, dict) and 'password' in data:
            safe_data = data.copy()
            safe_data['password'] = '******'
            return str(safe_data)
        return str(data)
    
    def parse_response(self, response: requests.Response, 
                      expected_code: int = 1) -> Dict:
        """
        解析响应，统一处理错误
        
        :param response: 响应对象
        :param expected_code: 期望的业务状态码（默认1表示成功）
        :return: 响应数据
        :raises Exception: 请求失败时抛出异常
        """
        # 检查HTTP状态码
        if response.status_code != 200:
            error_msg = self._extract_error_message(response)
            raise Exception(f'HTTP {response.status_code}: {error_msg}')
        
        # 解析JSON
        try:
            result = response.json()
        except ValueError as e:
            raise ValueError(f'响应格式错误：{str(e)}')
        
        # 检查业务状态码
        if result.get('code') != expected_code:
            error_msg = result.get('msg', result.get('message', '请求失败'))
            raise Exception(error_msg)
        
        return result.get('data', {})
    
    def _extract_error_message(self, response: requests.Response) -> str:
        """
        从响应中提取错误信息
        
        :param response: 响应对象
        :return: 错误信息
        """
        try:
            result = response.json()
            return result.get('msg', result.get('message', ''))
        except:
            if response.status_code == 401:
                return '未授权或登录已过期'
            elif response.status_code == 403:
                return '没有权限'
            elif response.status_code == 404:
                return '接口不存在'
            elif response.status_code == 500:
                return '服务器内部错误'
            return f'HTTP {response.status_code}'

