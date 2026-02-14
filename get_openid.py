#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取微信小程序用户openid的脚本
"""

import requests
import sys

def get_openid(code):
    """根据code获取openid"""
    app_id = "wx53d1fc369b492f98"
    app_secret = "7a78c0da7c1add7ea95146a11416caff"
    
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": app_id,
        "secret": app_secret,
        "js_code": code,
        "grant_type": "authorization_code"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python3 get_openid.py <code>")
        sys.exit(1)
    
    code = sys.argv[1]
    result = get_openid(code)
    print("响应结果:", result)
    
    if "openid" in result:
        print("✅ 获取成功！")
        print(f"openid: {result['openid']}")
        print(f"建议更新配置: SUBSCRIBE_USERS = ['{result['openid']}']")
    else:
        print("❌ 获取失败！")
        print(f"错误: {result.get('errmsg', '未知错误')}")
