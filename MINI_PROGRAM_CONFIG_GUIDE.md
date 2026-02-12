# 微信小程序配置指南

您提供的是小程序AppID和AppSecret，小程序与公众号的推送机制不同。小程序主要通过**订阅消息**来实现推送功能。

## 🔄 小程序 vs 公众号的区别

| 特性 | 小程序 | 公众号 |
|------|--------|--------|
| 推送方式 | 订阅消息 | 模板消息 |
| 用户交互 | 需要用户授权 | 用户关注即可 |
| 消息类型 | 一次性订阅/长期订阅 | 模板消息 |
| 使用场景 | 服务通知 | 营销推送 |

## 📋 小程序配置流程

### 1. 确认小程序信息

您已提供：
- **AppID(小程序ID)**: `wx53d1fc369b492f98`
- **AppSecret**: `df37a8d23ecd22977d5ae4e24e091562`

### 2. 创建订阅消息模板

1. 登录[微信公众平台](https://mp.weixin.qq.com/)
2. 进入"功能" → "订阅消息"
3. 选择"公共模板库"或"个人模板库"
4. 搜索合适的模板，如：
   - 天气提醒
   - 服务通知  
   - 日常提醒
5. 添加模板并获取**模板ID**

### 3. 获取用户openid

小程序需要获取用户的openid才能发送消息：

```javascript
// 小程序端代码
wx.login({
  success: (res) => {
    if (res.code) {
      // 将code发送到服务器，换取openid
      wx.request({
        url: 'https://yourserver.com/get_openid',
        data: { code: res.code },
        success: (result) => {
          console.log('openid:', result.data.openid)
        }
      })
    }
  }
})
```

## 🔧 修改系统支持小程序

### 1. 创建小程序专用配置文件

创建 `miniprogram_config.py`：

```python
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
    MINI_PROGRAM_TEMPLATE_ID = os.getenv('MINI_PROGRAM_TEMPLATE_ID', 'your_template_id')
    
    # 订阅消息配置
    SUBSCRIBE_MESSAGE_URL = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send"
    ACCESS_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
```

### 2. 修改主程序支持小程序

创建 `daily_briefing_miniprogram.py`：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序版每日信息简报系统
"""

import requests
import json
import schedule
import time
from datetime import datetime
import logging
from miniprogram_config import MiniProgramConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MiniProgramBriefing:
    def __init__(self, config: MiniProgramConfig):
        self.config = config
        self.access_token = ""
        self.token_expire_time = 0
    
    def get_access_token(self) -> str:
        """获取小程序Access Token"""
        # 检查token是否过期
        if self.access_token and time.time() < self.token_expire_time:
            return self.access_token
            
        url = f"{self.config.ACCESS_TOKEN_URL}?grant_type=client_credential&appid={self.config.MINI_PROGRAM_APP_ID}&secret={self.config.MINI_PROGRAM_APP_SECRET}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.access_token = data['access_token']
                    # token有效期为7200秒，提前5分钟刷新
                    self.token_expire_time = time.time() + 6600
                    logger.info("小程序Access Token获取成功")
                    return self.access_token
                else:
                    logger.error(f"获取Access Token失败: {data}")
        except Exception as e:
            logger.error(f"获取Access Token异常: {e}")
        
        return ""
    
    def send_subscribe_message(self, openid: str, message_data: dict) -> bool:
        """发送订阅消息"""
        access_token = self.get_access_token()
        if not access_token:
            return False
        
        # 构建订阅消息数据
        template_data = {
            "touser": openid,
            "template_id": self.config.MINI_PROGRAM_TEMPLATE_ID,
            "page": "pages/index/index",  # 点击消息跳转的小程序页面
            "data": self.format_message_data(message_data)
        }
        
        url = f"{self.config.SUBSCRIBE_MESSAGE_URL}?access_token={access_token}"
        
        try:
            response = requests.post(url, json=template_data)
            if response.status_code == 200:
                result = response.json()
                if result.get('errcode') == 0:
                    logger.info(f"订阅消息发送成功给用户: {openid}")
                    return True
                else:
                    logger.error(f"订阅消息发送失败: {result}")
        except Exception as e:
            logger.error(f"发送订阅消息异常: {e}")
        
        return False
    
    def format_message_data(self, briefing_data: dict) -> dict:
        """格式化消息数据（根据实际模板调整）"""
        return {
            "thing1": {
                "value": "每日信息简报"
            },
            "date2": {
                "value": datetime.now().strftime("%Y年%m月%d日")
            },
            "thing3": {
                "value": briefing_data.get('weather', 'N/A')
            },
            "thing4": {
                "value": briefing_data.get('traffic', 'N/A')
            }
        }
    
    def get_briefing_data(self) -> dict:
        """获取简报数据（复用原有逻辑）"""
        # 这里可以复用之前公众号版本的天气、黄历等数据获取逻辑
        from daily_briefing import DailyBriefing
        
        # 创建临时实例获取数据
        temp_briefing = DailyBriefing({})
        
        return {
            'weather': f"{temp_briefing.get_weather_info().get('weather', 'N/A')} {temp_briefing.get_weather_info().get('temperature', 'N/A')}",
            'traffic': f"限行尾号: {', '.join(map(str, temp_briefing.get_traffic_restriction().get('restricted_numbers', []))) if temp_briefing.get_traffic_restriction().get('restricted_numbers') else '不限行'}",
            'almanac': temp_briefing.get_almanac().get('suitable', 'N/A'),
            'life_index': temp_briefing.get_life_index().get('dressing', 'N/A')
        }
    
    def get_user_openids(self) -> list:
        """获取需要发送消息的用户openid列表"""
        # 这里需要您实现获取用户openid的逻辑
        # 可以从数据库、文件或API获取
        
        # 示例：从文件读取用户openid列表
        try:
            with open('user_openids.txt', 'r') as f:
                openids = [line.strip() for line in f if line.strip()]
                return openids
        except FileNotFoundError:
            logger.warning("用户openid文件不存在，请创建user_openids.txt")
            return []
    
    def daily_task(self):
        """每日任务"""
        logger.info("开始执行小程序版每日信息简报")
        
        # 获取简报数据
        briefing_data = self.get_briefing_data()
        
        # 获取用户列表
        user_openids = self.get_user_openids()
        
        if not user_openids:
            logger.warning("没有找到需要发送消息的用户")
            return
        
        success_count = 0
        for openid in user_openids:
            if self.send_subscribe_message(openid, briefing_data):
                success_count += 1
        
        logger.info(f"消息发送完成: 成功{success_count}个，失败{len(user_openids) - success_count}个")
    
    def run_scheduler(self):
        """启动定时任务"""
        logger.info("启动小程序版每日信息简报定时任务")
        
        # 每天上午9点执行
        schedule.every().day.at("09:00").do(self.daily_task)
        
        # 立即执行一次测试
        self.daily_task()
        
        while True:
            schedule.run_pending()
            time.sleep(60)

def main():
    """主函数"""
    config = MiniProgramConfig()
    briefing_system = MiniProgramBriefing(config)
    briefing_system.run_scheduler()

if __name__ == "__main__":
    main()
```

### 3. 创建环境配置文件

创建 `.env.miniprogram`：

```env
# 小程序配置
MINI_PROGRAM_APP_ID=wx53d1fc369b492f98
MINI_PROGRAM_APP_SECRET=df37a8d23ecd22977d5ae4e24e091562
MINI_PROGRAM_TEMPLATE_ID=your_template_id_here

# 天气API配置（可选）
WEATHER_API_KEY=your_weather_api_key

# 日志配置
LOG_LEVEL=INFO
```

## 📱 小程序端用户授权

### 1. 小程序端订阅消息授权

在小程序页面中添加订阅消息授权：

```javascript
// 小程序页面代码
Page({
  // 请求订阅消息授权
  requestSubscribeMessage: function() {
    wx.requestSubscribeMessage({
      tmplIds: ['您的模板ID'], // 替换为实际模板ID
      success: (res) => {
        console.log('订阅消息授权成功', res)
        // 将用户openid和订阅状态发送到服务器
        this.sendUserInfo()
      },
      fail: (err) => {
        console.log('订阅消息授权失败', err)
      }
    })
  },
  
  // 发送用户信息到服务器
  sendUserInfo: function() {
    wx.login({
      success: (loginRes) => {
        if (loginRes.code) {
          wx.request({
            url: 'https://yourserver.com/api/user/subscribe',
            method: 'POST',
            data: {
              code: loginRes.code,
              subscribe: true
            },
            success: (result) => {
              console.log('用户订阅信息保存成功')
            }
          })
        }
      }
    })
  }
})
```

### 2. 服务器端用户管理

创建用户管理API：

```python
# user_management.py
import requests

def get_user_openid(code: str, app_id: str, app_secret: str) -> str:
    """通过code获取用户openid"""
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={app_id}&secret={app_secret}&js_code={code}&grant_type=authorization_code"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('openid', '')
    return ""

def save_user_subscription(openid: str, template_id: str):
    """保存用户订阅信息"""
    # 将用户openid和模板ID保存到数据库或文件
    with open('subscribed_users.txt', 'a') as f:
        f.write(f"{openid},{template_id}\n")
```

## 🚀 部署步骤

### 1. 配置环境

```bash
# 复制配置文件
cp .env.miniprogram .env

# 安装依赖
pip install -r requirements.txt
```

### 2. 获取模板ID

1. 登录微信公众平台
2. 进入"功能" → "订阅消息"
3. 选择模板并获取模板ID
4. 更新 `.env` 文件中的 `MINI_PROGRAM_TEMPLATE_ID`

### 3. 收集用户openid

创建 `user_openids.txt` 文件，每行一个用户openid：

```
o6_bmjrPTlm6_2sgVt7hMZOPfL2M
 o6_bmjrPTlm6_2sgVt7hMZOPfL2N
 o6_bmjrPTlm6_2sgVt7hMZOPfL2O
```

### 4. 启动系统

```bash
python daily_briefing_miniprogram.py
```

## ⚠️ 重要注意事项

### 1. 订阅消息限制

- 用户需要**主动授权**才能接收消息
- 每个模板有**发送次数限制**
- 消息有**有效期**（通常7天）

### 2. 用户openid管理

- openid是用户的唯一标识
- 需要妥善保管用户openid
- 定期清理无效的openid

### 3. 安全考虑

- 保护AppSecret安全
- 使用HTTPS传输数据
- 定期更换Access Token

## 🔄 从公众号切换到小程序

如果您决定使用小程序方案：

1. **停止公众号版本**（如果已运行）
2. **配置小程序环境**（按照上述步骤）
3. **获取用户授权**（通过小程序界面）
4. **启动小程序版本**

## 📞 技术支持

如果在配置过程中遇到问题：

1. 查看微信官方文档：[小程序开发文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
2. 检查服务器日志
3. 验证Access Token获取
4. 测试单个用户消息发送

通过以上配置，您就可以使用小程序来实现每日信息简报的推送功能了！