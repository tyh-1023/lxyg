#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝心易购后端功能测试脚本
测试所有API接口和功能
"""

import requests
import json
import time
from datetime import datetime

# 服务器地址
BASE_URL = "http://localhost:5000"

def test_server_status():
    """测试服务器状态"""
    print("🔍 测试服务器状态...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器运行正常")
            return True
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器已启动")
        return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

def test_ai_analyze():
    """测试AI差评分析"""
    print("\n🔍 测试AI差评分析...")
    reviews = [
        "物流太慢了，等了半个月才到",
        "商品质量不错，但是价格有点贵",
        "客服态度很好，但是商品有瑕疵"
    ]
    
    try:
        response = requests.post(f"{BASE_URL}/api/ai/analyze", 
                               json={"reviews": reviews}, 
                               timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ AI差评分析成功")
            print(f"   - 总结: {result.get('summary', 'N/A')[:50]}...")
            print(f"   - 风险等级: {result.get('risk_level', 'N/A')}")
            return True
        else:
            print(f"❌ AI差评分析失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI差评分析错误: {e}")
        return False

def test_ai_recommend():
    """测试AI商品推荐"""
    print("\n🔍 测试AI商品推荐...")
    preferences = {
        "budget": "2000-3000元",
        "brands": ["华为", "小米"],
        "scenarios": "日常使用"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/ai/recommend", 
                               json={"preferences": preferences}, 
                               timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ AI商品推荐成功")
            print(f"   - 推荐数量: {len(result.get('recommendations', []))}")
            return True
        else:
            print(f"❌ AI商品推荐失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI商品推荐错误: {e}")
        return False

def test_ai_chat():
    """测试AI对话"""
    print("\n🔍 测试AI对话...")
    message = "我想买一个平板电脑，有什么推荐吗？"
    
    try:
        response = requests.post(f"{BASE_URL}/api/ai/chat", 
                               json={"message": message}, 
                               timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ AI对话成功")
            print(f"   - 响应: {result.get('response', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ AI对话失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI对话错误: {e}")
        return False

def test_jd_reviews():
    """测试京东差评爬取"""
    print("\n🔍 测试京东差评爬取...")
    product_id = "100012043978"  # 示例商品ID
    
    try:
        response = requests.get(f"{BASE_URL}/api/reviews/jd?product_id={product_id}&max_count=5", 
                              timeout=30)
        if response.status_code == 200:
            result = response.json()
            reviews = result.get('reviews', [])
            print("✅ 京东差评爬取成功")
            print(f"   - 获取差评数量: {len(reviews)}")
            if reviews:
                print(f"   - 示例差评: {reviews[0].get('content', 'N/A')[:50]}...")
            return True
        else:
            print(f"❌ 京东差评爬取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 京东差评爬取错误: {e}")
        return False

def test_product_list():
    """测试商品列表"""
    print("\n🔍 测试商品列表...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/products", timeout=10)
        if response.status_code == 200:
            result = response.json()
            products = result.get('products', [])
            print("✅ 商品列表获取成功")
            print(f"   - 商品数量: {len(products)}")
            return True
        else:
            print(f"❌ 商品列表获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 商品列表获取错误: {e}")
        return False

def test_product_detail():
    """测试商品详情"""
    print("\n🔍 测试商品详情...")
    product_id = "1"  # 示例商品ID
    
    try:
        response = requests.get(f"{BASE_URL}/api/products/{product_id}", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ 商品详情获取成功")
            print(f"   - 商品名称: {result.get('name', 'N/A')}")
            return True
        else:
            print(f"❌ 商品详情获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 商品详情获取错误: {e}")
        return False

def main():
    """主测试函数"""
    print("蓝心易购后端功能测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 测试结果统计
    total_tests = 7
    passed_tests = 0
    
    # 执行测试
    tests = [
        ("服务器状态", test_server_status),
        ("AI差评分析", test_ai_analyze),
        ("AI商品推荐", test_ai_recommend),
        ("AI对话", test_ai_chat),
        ("京东差评爬取", test_jd_reviews),
        ("商品列表", test_product_list),
        ("商品详情", test_product_detail)
    ]
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    print(f"总测试数: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"失败测试: {total_tests - passed_tests}")
    print(f"通过率: {passed_tests/total_tests*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 所有测试通过！系统运行正常")
    else:
        print(f"\n⚠️  有 {total_tests - passed_tests} 个测试失败，请检查相关功能")
    
    print("\n💡 提示:")
    print("  - 确保服务器已启动: python start_server.py")
    print("  - 检查网络连接")
    print("  - 验证API配置是否正确")

if __name__ == "__main__":
    main() 