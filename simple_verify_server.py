#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的微信接口验证服务器
使用Python内置的http.server
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

class WechatVerifyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理微信验证请求"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/wechat':
            # 微信接口验证
            query_params = parse_qs(parsed_path.query)
            
            signature = query_params.get('signature', [''])[0]
            timestamp = query_params.get('timestamp', [''])[0]
            nonce = query_params.get('nonce', [''])[0]
            echostr = query_params.get('echostr', [''])[0]
            
            print(f"📨 收到微信验证请求:")
            print(f"   Signature: {signature}")
            print(f"   Timestamp: {timestamp}")
            print(f"   Nonce: {nonce}")
            print(f"   Echostr: {echostr}")
            
            # 返回echostr完成验证
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(echostr.encode('utf-8'))
            
            print("✅ 验证请求已响应")
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """处理微信消息"""
        if self.path == '/wechat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            print("📨 收到微信消息:", post_data.decode('utf-8'))
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'success')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"🌐 {self.address_string()} - {format % args}")

def run_server(port=8080):
    """启动服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, WechatVerifyHandler)
    
    print("🚀 启动微信接口验证服务器")
    print(f"📡 服务器运行在: http://localhost:{port}")
    print(f"🔗 微信验证URL: http://localhost:{port}/wechat")
    print("⏹️  使用 Ctrl+C 停止服务器")
    print("-" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")

if __name__ == "__main__":
    import sys
    
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ 端口号必须是数字")
            sys.exit(1)
    
    run_server(port)