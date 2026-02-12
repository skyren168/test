#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序配置
"""

import os
from dotenv import load_dotenv

load_dotenv()

class MiniProgramConfig:
    """小程序配置类"""
    
    # 小程序配置
    MINI_PROGRAM_APP_ID = os.getenv('MINI_PROGRAM_APP_ID', 'wx53d1fc369b492f98')
    MINI_PROGRAM_APP_SECRET = os.getenv('MINI_PROGRAM_APP_SECRET', 'df37a8d23ecd22977d5ae4e24e091562')
    MINI_PROGRAM_TEMPLATE_ID = os.getenv('MINI_PROGRAM_TEMPLATE_ID', 'your_template_id_here')
    
    # API配置
    ACCESS_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
    SUBSCRIBE_MESSAGE_URL = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send"
    JSCODE_TO_SESSION_URL = "https://api.weixin.qq.com/sns/jscode2session"
    
    # 定时任务配置
    SCHEDULE_TIME = "08:00"  # 每天上午8点执行
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    
    # 其他配置
    MAX_RETRY = 3
    RETRY_DELAY = 5  # 重试延迟（秒）
    TOKEN_EXPIRE_BUFFER = 300  # token过期缓冲时间（秒）