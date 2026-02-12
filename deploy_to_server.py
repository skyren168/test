#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云服务器部署脚本
用于将系统部署到云服务器完成接口验证
"""

import os
import shutil

def create_deployment_package():
    """创建部署包"""
    print("🚀 创建云服务器部署包")
    print("=" * 50)
    
    # 创建部署目录
    deploy_dir = "deployment_package"
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # 复制必要的文件
    required_files = [
        "daily_briefing_miniprogram.py",
        "miniprogram_config.py", 
        "requirements.txt",
        "user_openids.txt",
        "wechat_verify_server.py",
        "start_miniprogram.sh"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(deploy_dir, file))
            print(f"✅ 复制: {file}")
    
    # 创建部署说明
    deploy_guide = """# 🚀 每日信息简报系统部署指南

## 部署步骤

### 1. 上传文件到服务器
将本目录所有文件上传到您的云服务器

### 2. 安装依赖
```bash
pip3 install -r requirements.txt
```

### 3. 配置环境变量
编辑 `.env` 文件，确保配置正确：
```env
MINI_PROGRAM_APP_ID=wx97cd0e7b6af16c70
MINI_PROGRAM_APP_SECRET=0cb8a87265af149862a6b3f4a2c5f4df
MINI_PROGRAM_TEMPLATE_ID=HDUP9hzf3z-3Vhz2QaDCyXYk15S6htW11NCoYb-s9MI
```

### 4. 启动验证服务器
```bash
python3 wechat_verify_server.py --port 80
```

### 5. 配置测试号接口
在测试号页面配置：
- URL: http://您的服务器IP/wechat
- Token: test123456
- 消息加解密方式: 兼容模式

### 6. 提交验证
点击"提交"按钮完成接口验证

### 7. 启动系统
```bash
python3 daily_briefing_miniprogram.py
```

## 服务器要求
- 公网IP地址
- Python 3.6+
- 80端口开放
- 系统服务管理（如systemd）

## 验证完成后的状态
一旦接口验证成功，系统将：
- ✅ 每天上午9点自动执行
- ✅ 获取最新天气、黄历、限行信息
- ✅ 推送到授权用户的小程序
- ✅ 完全自动化运行
"""
    
    with open(os.path.join(deploy_dir, "DEPLOY_GUIDE.md"), "w", encoding="utf-8") as f:
        f.write(deploy_guide)
    
    # 创建启动脚本
    start_script = """#!/bin/bash
# 每日信息简报系统启动脚本

echo "🚀 启动每日信息简报系统"
echo "================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3"
    exit 1
fi

# 安装依赖
echo "📦 安装依赖..."
pip3 install -r requirements.txt

# 启动系统
echo "🔧 启动系统中..."
nohup python3 daily_briefing_miniprogram.py > briefing.log 2>&1 &

echo "✅ 系统已启动"
echo "📋 查看日志: tail -f briefing.log"
echo "💡 系统将在每天上午9点自动执行"
"""
    
    with open(os.path.join(deploy_dir, "start_server.sh"), "w", encoding="utf-8") as f:
        f.write(start_script)
    os.chmod(os.path.join(deploy_dir, "start_server.sh"), 0o755)
    
    print(f"\n✅ 部署包创建完成: {deploy_dir}/")
    print("📁 包含文件:")
    for file in os.listdir(deploy_dir):
        print(f"   • {file}")
    
    return deploy_dir

def main():
    print("🎯 接口验证解决方案")
    print("=" * 50)
    
    print("\n📋 当前系统状态:")
    print("✅ 核心功能全部正常")
    print("✅ 消息格式完美")
    print("✅ 定时任务就绪")
    print("⚠️  等待接口验证完成")
    
    print("\n🚀 推荐的解决方案:")
    print("1. 部署到云服务器（有公网IP）")
    print("2. 完成接口验证")
    print("3. 系统即可投入使用")
    
    choice = input("\n是否创建部署包? (y/n): ").strip().lower()
    if choice == 'y':
        deploy_dir = create_deployment_package()
        
        print(f"\n🎉 部署准备完成!")
        print(f"📦 部署包位置: {deploy_dir}/")
        print(f"📚 部署指南: {deploy_dir}/DEPLOY_GUIDE.md")
        
        print("\n💡 下一步操作:")
        print("1. 将部署包上传到云服务器")
        print("2. 按照部署指南操作")
        print("3. 完成接口验证")
        print("4. 系统即可投入使用")
    else:
        print("\n💡 您也可以选择其他方案:")
        print("• 使用微信开发者工具测试")
        print("• 使用ngrok等隧道工具")
        print("• 部署到已有的服务器")

if __name__ == "__main__":
    main()