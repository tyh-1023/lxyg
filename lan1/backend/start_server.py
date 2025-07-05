#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝心易购后端服务器启动脚本
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ Python版本过低，需要Python 3.7或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python版本检查通过: {sys.version}")
    return True

def install_requirements():
    """安装依赖包"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    if not requirements_file.exists():
        print("❌ requirements.txt文件不存在")
        return False
    
    print("📦 正在安装依赖包...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 依赖包安装成功")
            return True
        else:
            print(f"❌ 依赖包安装失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 安装依赖包时出错: {e}")
        return False

def check_config():
    """检查配置文件"""
    config_file = Path(__file__).parent / "config.py"
    if not config_file.exists():
        print("❌ config.py配置文件不存在")
        return False
    
    try:
        from config import get_lixin_config
        config = get_lixin_config()
        app_id = config.get('APP_ID', '')
        app_key = config.get('APP_KEY', '')
        
        if app_id == 'your_app_id_here' or app_key == 'your_app_key_here':
            print("⚠️  警告: 请先在config.py中配置正确的APP_ID和APP_KEY")
            print("   或者设置环境变量LIXIN_APP_ID和LIXIN_APP_KEY")
        else:
            print("✅ 配置文件检查通过")
        
        return True
    except Exception as e:
        print(f"❌ 配置文件检查失败: {e}")
        return False

def start_server():
    """启动Flask服务器"""
    print("🚀 正在启动蓝心易购后端服务器...")
    
    # 设置环境变量
    os.environ.setdefault('FLASK_APP', 'app.py')
    os.environ.setdefault('FLASK_ENV', 'development')
    
    try:
        # 启动Flask服务器
        result = subprocess.run([
            sys.executable, "-m", "flask", "run", 
            "--host=0.0.0.0", 
            "--port=5000",
            "--debug"
        ])
        
        if result.returncode != 0:
            print("❌ 服务器启动失败")
            return False
            
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
        return True
    except Exception as e:
        print(f"❌ 启动服务器时出错: {e}")
        return False

def show_help():
    """显示帮助信息"""
    print("蓝心易购后端服务器启动脚本")
    print("=" * 50)
    print("用法:")
    print("  python start_server.py          # 启动服务器")
    print("  python start_server.py --help   # 显示帮助")
    print("  python start_server.py --check  # 仅检查环境")
    print("  python start_server.py --install # 仅安装依赖")
    print("\n环境要求:")
    print("  - Python 3.7+")
    print("  - 网络连接（用于安装依赖）")
    print("  - 蓝心大模型API配置")
    print("\n配置说明:")
    print("  1. 编辑 config.py 文件")
    print("  2. 或设置环境变量:")
    print("     LIXIN_APP_ID=你的AppID")
    print("     LIXIN_APP_KEY=你的AppKEY")
    print("\nAPI文档:")
    print("  - 主页: http://localhost:5000")
    print("  - 差评分析: GET /api/ai/analyze")
    print("  - 商品推荐: GET /api/ai/recommend")
    print("  - 价格分析: GET /api/ai/price")
    print("  - AI对话: POST /api/ai/chat")
    print("  - 京东差评: GET /api/reviews/jd")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            show_help()
            return
        elif sys.argv[1] == "--check":
            print("🔍 环境检查模式")
            check_python_version()
            check_config()
            return
        elif sys.argv[1] == "--install":
            print("📦 依赖安装模式")
            install_requirements()
            return
    
    print("🔍 开始环境检查...")
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 检查配置文件
    if not check_config():
        return
    
    # 安装依赖
    if not install_requirements():
        print("是否继续启动服务器？(y/N): ", end="")
        if input().lower() != 'y':
            return
    
    print("\n" + "=" * 50)
    print("🎉 环境检查完成，准备启动服务器")
    print("=" * 50)
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main() 