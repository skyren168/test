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
├── miniprogram_config.py           # 小程序配置
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

### 测试完整功能

```bash
# 运行Rocket版系统
python3 daily_briefing_rocket.py
```

## 💡 注意事项

### Rocket推送
- 需要配置正确的Rocket服务器地址
- 确保令牌和用户ID有效
- 确保"每日黄历"频道存在

### 微信小程序推送
- 需要完成接口验证
- 需要用户授权订阅消息
- 需要正确的模板ID

## 🚀 部署方案

### 本地部署

```bash
# 直接运行
./start_rocket.sh  # Rocket版
# 或
./start_miniprogram.sh  # 小程序版
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

## 🎯 系统状态

✅ **核心功能全部正常**
- 天气信息获取
- 生活指数获取
- 黄历信息获取
- 尾号限行获取
- 消息格式化
- 定时任务调度

✅ **推送功能**
- Rocket推送（已配置）
- 微信小程序推送（可选）

---

**系统已经准备就绪，等待您的启动！** 🎉