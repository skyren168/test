#!/bin/bash

# 小程序版每日信息简报系统启动脚本

echo "🚀 启动小程序版每日信息简报系统"
echo "================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查依赖
if [ ! -f "requirements.txt" ]; then
    echo "❌ 错误: requirements.txt 文件不存在"
    exit 1
fi

echo "📦 检查依赖包..."
pip3 install -r requirements.txt

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "⚠️ 警告: .env 文件不存在，使用默认配置"
    cp .env.miniprogram .env
    echo "✅ 已创建默认配置文件，请编辑 .env 文件配置参数"
fi

# 检查用户openid文件
if [ ! -f "user_openids.txt" ]; then
    echo "⚠️ 警告: user_openids.txt 文件不存在，创建示例文件"
    echo "# 用户openid列表文件" > user_openids.txt
    echo "# 每行一个用户的openid" >> user_openids.txt
    echo "# 以#开头的行是注释" >> user_openids.txt
    echo "" >> user_openids.txt
    echo "# 示例openid（需要替换为实际用户openid）" >> user_openids.txt
    echo "o6_bmjrPTlm6_2sgVt7hMZOPfL2M" >> user_openids.txt
    echo "✅ 已创建用户openid文件，请编辑 user_openids.txt 添加实际用户"
fi

echo ""
echo "🔧 系统配置检查完成"
echo "📋 下一步操作:"
echo "   1. 编辑 .env 文件，配置模板ID"
echo "   2. 编辑 user_openids.txt，添加用户openid"
echo "   3. 运行系统"
echo ""

# 询问是否立即启动
read -p "是否立即启动系统? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 启动系统中..."
    python3 daily_briefing_miniprogram.py
else
    echo "💡 您可以稍后手动运行: python3 daily_briefing_miniprogram.py"
fi