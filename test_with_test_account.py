#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试号一键测试工具
"""

import os
import subprocess
import time

def test_with_test_account():
    print("🧪 测试号一键测试工具")
    print("=" * 50)
    
    # 检查配置文件
    if not os.path.exists('.env.test.account'):
        print("❌ 测试号配置文件不存在")
        print("请先运行: python3 setup_test_account.py")
        return
    
    # 使用测试号配置
    os.system('cp .env.test.account .env')
    print("✅ 已切换到测试号配置")
    
    # 检查用户openid
    try:
        with open('user_openids.txt', 'r', encoding='utf-8') as f:
            openids = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("❌ 用户openid文件不存在")
        print("请先添加测试用户openid")
        return
    
    if not openids:
        print("❌ 未找到任何用户openid")
        print("请先运行: python3 add_openids.py 您的openid")
        return
    
    print(f"📋 找到 {len(openids)} 个测试用户")
    
    # 测试系统（短暂运行）
    print("\n🔧 开始测试系统（运行10秒后自动停止）...")
    
    try:
        # 启动系统进程
        process = subprocess.Popen(['python3', 'daily_briefing_miniprogram.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        # 等待10秒
        time.sleep(10)
        
        # 终止进程
        process.terminate()
        
        # 获取输出
        stdout, stderr = process.communicate(timeout=5)
        
        print("\n📊 测试输出:")
        print("-" * 30)
        
        # 显示关键信息
        lines = stdout.split('\n')
        for line in lines:
            if any(keyword in line for keyword in ['INFO', 'ERROR', 'WARNING', '成功', '失败']):
                print(line)
        
        if stderr:
            print("\n❌ 错误信息:")
            print(stderr)
            
        print("\n✅ 测试完成")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
    
    print("\n💡 测试结果分析:")
    print("• 如果看到 'Access Token获取成功' - ✅ 配置正确")
    print("• 如果看到 '消息数据格式化成功' - ✅ 消息模板正确") 
    print("• 如果看到 '用户未授权' - ⚠️ 需要用户授权")
    print("• 如果看到 '无效openid' - ❌ openid错误")

if __name__ == "__main__":
    test_with_test_account()