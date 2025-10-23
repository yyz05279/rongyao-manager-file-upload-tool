#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理服务
处理登录状态保存、账号密码记住等功能
"""

import json
import os
from typing import Optional, Dict
from pathlib import Path


class ConfigService:
    """配置管理服务类"""
    
    def __init__(self):
        """初始化配置服务"""
        # 配置文件存储路径（用户主目录）
        self.config_dir = Path.home() / '.molten_salt_uploader'
        self.config_file = self.config_dir / 'config.json'
        
        # 确保配置目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载配置
        self._config = self._load_config()
    
    def _load_config(self) -> Dict:
        """
        加载配置文件
        
        :return: 配置字典
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  加载配置文件失败: {e}")
                return {}
        return {}
    
    def _save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, ensure_ascii=False, indent=2)
            print(f"✅ 配置已保存到: {self.config_file}")
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")
    
    def save_login_info(self, server_url: str, username: str, 
                        password: str = None, remember_password: bool = False):
        """
        保存登录信息
        
        :param server_url: 服务器地址
        :param username: 用户名
        :param password: 密码（可选）
        :param remember_password: 是否记住密码
        """
        self._config['server_url'] = server_url
        self._config['username'] = username
        self._config['remember_password'] = remember_password
        
        if remember_password and password:
            # 简单加密存储（实际项目中应使用更安全的加密方式）
            self._config['password'] = self._simple_encrypt(password)
        else:
            self._config.pop('password', None)
        
        self._save_config()
    
    def get_login_info(self) -> Dict:
        """
        获取保存的登录信息
        
        :return: 登录信息字典
        """
        server_url = self._config.get('server_url', 'http://42.192.76.234:8081')
        username = self._config.get('username', '')
        remember_password = self._config.get('remember_password', False)
        password = ''
        
        if remember_password and 'password' in self._config:
            password = self._simple_decrypt(self._config['password'])
        
        return {
            'server_url': server_url,
            'username': username,
            'password': password,
            'remember_password': remember_password
        }
    
    def save_token(self, token: str, refresh_token: str = None, 
                   expires_at: str = None):
        """
        保存Token信息
        
        :param token: 访问Token
        :param refresh_token: 刷新Token
        :param expires_at: 过期时间
        """
        self._config['token'] = token
        if refresh_token:
            self._config['refresh_token'] = refresh_token
        if expires_at:
            self._config['expires_at'] = expires_at
        
        self._save_config()
    
    def get_token(self) -> Optional[str]:
        """
        获取保存的Token
        
        :return: Token字符串或None
        """
        return self._config.get('token')
    
    def get_refresh_token(self) -> Optional[str]:
        """
        获取保存的刷新Token
        
        :return: 刷新Token字符串或None
        """
        return self._config.get('refresh_token')
    
    def get_expires_at(self) -> Optional[str]:
        """
        获取Token过期时间
        
        :return: 过期时间字符串或None
        """
        return self._config.get('expires_at')
    
    def clear_token(self):
        """清除Token信息"""
        self._config.pop('token', None)
        self._config.pop('refresh_token', None)
        self._config.pop('expires_at', None)
        self._save_config()
    
    def clear_all(self):
        """清除所有配置"""
        self._config.clear()
        self._save_config()
    
    def _simple_encrypt(self, text: str) -> str:
        """
        简单加密（实际项目中应使用更安全的加密方式）
        
        :param text: 原始文本
        :return: 加密后的文本
        """
        import base64
        # 这里只是简单的base64编码，不是真正的加密
        # 实际项目中应使用更安全的加密算法
        return base64.b64encode(text.encode()).decode()
    
    def _simple_decrypt(self, encrypted_text: str) -> str:
        """
        简单解密
        
        :param encrypted_text: 加密文本
        :return: 解密后的文本
        """
        import base64
        try:
            return base64.b64decode(encrypted_text.encode()).decode()
        except Exception:
            return ''

