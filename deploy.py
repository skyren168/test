#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署脚本
"""

import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def install_dependencies():
    """安装依赖"""
    logger.info("正在安装依赖包...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("依赖包安装成功")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"依赖包安装失败: {e}")
        return False

def setup_environment():
    """设置环境"""
    logger.info("正在设置环境...")
    
    # 检查.env文件是否存在
    if not os.path.exists(".env"):
        logger.warning(".env文件不存在，请复制.env.example并配置相关参数")
        return False
    
    logger.info("环境设置完成")
    return True

def test_system():
    """测试系统"""
    logger.info("正在测试系统...")
    
    try:
        # 导入主模块进行测试
        from daily_briefing import DailyBriefing
        from config import Config
        
        # 创建测试配置
        test_config = {
            "app_id": "test",
            "app_secret": "test",
            "template_id": "test"
        }
        
        # 创建实例
        briefing = DailyBriefing(test_config)
        
        # 测试消息格式化
        message = briefing.format_briefing_message()
        logger.info("消息格式化测试成功")
        
        # 测试发送（模拟）
        success = briefing.send_to_wechat("测试消息")
        if success:
            logger.info("消息发送测试成功")
        
        return True
        
    except Exception as e:
        logger.error(f"系统测试失败: {e}")
        return False

def main():
    """主部署函数"""
    logger.info("开始部署每日信息简报系统")
    
    # 安装依赖
    if not install_dependencies():
        logger.error("依赖安装失败，部署中止")
        return False
    
    # 设置环境
    if not setup_environment():
        logger.warning("环境设置不完整，请手动配置.env文件")
    
    # 测试系统
    if test_system():
        logger.info("系统部署成功！")
        logger.info("请运行以下命令启动系统:")
        logger.info("python daily_briefing.py")
        return True
    else:
        logger.error("系统测试失败，请检查配置")
        return False

if __name__ == "__main__":
    main()