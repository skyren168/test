#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信接口验证服务器
用于通过测试号接口配置验证
"""

from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/wechat', methods=['GET', 'POST'])
def wechat_verify():
    """微信接口验证和处理"""
    if request.method == 'GET':
        # 微信验证请求
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        
        # 这里应该验证签名，但为了简化，直接返回echostr
        print(f"微信验证请求: signature={signature}, timestamp={timestamp}")
        return echostr
    
    elif request.method == 'POST':
        # 处理微信消息
        print("收到微信消息:", request.data)
        return "success"

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='微信接口验证服务器')
    parser.add_argument('--port', type=int, default=8080, help='服务器端口 (默认: 8080)')
    args = parser.parse_args()
    
    print("🚀 启动微信验证服务器...")
    print(f"访问地址: http://localhost:{args.port}/wechat")
    print(f"在测试号页面配置URL为: http://your-public-ip:{args.port}/wechat")
    print("使用 Ctrl+C 停止服务器")
    app.run(host='0.0.0.0', port=args.port, debug=False)