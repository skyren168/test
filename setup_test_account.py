#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试号快速配置工具
"""

import os

def setup_test_account():
    print("🚀 微信测试号快速配置工具")
    print("=" * 50)
    
    print("📋 使用说明:")
    print("1. 访问: https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login")
    print("2. 微信扫码登录")
    print("3. 获取测试号appID和appsecret")
    print("")
    
    # 获取用户输入的测试号信息
    app_id = input("请输入测试号appID: ").strip()
    app_secret = input("请输入测试号appsecret: ").strip()
    
    if not app_id or not app_secret:
        print("❌ 输入信息不完整")
        return
    
    # 创建测试号配置文件
    config_content = f"""# 微信测试号配置
MINI_PROGRAM_APP_ID={app_id}
MINI_PROGRAM_APP_SECRET={app_secret}
MINI_PROGRAM_TEMPLATE_ID=hh-rt2ihhh-rMUhhbrAapOOy5vfrju-trIkRFRJvfrc

# 日志配置
LOG_LEVEL=DEBUG
"""
    
    with open('.env.test.account', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("\n✅ 测试号配置文件已创建: .env.test.account")
    
    # 询问是否设置为当前配置
    choice = input("\n是否设置为当前使用配置? (y/n): ").strip().lower()
    if choice == 'y':
        os.system('cp .env.test.account .env')
        print("✅ 已设置为当前配置")
    
    print("\n📋 下一步操作:")
    print("1. 扫描测试号二维码关注公众号")
    print("2. 在测试号页面获取您的openid")
    print("3. 使用以下命令添加openid:")
    print("   python3 add_openids.py 您的openid")
    print("4. 启动系统测试:")
    print("   python3 daily_briefing_miniprogram.py")
    
    # 询问是否立即添加测试openid
    test_openid = input("\n是否添加测试openid? (输入openid或直接回车跳过): ").strip()
    if test_openid:
        os.system(f'python3 add_openids.py {test_openid}')
        print("✅ 测试openid已添加")

if __name__ == "__main__":
    setup_test_account()