#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rocket推送模块
功能：将每日信息简报推送到Rocket的每日黄历频道
"""

import requests
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RocketPush:
    """Rocket推送类"""
    
    def __init__(self, token, user_id, channel="每日黄历"):
        """
        初始化Rocket推送
        
        Args:
            token: Rocket个人访问令牌
            user_id: Rocket用户ID
            channel: 推送频道名称
        """
        self.token = token
        self.user_id = user_id
        self.channel = "mei3-ri4-huang2-li4"  # 实际频道名称
        self.base_url = "https://chat.akria.net/api/v1"  # Rocket服务器地址
    
    def get_user_channels(self):
        """获取用户的所有频道"""
        headers = {
            "X-Auth-Token": self.token,
            "X-User-Id": self.user_id,
            "Content-Type": "application/json"
        }
        
        try:
            # 获取用户加入的channels
            response = requests.get(f"{self.base_url}/channels.list.joined", 
                                  headers=headers, 
                                  timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    channels = data.get("channels", [])
                    print("\n📋 用户加入的Channels:")
                    for channel in channels:
                        print(f"  - {channel.get('name')} (ID: {channel.get('_id')})")
            
            # 获取用户加入的groups
            response = requests.get(f"{self.base_url}/groups.list", 
                                  headers=headers, 
                                  timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    groups = data.get("groups", [])
                    print("\n📋 用户加入的Groups:")
                    for group in groups:
                        print(f"  - {group.get('name')} (ID: {group.get('_id')})")
            
        except Exception as e:
            logger.error(f"获取用户频道列表异常: {e}")
        
    def get_channel_id(self):
        """获取频道ID"""
        # 直接返回已知的频道ID
        return "698d7b667c0af801b7e72bd8"
    
    def send_message(self, message):
        """
        发送消息到Rocket频道
        
        Args:
            message: 消息内容
            
        Returns:
            bool: 发送是否成功
        """
        channel_id = self.get_channel_id()
        if not channel_id:
            logger.error("无法获取频道ID，发送失败")
            return False
        
        headers = {
            "X-Auth-Token": self.token,
            "X-User-Id": self.user_id,
            "Content-Type": "application/json"
        }
        
        # 简化消息格式，只包含必要字段
        payload = {
            "roomId": channel_id,
            "text": message
        }
        
        try:
            # 尝试使用简化的消息格式
            response = requests.post(f"{self.base_url}/chat.postMessage", 
                                   headers=headers, 
                                   json=payload, 
                                   timeout=10)
            
            print(f"\n🔧 发送消息请求:")
            print(f"  URL: {self.base_url}/chat.postMessage")
            print(f"  Headers: {headers}")
            print(f"  Payload: {payload}")
            print(f"  Response status: {response.status_code}")
            print(f"  Response text: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    logger.info(f"Rocket消息发送成功")
                    return True
                else:
                    logger.error(f"Rocket消息发送失败: {data.get('error')}")
            else:
                logger.error(f"Rocket消息发送失败: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Rocket消息发送异常: {e}")
        
        return False
    
    def format_message(self, weather, life_index, almanac, traffic, constellation=None, i_ching=None):
        """
        格式化消息内容
        
        Args:
            weather: 天气信息
            life_index: 生活指数
            almanac: 黄历信息
            traffic: 交通限行信息
            constellation: 星座运势信息
            i_ching: 易经信息
            
        Returns:
            str: 格式化后的消息
        """
        today = datetime.now().strftime("%Y年%m月%d日")
        
        message = f"""
【每日信息简报】
📅 {today}

--------------------
【天气】
🌤️ 天气：{weather.get('weather', '未知')}
🌡️ 温度：{weather.get('temperature', '未知')}
💧 湿度：{weather.get('humidity', '未知')}
💨 风力：{weather.get('wind', '未知')}

--------------------
【生活指数】
👔 穿衣：{life_index.get('dressing', '未知')}
☀️ 紫外线：{life_index.get('uv', '未知')}
🚗 洗车：{life_index.get('car_washing', '未知')}
🤧 感冒：{life_index.get('cold', '未知')}
🏃 运动：{life_index.get('sport', '未知')}
🌬️ 空气：{life_index.get('air_quality', '未知')}

--------------------
【黄历】
📅 农历：{almanac.get('lunar', '未知')}
🐉 生肖：{almanac.get('zodiac', '未知')}
✅ 宜：{almanac.get('suitable', '未知')}
❌ 忌：{almanac.get('avoid', '未知')}

--------------------
【限行】
🚫 {', '.join(map(str, traffic.get('restricted_numbers', []))) if traffic.get('restricted_numbers') else '不限行'}
⏰ 7:00-20:00 | 📍 五环路以内

--------------------
【星座】
⭐ {constellation.get('constellation', '未知') if constellation else '未知'}
🌟 整体：{constellation.get('overall', '未知') if constellation else '未知'}
💖 爱情：{constellation.get('love', '未知') if constellation else '未知'}
💼 事业：{constellation.get('career', '未知') if constellation else '未知'}
💰 财运：{constellation.get('wealth', '未知') if constellation else '未知'}
🧘 健康：{constellation.get('health', '未知') if constellation else '未知'}

--------------------
【易经】
🔮 卦象：{i_ching.get('hexagram', '未知') if i_ching else '未知'}
🌅 寓意：{i_ching.get('meaning', '未知') if i_ching else '未知'}
🔢 幸运数字：{i_ching.get('lucky_number', '未知') if i_ching else '未知'}
🎨 幸运颜色：{i_ching.get('lucky_color', '未知') if i_ching else '未知'}

--------------------
【寄语】
愿您的每一天都充满阳光与希望，事业有成，家庭幸福！
"""
        
        return message

class RocketConfig:
    """Rocket配置类"""
    
    # Rocket配置
    ROCKET_TOKEN = "Z8J2ssokeK0IdJo7e-h7qtpWinhJhac6tC6E13rBFL0"
    ROCKET_USER_ID = "mkvGvyyAjT5x4d8xt"
    ROCKET_CHANNEL = "mei3-ri4-huang2-li4"  # 实际频道名称
    ROCKET_SERVER_URL = "https://chat.akria.net/api/v1"  # Rocket服务器地址

if __name__ == "__main__":
    """测试Rocket推送"""
    print("🧪 测试Rocket推送功能")
    print("=" * 50)
    
    # 测试配置
    config = RocketConfig()
    rocket = RocketPush(
        token=config.ROCKET_TOKEN,
        user_id=config.ROCKET_USER_ID,
        channel=config.ROCKET_CHANNEL
    )
    
    # 获取用户频道列表
    print("\n🔍 获取用户频道列表...")
    rocket.get_user_channels()
    
    # 测试消息
    test_message = """
🌅 测试消息
📅 2024年1月1日

这是一条测试消息，用于验证Rocket推送功能是否正常。
"""
    
    print("\n发送测试消息...")
    success = rocket.send_message(test_message)
    
    if success:
        print("✅ 测试消息发送成功！")
    else:
        print("❌ 测试消息发送失败！")
    
    print("\n💡 注意：")
    print("1. 请确保Rocket服务器地址正确")
    print("2. 请确保令牌和用户ID有效")
    print("3. 请确保频道'每日黄历'存在")
