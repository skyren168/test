#!/bin/bash
# Rocket版每日信息简报系统启动脚本

echo "🚀 启动Rocket版每日信息简报系统"
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
python3 daily_briefing_rocket.py
