from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import logging
from datetime import datetime

# 添加模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crawler.review_spider import get_negative_reviews
from lixin_ai.lixin_api import (
    analyze_reviews, 
    get_product_recommendation, 
    analyze_price_trend,
    lixin_ai
)
from recommender.recommend import get_recommendations
from crawler.negative_reviews import fetch_jd_negative_reviews

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/api/hello')
def hello():
    """健康检查接口"""
    return jsonify({
        "msg": "蓝心易购后端已启动",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/review')
def get_reviews():
    """获取商品差评"""
    try:
        product = request.args.get('product', 'Redmi Pad')
        reviews = get_negative_reviews(product)
        
        logger.info(f"获取商品差评: {product}, 数量: {len(reviews)}")
        
        return jsonify({
            "success": True,
            "product": product,
            "reviews": reviews,
            "count": len(reviews),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"获取差评失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/ai_analyze', methods=['POST'])
def ai_analyze():
    """AI分析差评"""
    try:
        data = request.get_json()
        reviews = data.get('reviews', [])
        
        if not reviews:
            return jsonify({
                "success": False,
                "error": "没有提供差评数据"
            }), 400
        
        logger.info(f"开始AI分析，差评数量: {len(reviews)}")
        
        # 调用蓝心大模型分析
        analysis = analyze_reviews(reviews)
        
        logger.info("AI分析完成")
        
        return jsonify({
            "success": True,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"AI分析失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/ai_recommend', methods=['POST'])
def ai_recommend():
    """AI智能推荐"""
    try:
        data = request.get_json()
        user_preferences = data.get('preferences', {})
        
        logger.info(f"开始AI推荐，用户偏好: {user_preferences}")
        
        # 调用蓝心大模型推荐
        recommendations = get_product_recommendation(user_preferences)
        
        logger.info("AI推荐完成")
        
        return jsonify({
            "success": True,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"AI推荐失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/price_analysis', methods=['POST'])
def price_analysis():
    """价格走势分析"""
    try:
        data = request.get_json()
        product_name = data.get('product_name', '')
        price_history = data.get('price_history', [])
        
        if not product_name:
            return jsonify({
                "success": False,
                "error": "没有提供商品名称"
            }), 400
        
        logger.info(f"开始价格分析: {product_name}")
        
        # 调用蓝心大模型分析价格走势
        analysis = analyze_price_trend(product_name, price_history)
        
        logger.info("价格分析完成")
        
        return jsonify({
            "success": True,
            "product_name": product_name,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"价格分析失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """与AI对话"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', [])
        
        if not message:
            return jsonify({
                "success": False,
                "error": "没有提供消息内容"
            }), 400
        
        logger.info(f"AI对话: {message[:50]}...")
        
        # 构建对话消息
        messages = []
        if context:
            messages.extend(context)
        
        messages.append({"role": "user", "content": message})
        
        # 调用蓝心大模型
        result = lixin_ai._call_api(messages)
        
        if "error" in result:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 500
        
        # 解析回复
        if "choices" in result and len(result["choices"]) > 0:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = "抱歉，我现在无法回答您的问题。"
        
        logger.info("AI对话完成")
        
        return jsonify({
            "success": True,
            "reply": reply,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"AI对话失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/recommend')
def get_recommend():
    """获取个性化推荐（兼容旧接口）"""
    try:
        user_info = request.args.get('user', 'default')
        recommendations = get_recommendations(user_info)
        
        return jsonify({
            "success": True,
            "recommendations": recommendations,
            "count": len(recommendations),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"获取推荐失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/product/<int:product_id>')
def get_product_detail(product_id):
    """获取商品详情"""
    try:
        products = [
            {
                "id": 0,
                "name": "Redmi Pad 4GB+128GB",
                "price": 1299,
                "img": "https://img14.360buyimg.com/n7/jfs/t1/123456/1.jpg",
                "desc": "优点：性价比高，屏幕素质好，系统流畅，适合学习娱乐\n缺点：不支持手写笔，性能一般",
                "brand": "小米",
                "material": "金属",
                "type": "简约",
                "adv": [
                    "2K高清全屏，护眼显示效果出色",
                    "8000mAh大电池，续航持久",
                    "4扬声器环绕，音质清晰",
                    "轻薄机身，便携携带",
                    "性价比高，适合均衡需求"
                ],
                "disadv": [
                    "不支持手写笔，不适合绘图需求",
                    "性能一般，不适合大型游戏或专业设计软件",
                    "无LTE版本，外出需连接WiFi"
                ],
                "ai": "主要问题集中在续航和性能，适合日常学习娱乐，建议选择官方旗舰店购买。"
            },
            {
                "id": 1,
                "name": "荣耀平板V7 6GB+128GB",
                "price": 1499,
                "img": "https://img14.360buyimg.com/n7/jfs/t1/654321/2.jpg",
                "desc": "优点：大屏护眼，支持多窗口，适合记笔记\n缺点：处理器一般，重量略大",
                "brand": "华为",
                "material": "塑料",
                "type": "科技感",
                "adv": [
                    "大屏护眼，支持多窗口",
                    "适合记笔记，系统流畅",
                    "音质好，续航不错"
                ],
                "disadv": [
                    "处理器一般",
                    "重量略大"
                ],
                "ai": "适合学生和办公用户，推荐购买高配版，注意重量和便携性。"
            },
            {
                "id": 2,
                "name": "小米手环7 Pro",
                "price": 399,
                "img": "https://img14.360buyimg.com/n7/jfs/t1/789012/3.jpg",
                "desc": "优点：续航长，功能丰富，性价比高\n缺点：屏幕较小，充电方式不便",
                "brand": "小米",
                "material": "硅胶",
                "type": "简约",
                "adv": [
                    "14天超长续航",
                    "AMOLED高清彩屏",
                    "117种运动模式",
                    "血氧饱和度监测",
                    "5ATM防水等级"
                ],
                "disadv": [
                    "屏幕相对较小",
                    "充电需要专用充电器",
                    "部分功能需要手机配合"
                ],
                "ai": "性价比很高的智能手环，适合日常运动和健康监测，推荐给预算有限的用户。"
            },
            {
                "id": 3,
                "name": "AirPods Pro 2代",
                "price": 1899,
                "img": "https://img14.360buyimg.com/n7/jfs/t1/456789/4.jpg",
                "desc": "优点：降噪效果好，音质优秀，连接稳定\n缺点：价格较高，续航一般",
                "brand": "苹果",
                "material": "塑料",
                "type": "科技感",
                "adv": [
                    "主动降噪效果出色",
                    "空间音频技术",
                    "IPX4防水等级",
                    "MagSafe充电盒",
                    "与苹果生态完美融合"
                ],
                "disadv": [
                    "价格较高",
                    "续航时间一般",
                    "仅支持苹果设备最佳体验"
                ],
                "ai": "音质和降噪效果都很优秀，适合对音质有要求的用户，但价格偏高。"
            }
        ]
        
        if product_id < len(products):
            logger.info(f"获取商品详情: ID {product_id}")
            return jsonify({
                "success": True,
                "product": products[product_id],
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "success": False,
                "error": "商品不存在"
            }), 404
            
    except Exception as e:
        logger.error(f"获取商品详情失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/products')
def get_products():
    """获取商品列表"""
    try:
        # 支持筛选参数
        brand = request.args.get('brand', '')
        price_min = request.args.get('price_min', '')
        price_max = request.args.get('price_max', '')
        product_type = request.args.get('type', '')
        
        # 这里可以从数据库获取商品列表
        # 暂时返回模拟数据
        products = [
            {"id": 0, "name": "Redmi Pad 4GB+128GB", "price": 1299, "brand": "小米"},
            {"id": 1, "name": "荣耀平板V7 6GB+128GB", "price": 1499, "brand": "华为"},
            {"id": 2, "name": "小米手环7 Pro", "price": 399, "brand": "小米"},
            {"id": 3, "name": "AirPods Pro 2代", "price": 1899, "brand": "苹果"}
        ]
        
        # 应用筛选
        if brand:
            products = [p for p in products if brand.lower() in p['brand'].lower()]
        if price_min:
            products = [p for p in products if p['price'] >= int(price_min)]
        if price_max:
            products = [p for p in products if p['price'] <= int(price_max)]
        
        logger.info(f"获取商品列表，筛选条件: brand={brand}, price={price_min}-{price_max}, type={product_type}")
        
        return jsonify({
            "success": True,
            "products": products,
            "count": len(products),
            "filters": {
                "brand": brand,
                "price_min": price_min,
                "price_max": price_max,
                "type": product_type
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"获取商品列表失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/status')
def get_status():
    """获取系统状态"""
    try:
        # 检查各个模块状态
        status = {
            "api": "running",
            "lixin_ai": "available",
            "crawler": "available",
            "recommender": "available"
        }
        
        return jsonify({
            "success": True,
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"获取状态失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/reviews/jd', methods=['GET'])
def api_jd_negative_reviews():
    product_id = request.args.get('product_id')
    max_count = int(request.args.get('max_count', 20))
    if not product_id:
        return jsonify({"error": "缺少product_id"}), 400
    reviews = fetch_jd_negative_reviews(product_id, max_count)
    return jsonify({"reviews": reviews})

if __name__ == '__main__':
    logger.info("启动蓝心易购后端服务...")
    app.run(host='0.0.0.0', port=5000, debug=True) 