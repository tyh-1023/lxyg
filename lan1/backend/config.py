#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
包含蓝心大模型API的配置信息
"""

import os
from typing import Dict, Any

def get_lixin_config() -> Dict[str, Any]:
    """
    获取蓝心大模型API配置
    
    Returns:
        配置字典
    """
    return {
        'APP_ID': os.getenv('LIXIN_APP_ID', 'your_app_id_here'),
        'APP_KEY': os.getenv('LIXIN_APP_KEY', 'your_app_key_here'),
        'API_URL': os.getenv('LIXIN_API_URL', 'https://api.lixin.com/v1/chat/completions'),
        'MODEL': os.getenv('LIXIN_MODEL', 'lixin-v1'),
        'MAX_TOKENS': int(os.getenv('LIXIN_MAX_TOKENS', '2000')),
        'TEMPERATURE': float(os.getenv('LIXIN_TEMPERATURE', '0.7'))
    }

def get_database_config() -> Dict[str, Any]:
    """
    获取数据库配置
    
    Returns:
        配置字典
    """
    return {
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': int(os.getenv('DB_PORT', '5432')),
        'DATABASE': os.getenv('DB_NAME', 'lanxin_db'),
        'USERNAME': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password')
    }

def get_server_config() -> Dict[str, Any]:
    """
    获取服务器配置
    
    Returns:
        配置字典
    """
    return {
        'HOST': os.getenv('SERVER_HOST', '0.0.0.0'),
        'PORT': int(os.getenv('SERVER_PORT', '5000')),
        'DEBUG': os.getenv('DEBUG', 'False').lower() == 'true',
        'SECRET_KEY': os.getenv('SECRET_KEY', 'your-secret-key-here')
    }

def get_crawler_config() -> Dict[str, Any]:
    """
    获取爬虫配置
    
    Returns:
        配置字典
    """
    return {
        'DELAY': float(os.getenv('CRAWLER_DELAY', '1.0')),
        'MAX_RETRIES': int(os.getenv('CRAWLER_MAX_RETRIES', '3')),
        'TIMEOUT': int(os.getenv('CRAWLER_TIMEOUT', '30')),
        'USER_AGENT': os.getenv('CRAWLER_USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    }

# 环境变量说明
ENV_VARS = {
    'LIXIN_APP_ID': '蓝心大模型API的App ID',
    'LIXIN_APP_KEY': '蓝心大模型API的App Key',
    'LIXIN_API_URL': '蓝心大模型API的URL地址',
    'LIXIN_MODEL': '使用的模型名称',
    'LIXIN_MAX_TOKENS': '最大token数量',
    'LIXIN_TEMPERATURE': '生成温度参数',
    'DB_HOST': '数据库主机地址',
    'DB_PORT': '数据库端口',
    'DB_NAME': '数据库名称',
    'DB_USER': '数据库用户名',
    'DB_PASSWORD': '数据库密码',
    'SERVER_HOST': '服务器主机地址',
    'SERVER_PORT': '服务器端口',
    'DEBUG': '是否开启调试模式',
    'SECRET_KEY': '应用密钥',
    'CRAWLER_DELAY': '爬虫延迟时间（秒）',
    'CRAWLER_MAX_RETRIES': '爬虫最大重试次数',
    'CRAWLER_TIMEOUT': '爬虫超时时间（秒）',
    'CRAWLER_USER_AGENT': '爬虫User-Agent'
}

def print_env_vars_help():
    """打印环境变量说明"""
    print("环境变量配置说明：")
    print("=" * 50)
    for var, desc in ENV_VARS.items():
        print(f"{var}: {desc}")
    print("\n示例.env文件内容：")
    print("=" * 50)
    print("# 蓝心大模型API配置")
    print("LIXIN_APP_ID=your_app_id_here")
    print("LIXIN_APP_KEY=your_app_key_here")
    print("LIXIN_API_URL=https://api.lixin.com/v1/chat/completions")
    print("LIXIN_MODEL=lixin-v1")
    print("LIXIN_MAX_TOKENS=2000")
    print("LIXIN_TEMPERATURE=0.7")
    print("\n# 数据库配置")
    print("DB_HOST=localhost")
    print("DB_PORT=5432")
    print("DB_NAME=lanxin_db")
    print("DB_USER=postgres")
    print("DB_PASSWORD=password")
    print("\n# 服务器配置")
    print("SERVER_HOST=0.0.0.0")
    print("SERVER_PORT=5000")
    print("DEBUG=False")
    print("SECRET_KEY=your-secret-key-here")
    print("\n# 爬虫配置")
    print("CRAWLER_DELAY=1.0")
    print("CRAWLER_MAX_RETRIES=3")
    print("CRAWLER_TIMEOUT=30")
    print("CRAWLER_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

if __name__ == "__main__":
    print_env_vars_help() 