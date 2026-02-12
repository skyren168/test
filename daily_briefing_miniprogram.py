#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序版每日信息简报系统
功能：获取北京天气、生活指数、黄历、限行信息，通过小程序订阅消息推送给用户
"""

import requests
import json
import schedule
import time
from datetime import datetime
import logging
from miniprogram_config import MiniProgramConfig

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MiniProgramBriefing:
    def __init__(self, config: MiniProgramConfig):
        """
        初始化小程序简报系统
        
        Args:
            config: 小程序配置
        """
        self.config = config
        self.access_token = ""
        self.token_expire_time = 0
    
    def get_access_token(self) -> str:
        """获取小程序Access Token"""
        # 检查token是否过期
        current_time = time.time()
        if self.access_token and current_time < self.token_expire_time:
            return self.access_token
            
        url = f"{self.config.ACCESS_TOKEN_URL}?grant_type=client_credential&appid={self.config.MINI_PROGRAM_APP_ID}&secret={self.config.MINI_PROGRAM_APP_SECRET}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.access_token = data['access_token']
                    # token有效期为7200秒，提前5分钟刷新
                    self.token_expire_time = current_time + 7200 - self.config.TOKEN_EXPIRE_BUFFER
                    logger.info("小程序Access Token获取成功")
                    return self.access_token
                else:
                    logger.error(f"获取Access Token失败: {data}")
            else:
                logger.error(f"HTTP请求失败: {response.status_code}")
        except Exception as e:
            logger.error(f"获取Access Token异常: {e}")
        
        return ""
    
    def get_weather_info(self) -> dict:
        """获取北京天气信息"""
        try:
            # 模拟天气数据（实际使用时可以接入天气API）
            return {
                "temperature": "8℃",
                "weather": "晴",
                "humidity": "45%",
                "wind": "北风3级",
                "update_time": datetime.now().strftime("%H:%M")
            }
        except Exception as e:
            logger.error(f"获取天气信息失败: {e}")
            return {}
    
    def get_life_index(self) -> dict:
        """获取生活指数"""
        try:
            return {
                "dressing": "较舒适",
                "uv": "中等",
                "car_washing": "适宜",
                "cold": "少发",
                "sport": "适宜",
                "air_quality": "良"
            }
        except Exception as e:
            logger.error(f"获取生活指数失败: {e}")
            return {}
    
    def get_almanac(self) -> dict:
        """获取今日黄历"""
        try:
            today = datetime.now()
            return {
                "date": today.strftime("%Y年%m月%d日"),
                "lunar": "农历腊月廿三",
                "suitable": "祭祀、祈福、求嗣、开光、出行",
                "avoid": "破土、安葬、作灶",
                "zodiac": "龙",
                "star": "心宿"
            }
        except Exception as e:
            logger.error(f"获取黄历失败: {e}")
            return {}
    
    def get_traffic_restriction(self) -> dict:
        """获取尾号限行信息"""
        try:
            today = datetime.now()
            weekday = today.weekday()
            
            # 北京尾号限行规则
            restriction_rules = {
                0: [1, 6],  # 周一
                1: [2, 7],  # 周二
                2: [3, 8],  # 周三
                3: [4, 9],  # 周四
                4: [5, 0],  # 周五
                5: [],      # 周六不限行
                6: []       # 周日不限行
            }
            
            restricted_numbers = restriction_rules.get(weekday, [])
            
            return {
                "date": today.strftime("%Y年%m月%d日"),
                "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][weekday],
                "restricted_numbers": restricted_numbers,
                "time": "7:00-20:00",
                "area": "五环路以内道路（不含五环路）"
            }
        except Exception as e:
            logger.error(f"获取限行信息失败: {e}")
            return {}
    
    def format_subscribe_message_data(self) -> dict:
        """格式化订阅消息数据"""
        # 获取所有信息
        weather = self.get_weather_info()
        life_index = self.get_life_index()
        almanac = self.get_almanac()
        traffic = self.get_traffic_restriction()
        
        # 根据小程序模板格式构建数据
        # 这里需要根据您实际选择的模板调整字段名
        return {
            "thing1": {
                "value": "每日信息简报"
            },
            "date2": {
                "value": datetime.now().strftime("%Y年%m月%d日")
            },
            "thing3": {
                "value": f"{weather.get('weather', 'N/A')} {weather.get('temperature', 'N/A')}"
            },
            "thing4": {
                "value": f"限行:{', '.join(map(str, traffic.get('restricted_numbers', []))) if traffic.get('restricted_numbers') else '不限行'}"
            },
            "thing5": {
                "value": almanac.get('suitable', 'N/A')[:10] + "..." if len(almanac.get('suitable', '')) > 10 else almanac.get('suitable', 'N/A')
            },
            "thing6": {
                "value": f"穿衣:{life_index.get('dressing', 'N/A')}"
            }
        }
    
    def get_user_openids(self) -> list:
        """获取需要发送消息的用户openid列表"""
        # 从文件读取用户openid列表
        # 您需要先创建这个文件并添加用户openid
        try:
            with open('user_openids.txt', 'r', encoding='utf-8') as f:
                openids = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                logger.info(f"找到 {len(openids)} 个用户openid")
                return openids
        except FileNotFoundError:
            logger.warning("用户openid文件不存在，请创建 user_openids.txt")
            # 返回一个测试openid（需要替换为实际用户openid）
            return ["o6_bmjrPTlm6_2sgVt7hMZOPfL2M"]  # 示例openid
        except Exception as e:
            logger.error(f"读取用户openid文件失败: {e}")
            return []
    
    def send_subscribe_message(self, openid: str, message_data: dict) -> bool:
        """发送订阅消息"""
        access_token = self.get_access_token()
        if not access_token:
            logger.error("无法获取Access Token，消息发送失败")
            return False
        
        # 构建订阅消息数据
        template_data = {
            "touser": openid,
            "template_id": self.config.MINI_PROGRAM_TEMPLATE_ID,
            "page": "pages/index/index",  # 点击消息跳转的小程序页面
            "data": message_data
        }
        
        url = f"{self.config.SUBSCRIBE_MESSAGE_URL}?access_token={access_token}"
        
        try:
            response = requests.post(url, json=template_data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                errcode = result.get('errcode', -1)
                
                if errcode == 0:
                    logger.info(f"订阅消息发送成功给用户: {openid[:8]}...")
                    return True
                elif errcode == 43101:
                    logger.warning(f"用户未授权订阅消息: {openid[:8]}...")
                elif errcode == 40037:
                    logger.error(f"模板ID无效，请检查配置")
                else:
                    logger.error(f"订阅消息发送失败: {result}")
            else:
                logger.error(f"HTTP请求失败: {response.status_code}")
                
        except Exception as e:
            logger.error(f"发送订阅消息异常: {e}")
        
        return False
    
    def daily_task(self):
        """每日任务执行"""
        logger.info("开始执行小程序版每日信息简报任务")
        
        try:
            # 获取消息数据
            message_data = self.format_subscribe_message_data()
            
            # 获取用户列表
            user_openids = self.get_user_openids()
            
            if not user_openids:
                logger.warning("没有找到需要发送消息的用户")
                # 测试消息格式
                test_data = {
                    "thing1": {"value": "测试消息"},
                    "date2": {"value": datetime.now().strftime("%Y-%m-%d")},
                    "thing3": {"value": "系统运行正常"}
                }
                logger.info("消息格式测试: %s", json.dumps(test_data, ensure_ascii=False))
                return
            
            success_count = 0
            total_count = len(user_openids)
            
            for i, openid in enumerate(user_openids, 1):
                logger.info(f"正在发送给第 {i}/{total_count} 个用户...")
                if self.send_subscribe_message(openid, message_data):
                    success_count += 1
                
                # 避免发送频率过高
                if i < total_count:
                    time.sleep(0.5)
            
            logger.info(f"每日信息简报发送完成: 成功 {success_count}/{total_count}")
            
        except Exception as e:
            logger.error(f"每日任务执行失败: {e}")
    
    def test_system(self):
        """测试系统功能"""
        logger.info("开始测试小程序版系统功能")
        
        # 测试Access Token获取
        token = self.get_access_token()
        if token:
            logger.info("✓ Access Token获取测试通过")
        else:
            logger.error("✗ Access Token获取测试失败")
            return False
        
        # 测试消息数据格式化
        message_data = self.format_subscribe_message_data()
        if message_data:
            logger.info("✓ 消息数据格式化测试通过")
            logger.info("消息数据示例: %s", json.dumps(message_data, ensure_ascii=False))
        else:
            logger.error("✗ 消息数据格式化测试失败")
            return False
        
        # 测试用户列表获取
        user_openids = self.get_user_openids()
        if user_openids:
            logger.info("✓ 用户列表获取测试通过")
        else:
            logger.warning("⚠ 用户列表为空，请添加用户openid")
        
        logger.info("系统功能测试完成")
        return True
    
    def run_scheduler(self):
        """启动定时任务调度"""
        logger.info("启动小程序版每日信息简报定时任务")
        
        # 先测试系统
        if not self.test_system():
            logger.error("系统测试失败，请检查配置")
            return
        
        # 每天上午9点执行
        schedule.every().day.at(self.config.SCHEDULE_TIME).do(self.daily_task)
        
        logger.info(f"定时任务已设置: 每天 {self.config.SCHEDULE_TIME} 执行")
        
        # 立即执行一次（测试用）
        logger.info("立即执行一次测试任务...")
        self.daily_task()
        
        # 保持调度运行
        logger.info("定时任务调度器已启动，等待执行...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次

def main():
    """主函数"""
    # 创建配置实例
    config = MiniProgramConfig()
    
    # 创建简报系统实例
    briefing_system = MiniProgramBriefing(config)
    
    # 启动定时任务
    briefing_system.run_scheduler()

if __name__ == "__main__":
    main()