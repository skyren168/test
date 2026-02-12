#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户授权状态检查工具
用于检查用户是否已授权订阅消息
"""

import requests
from miniprogram_config import MiniProgramConfig

def check_user_authorization():
    """检查用户授权状态"""
    config = MiniProgramConfig()
    
    print("🔍 用户授权状态检查工具")
    print("=" * 50)
    
    # 获取Access Token
    url = f"{config.ACCESS_TOKEN_URL}?grant_type=client_credential&appid={config.MINI_PROGRAM_APP_ID}&secret={config.MINI_PROGRAM_APP_SECRET}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                access_token = data['access_token']
                print("✅ Access Token获取成功")
            else:
                print("❌ Access Token获取失败")
                print(f"错误信息: {data}")
                return
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return
    
    # 读取用户openid
    try:
        with open('user_openids.txt', 'r', encoding='utf-8') as f:
            openids = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("❌ 用户openid文件不存在")
        return
    
    if not openids:
        print("❌ 未找到用户openid")
        return
    
    print(f"📋 检查 {len(openids)} 个用户的授权状态...\n")
    
    for i, openid in enumerate(openids, 1):
        print(f"[{i}/{len(openids)}] 用户 {openid[:8]}...")
        
        # 尝试发送测试消息检查授权状态
        test_data = {
            "touser": openid,
            "template_id": config.MINI_PROGRAM_TEMPLATE_ID,
            "page": "pages/index/index",
            "data": {
                "thing1": {"value": "授权测试"},
                "date2": {"value": "2024-01-01"},
                "thing3": {"value": "测试消息"}
            }
        }
        
        send_url = f"https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={access_token}"
        
        try:
            response = requests.post(send_url, json=test_data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                errcode = result.get('errcode', -1)
                
                if errcode == 0:
                    print("   ✅ 授权成功 - 可以接收消息")
                elif errcode == 43101:
                    print("   ❌ 用户未授权订阅消息")
                    print("   💡 需要用户授权后才能接收消息")
                elif errcode == 48001:
                    print("   ⚠️ API未授权 (接口配置问题)")
                    print("   💡 请检查测试号接口配置")
                elif errcode == 40003:
                    print("   ❌ 无效openid")
                    print("   💡 请检查openid是否正确")
                else:
                    print(f"   ❓ 其他错误: {result}")
            else:
                print(f"   ❌ HTTP请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
    
    print(f"\n🎯 授权状态总结:")
    print("• 如果显示'授权成功' → ✅ 用户可以接收消息")
    print("• 如果显示'用户未授权' → ❌ 需要用户授权")
    print("• 如果显示'API未授权' → ⚠️ 检查接口配置")
    
    print(f"\n💡 授权操作指南:")
    print("1. 关注测试号 (扫描测试号二维码)")
    print("2. 在测试号页面发送测试消息")
    print("3. 用户点击消息并授权")
    print("4. 重新运行此工具检查授权状态")

def main():
    check_user_authorization()

if __name__ == "__main__":
    main()