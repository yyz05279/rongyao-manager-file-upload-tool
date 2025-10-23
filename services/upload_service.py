#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传服务
处理日报Excel文件的解析和上传
"""

import warnings
# 忽略urllib3的OpenSSL警告
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')

import json
import tempfile
from typing import Dict, Callable, Optional
from pathlib import Path

import requests

from parse_daily_report_excel import DailyReportExcelParser
from convert_to_api_format import convert_to_api_format


class UploadService:
    """上传服务类"""
    
    def __init__(self, api_base_url: str = None, token: str = None):
        """
        初始化上传服务
        
        :param api_base_url: API基础URL
        :param token: 认证Token
        """
        self.api_base_url = api_base_url
        self.token = token
    
    def upload_daily_report_excel(
        self,
        excel_path: str,
        project_id: int,
        reporter_id: int,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> Dict:
        """
        上传日报Excel文件
        
        :param excel_path: Excel文件路径
        :param project_id: 项目ID
        :param reporter_id: 填报人ID
        :param progress_callback: 进度回调函数
        :return: 上传结果字典
        :raises Exception: 上传失败时抛出异常
        """
        # 检查登录状态
        if not self.token or not self.api_base_url:
            raise Exception('未登录，请先登录')
        
        try:
            # 1. 解析Excel文件 (0-30%)
            if progress_callback:
                progress_callback(10)
            
            parser = DailyReportExcelParser(excel_path)
            all_reports = parser.parse_all_sheets()
            
            if not all_reports:
                raise Exception('Excel文件中没有找到有效数据')
            
            if progress_callback:
                progress_callback(30)
            
            # 2. 转换为API格式 (30-40%)
            api_data = convert_to_api_format(all_reports, project_id, reporter_id)
            
            if progress_callback:
                progress_callback(40)
            
            # 3. 调用批量导入API (40-100%)
            result = self._call_batch_import_api(api_data, progress_callback)
            
            if progress_callback:
                progress_callback(100)
            
            return result
            
        except Exception as e:
            raise Exception(f'上传失败：{str(e)}')
    
    def _call_batch_import_api(
        self,
        api_data: Dict,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> Dict:
        """
        调用批量导入API
        
        :param api_data: API格式的数据
        :param progress_callback: 进度回调函数
        :return: 导入结果
        """
        if not self.api_base_url or not self.token:
            raise Exception('未登录或登录已过期')
        
        # 构建API URL
        import_url = f"{self.api_base_url}/api/v1/daily-reports/batch-import"
        
        # 请求头
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        try:
            if progress_callback:
                progress_callback(50)
            
            # 发送请求
            response = requests.post(
                import_url,
                json=api_data,
                headers=headers,
                timeout=60
            )
            
            if progress_callback:
                progress_callback(80)
            
            # 检查响应
            if response.status_code != 200:
                error_msg = self._extract_error_message(response)
                raise Exception(error_msg)
            
            # 解析响应
            result = response.json()
            
            # 检查业务状态码
            if result.get('code') != 200:
                raise Exception(result.get('message', '导入失败'))
            
            # 返回导入结果
            data = result.get('data', {})
            return {
                'totalCount': data.get('totalCount', 0),
                'successCount': data.get('successCount', 0),
                'failedCount': data.get('failedCount', 0),
                'skippedCount': data.get('skippedCount', 0),
                'successReports': data.get('successReports', []),
                'failedReports': data.get('failedReports', [])
            }
            
        except requests.exceptions.Timeout:
            raise Exception('请求超时，请重试')
        except requests.exceptions.ConnectionError:
            raise Exception('网络连接失败')
        except requests.exceptions.RequestException as e:
            raise Exception(f'网络请求失败：{str(e)}')
    
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
            if response.status_code == 401:
                return '登录已过期，请重新登录'
            elif response.status_code == 403:
                return '没有权限执行此操作'
            elif response.status_code == 404:
                return 'API接口不存在'
            else:
                return f'HTTP {response.status_code}'

