#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
openid验证工具
"""

import requests
from miniprogram_config import MiniProgramConfig

def verify_openid(openid, config):
    """验证单个openid是否有效"""
    access_token = get_access_token(config)
    if not access_token:
        return False, "无法获取Access Token"
    
    # 构建测试消息
    test_data = {
        "thing1": {"value": "测试消息"},
        "date2": {"value": "2024-01-01"},
        "thing3": {"value": "测试"}
    }
    
    template_data = {
        "touser": openid,
        "template_id": config.MINI_PROGRAM_TEMPLATE_ID,
        "page": "pages/index/index",
        "data": test_data
    }
    
    url = f"https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={access_token}"
    
    try:
        response = requests.post(url, json=template_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            errcode = result.get('errcode', -1)
            
            if errcode == 0:
                return True, "有效"
            elif errcode == 40003:
                return False, "无效openid"
            elif errcode == 43101:
                return False, "用户未授权"
            else:
                return False, f"其他错误: {result}"
    except Exception as e:
        return False, f"请求异常: {e}"
    
    return False, "未知错误"

def get_access_token(config):
    """获取Access Token"""
    url = f"{config.ACCESS_TOKEN_URL}?grant_type=client_credential&appid={config.MINI_PROGRAM_APP_ID}&secret={config.MINI_PROGRAM_APP_SECRET}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token', '')
    except:
        pass
    
    return ""

def main():
    print("🔍 openid验证工具")
    print("=" * 50)
    
    config = MiniProgramConfig()
    
    # 读取openid文件
    try:
        with open('user_openids.txt', 'r', encoding='utf-8') as f:
            openids = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("❌ user_openids.txt 文件不存在")
        return
    
    if not openids:
        print("❌ 未找到任何openid")
        return
    
    print(f"📋 开始验证 {len(openids)} 个openid...\n")
    
    valid_count = 0
    for i, openid in enumerate(openids, 1):
        print(f"[{i}/{len(openids)}] 验证 {openid[:8]}...", end=" ")
        
        is_valid, message = verify_openid(openid, config)
        
        if is_valid:
            print("✅ 有效")
            valid_count += 1
        else:
            print(f"❌ {message}")
    
    print(f"\n📊 验证结果: {valid_count}/{len(openids)} 个有效openid")

if __name__ == "__main__":
    main()