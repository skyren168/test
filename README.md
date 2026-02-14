# 🚀 每日信息简报系统

## 📋 项目概述

一个自动化的每日信息简报系统，为用户提供北京地区的天气、生活指数、黄历和尾号限行信息。

**支持的推送方式：**
- 📱 **微信小程序** - 订阅消息推送
- 🚀 **Rocket** - 团队协作平台推送

**推送时间：** 每天上午8:00

## 🎯 功能特点

### 🌤️ 天气信息
- 实时温度
- 天气状况
- 湿度
- 风力

### 📊 生活指数
- 穿衣指数
- 紫外线指数
- 空气质量指数

### 📅 今日黄历
- 农历日期
- 宜做事项
- 忌做事项

### 🚗 尾号限行
- 当日限行尾号
- 限行时间
- 限行区域

### ✨ 星座运势
- 今日星座
- 整体运势
- 爱情运势
- 事业运势
- 财运运势
- 健康运势

### 🧘 易经智慧
- 今日卦象
- 卦象寓意
- 幸运数字
- 幸运颜色

## 🚀 快速开始

### 方法1：使用Rocket推送（推荐）

**配置说明：**
- 个人访问令牌：`qxxUtal9ejPn5IRnM-VxISCjsfd-XJCDGsFTF6EwARC`
- 用户ID：`mkvGvyyAjT5x4d8xt`
- 推送频道：`每日黄历`

**启动方式：**
```bash
# 启动Rocket版系统
chmod +x start_rocket.sh
./start_rocket.sh
```

### 方法2：使用微信小程序推送

**配置说明：**
- 参考 `MINI_PROGRAM_CONFIG_GUIDE.md`

**启动方式：**
```bash
# 启动小程序版系统
chmod +x start_miniprogram.sh
./start_miniprogram.sh
```

## 📁 项目结构

```
.
├── daily_briefing_rocket.py        # Rocket版主程序
├── daily_briefing_miniprogram.py    # 小程序版主程序
├── rocket_push.py                  # Rocket推送模块
├── miniprogram_push.py             # 微信小程序推送模块
├── miniprogram_config.py           # 微信小程序配置
├── image_generator.py              # 图片生成模块
├── start_rocket.sh                 # Rocket版启动脚本
├── start_miniprogram.sh            # 小程序版启动脚本
├── requirements.txt                # Python依赖
├── vercel_deployment/              # Vercel部署文件
└── 各种工具和指南文件
```

## 🔧 系统配置

### Rocket配置

在 `rocket_push.py` 中配置：

```python
class RocketConfig:
    # Rocket配置
    ROCKET_TOKEN = "qxxUtal9ejPn5IRnM-VxISCjsfd-XJCDGsFTF6EwARC"
    ROCKET_USER_ID = "mkvGvyyAjT5x4d8xt"
    ROCKET_CHANNEL = "每日黄历"
    ROCKET_SERVER_URL = "https://rocket.example.com/api/v1"  # 替换为实际地址
```

### 微信小程序配置

在 `miniprogram_config.py` 中配置：

```python
class MiniprogramConfig:
    # 小程序基本配置
    APP_ID = "your_app_id"  # 替换为实际的AppID
    APP_SECRET = "your_app_secret"  # 替换为实际的AppSecret
    TEMPLATE_ID = "your_template_id"  # 替换为实际的订阅消息模板ID
    
    # 推送配置
    SUBSCRIBE_USERS = ["user_openid_1", "user_openid_2"]  # 订阅用户的openid列表
    SCHEDULE_TIME = "08:00"  # 推送时间（每天早上8点）
```

**如何获取配置信息：**
1. **APP_ID 和 APP_SECRET**：
   - 登录微信公众平台 (https://mp.weixin.qq.com/)
   - 进入小程序管理后台
   - 在 "开发" -> "开发设置" 中查看

2. **TEMPLATE_ID（订阅消息模板ID）**：
   - 登录微信公众平台
   - 进入小程序管理后台
   - 在 "功能" -> "订阅消息" 中选择模板
   - 或申请新的模板
   - 建议使用包含以下字段的模板：
     - 日期：date.DATE
     - 天气：thing.THING
     - 温度：thing.THING
     - 穿衣建议：thing.THING
     - 农历：thing.THING
     - 宜：thing.THING
     - 忌：thing.THING
     - 限行：thing.THING
     - 星座：thing.THING
     - 运势：thing.THING
     - 卦象：thing.THING
     - 幸运数字：thing.THING

3. **SUBSCRIBE_USERS（用户openid列表）**：
   - 通过小程序的wx.login()获取code
   - 调用微信登录凭证校验接口获取openid
   - 将用户的openid添加到列表中

### 推送时间配置

默认推送时间为每天上午8:00，可在对应主程序中修改：

```python
# Rocket版
schedule.every().day.at("08:00").do(self.daily_task)

# 小程序版
SCHEDULE_TIME = "08:00"  # 在miniprogram_config.py中
```

## 📦 依赖安装

```bash
# 安装Python依赖
pip3 install -r requirements.txt
```

## 🎉 系统功能验证

### 测试Rocket推送

```bash
# 运行测试
python3 rocket_push.py
```

### 测试微信小程序推送

```bash
# 运行测试
python3 miniprogram_push.py
```

### 测试完整功能

```bash
# 运行Rocket版系统
python3 daily_briefing_rocket.py

# 运行小程序版系统
python3 daily_briefing_miniprogram.py
```

## 💡 注意事项

### Rocket推送
- 需要配置正确的Rocket服务器地址
- 确保令牌和用户ID有效
- 确保"每日黄历"频道存在

### 微信小程序推送
- **配置要求**：需要正确配置APP_ID、APP_SECRET和TEMPLATE_ID
- **用户授权**：用户需要在小程序中授权订阅消息
- **模板创建**：需要在微信公众平台创建包含相应字段的订阅消息模板
- **openid获取**：需要通过小程序登录获取用户的openid
- **API权限**：需要确保小程序已经开通订阅消息权限
- **发送限制**：微信对订阅消息有发送频率限制，请勿频繁测试
- **网络要求**：需要能够访问微信API接口

### 通用注意事项
- 确保Python环境为3.7或更高版本
- 确保安装了所有必要的依赖包
- 确保系统时间正确（影响定时任务执行）
- 建议在测试环境中先验证功能

## 🚀 部署方案

### 本地部署

```bash
# 运行Rocket版系统
./start_rocket.sh  # Rocket推送

# 运行小程序版系统
./start_miniprogram.sh  # 微信小程序推送

# 同时运行两个版本
# 打开两个终端分别执行上述命令
```

### 云平台部署

**使用Vercel（免费）：**
- 参考 `vercel_deployment/README.md`

**使用Docker：**
- 可创建Dockerfile进行容器化部署

## 📝 版本历史

- **v1.0** - 初始版本（微信小程序推送）
- **v2.0** - 添加Rocket推送支持
- **v2.1** - 优化消息格式，调整推送时间为8:00
- **v2.2** - 添加星座运势和易经智慧内容
- **v3.0** - 重构微信小程序推送功能，完善配置系统

## 🎯 系统状态

✅ **核心功能全部正常**
- 天气信息获取
- 生活指数获取
- 黄历信息获取
- 尾号限行获取
- 星座运势获取
- 易经智慧获取
- 消息格式化
- 定时任务调度

✅ **推送功能**
- Rocket推送（已配置）
- 微信小程序推送（可选）

---

**系统已经准备就绪，等待您的启动！** 🎉
