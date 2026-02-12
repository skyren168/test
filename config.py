#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类"""
    
    # 微信公众号配置
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', 'your_wechat_app_id')
    WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET', 'your_wechat_app_secret')
    WECHAT_TEMPLATE_ID = os.getenv('WECHAT_TEMPLATE_ID', 'your_template_id')
    
    # 天气API配置
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'your_weather_api_key')
    WEATHER_LOCATION = "101010100"  # 北京地区代码
    
    # 定时任务配置
    SCHEDULE_TIME = "09:00"  # 每天上午9点执行
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    
    # 其他配置
    MAX_RETRY = 3
    RETRY_DELAY = 5  # 重试延迟（秒）