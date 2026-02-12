# 🚀 小程序版每日信息简报 - 快速开始指南

## ✅ 系统已创建完成！

您的小程序版每日信息简报系统已经准备就绪！以下是完整的配置和使用说明。

## 📁 项目文件结构

```
├── daily_briefing_miniprogram.py    # 小程序版主程序
├── miniprogram_config.py           # 小程序配置
├── .env                            # 环境变量配置
├── .env.miniprogram                # 环境变量示例
├── user_openids.txt                # 用户openid列表
├── start_miniprogram.sh            # 启动脚本
└── QUICK_START_MINIPROGRAM.md      # 本指南
```

## 🎯 系统功能

- ✅ **北京天气信息**：温度、天气状况、湿度、风力
- ✅ **生活指数**：穿衣、紫外线、洗车、感冒、运动、空气质量
- ✅ **今日黄历**：农历日期、宜忌事项、生肖星宿
- ✅ **尾号限行**：北京地区当日限行尾号、时间、区域
- ✅ **定时推送**：每天上午9点自动执行
- ✅ **小程序订阅消息**：通过微信小程序推送

## 🚀 快速启动（3步完成）

### 步骤1：获取小程序模板ID

1. 登录[微信公众平台](https://mp.weixin.qq.com/)
2. 进入"功能" → "订阅消息"
3. 在模板库搜索以下关键词：
   - **天气提醒**
   - **服务通知**  
   - **日常提醒**
4. 选择模板并获取**模板ID**

### 步骤2：配置模板ID

编辑 `.env` 文件：

```env
# 小程序配置
MINI_PROGRAM_APP_ID=wx53d1fc369b492f98
MINI_PROGRAM_APP_SECRET=df37a8d23ecd22977d5ae4e24e091562
MINI_PROGRAM_TEMPLATE_ID=这里填入您的模板ID

# 日志配置
LOG_LEVEL=INFO
```

### 步骤3：添加用户openid

编辑 `user_openids.txt` 文件，每行一个用户openid：

```
# 用户openid列表
# 每行一个用户的openid

o6_bmjrPTlm6_2sgVt7hMZOPfL2M  # 替换为实际用户openid
o6_bmjrPTlm6_2sgVt7hMZOPfL2N  # 添加更多用户
```

## 💡 如何获取用户openid？

### 方法1：通过小程序获取

在小程序端代码中添加：

```javascript
// 小程序页面代码
wx.login({
  success: (res) => {
    if (res.code) {
      // 将code发送到您的服务器
      wx.request({
        url: 'https://yourserver.com/api/get_openid',
        data: { code: res.code },
        success: (result) => {
          console.log('用户openid:', result.data.openid)
        }
      })
    }
  }
})
```

### 方法2：服务器端代码

创建API接口获取openid：

```python
import requests

def get_openid_by_code(code: str, app_id: str, app_secret: str) -> str:
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={app_id}&secret={app_secret}&js_code={code}&grant_type=authorization_code"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('openid', '')
    return ""
```

## 🏃‍♂️ 启动系统

### 方法1：使用启动脚本（推荐）

```bash
# 给脚本执行权限
chmod +x start_miniprogram.sh

# 运行启动脚本
./start_miniprogram.sh
```

### 方法2：手动启动

```bash
# 安装依赖
pip3 install -r requirements.txt

# 启动系统
python3 daily_briefing_miniprogram.py
```

## 📊 系统运行效果

启动后系统会显示：

```
🚀 启动小程序版每日信息简报系统
================================
📦 检查依赖包...
✅ 依赖安装完成
🔧 系统配置检查完成
📋 下一步操作:
   1. 编辑 .env 文件，配置模板ID
   2. 编辑 user_openids.txt，添加用户openid
   3. 运行系统
```

## 🔧 自定义配置

### 修改推送时间

编辑 `miniprogram_config.py`：

```python
# 定时任务配置
SCHEDULE_TIME = "09:00"  # 修改为其他时间，如 "08:30"
```

### 修改消息模板

在 `daily_briefing_miniprogram.py` 中修改 `format_subscribe_message_data` 方法：

```python
def format_subscribe_message_data(self) -> dict:
    # 根据您选择的模板调整字段名
    return {
        "thing1": {"value": "自定义标题"},
        "date2": {"value": "日期"},
        # ... 其他字段
    }
```

## 🐛 故障排除

### 常见问题

1. **invalid openid 错误**
   - 原因：用户openid无效或格式错误
   - 解决：检查openid是否正确，用户是否授权

2. **模板ID无效**
   - 原因：模板ID配置错误或模板未启用
   - 解决：检查模板ID，确认模板已添加

3. **Access Token获取失败**
   - 原因：AppID或AppSecret错误
   - 解决：检查小程序配置参数

### 查看日志

系统会输出详细日志，帮助诊断问题：

```
2026-02-10 16:39:23,114 - INFO - 找到 1 个用户openid
2026-02-10 16:39:23,394 - ERROR - 订阅消息发送失败: {'errcode': 40003, 'errmsg': 'invalid openid'}
```

## 🔄 从测试到生产

### 测试阶段
1. 使用测试用户openid
2. 配置测试模板
3. 验证消息格式

### 生产部署
1. 获取真实用户openid
2. 配置正式模板
3. 部署到服务器
4. 设置开机自启动

## 📱 小程序端用户授权

用户需要在小程序内授权订阅消息：

```javascript
// 小程序页面代码
wx.requestSubscribeMessage({
  tmplIds: ['您的模板ID'],
  success: (res) => {
    console.log('订阅授权成功')
  },
  fail: (err) => {
    console.log('订阅授权失败', err)
  }
})
```

## 🎉 完成！

按照以上步骤配置完成后，您的每日信息简报系统就可以正常运行了！系统会在每天上午9点自动获取信息并推送到用户的小程序。

如果有任何问题，请查看日志输出或参考微信小程序官方文档。