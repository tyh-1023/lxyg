#!/bin/bash

# 蓝心易购后端服务器启动脚本

echo "========================================"
echo "           蓝心易购后端服务器"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.7+"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "macOS: brew install python3"
    exit 1
fi

# 切换到脚本目录
cd "$(dirname "$0")"

# 检查Python版本
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ 错误: Python版本过低，需要Python 3.7+"
    echo "当前版本: $python_version"
    exit 1
fi

echo "✅ Python版本检查通过: $python_version"
echo

# 启动服务器
echo "🚀 正在启动服务器..."
echo
echo "服务器地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务器"
echo

python3 start_server.py

echo
echo "🛑 服务器已停止" 