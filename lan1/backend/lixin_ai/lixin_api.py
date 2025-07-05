# 蓝心大模型API调用模块
import requests
import json
import time
import hashlib
import hmac
import base64
import re
from typing import List, Dict, Any, Optional, Tuple
import logging
import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_lixin_config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取蓝心大模型API配置
LIXIN_CONFIG = get_lixin_config()
APP_ID = LIXIN_CONFIG['APP_ID']
APP_KEY = LIXIN_CONFIG['APP_KEY']
LIXIN_API_URL = LIXIN_CONFIG['API_URL']
MODEL = LIXIN_CONFIG.get('MODEL', 'lixin-v1')
MAX_TOKENS = LIXIN_CONFIG.get('MAX_TOKENS', 2000)
TEMPERATURE = LIXIN_CONFIG.get('TEMPERATURE', 0.7)

class LixinAI:
    """蓝心大模型API调用类"""
    
    def __init__(self, app_id: str = APP_ID, app_key: str = APP_KEY):
        self.app_id = app_id
        self.app_key = app_key
        self.api_url = LIXIN_API_URL
    
    def _generate_signature(self, timestamp: str, nonce: str) -> str:
        """生成API签名"""
        # 按照蓝心API文档生成签名
        message = f"{self.app_id}{timestamp}{nonce}"
        signature = hmac.new(
            self.app_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(signature).decode('utf-8')
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        timestamp = str(int(time.time()))
        nonce = str(int(time.time() * 1000))
        signature = self._generate_signature(timestamp, nonce)
        
        return {
            'Content-Type': 'application/json',
            'X-App-Id': self.app_id,
            'X-Timestamp': timestamp,
            'X-Nonce': nonce,
            'X-Signature': signature
        }
    
    def _call_api(self, messages: List[Dict[str, str]], model: str = MODEL, 
                  temperature: float = TEMPERATURE, max_tokens: int = MAX_TOKENS,
                  retry_count: int = 3) -> Dict[str, Any]:
        """
        调用蓝心大模型API
        
        Args:
            messages: 对话消息列表
            model: 模型名称
            temperature: 生成温度
            max_tokens: 最大token数
            retry_count: 重试次数
            
        Returns:
            API响应结果
        """
        for attempt in range(retry_count):
            try:
                payload = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                }
                
                headers = self._get_headers()
                
                logger.info(f"调用蓝心API，模型: {model}，第{attempt + 1}次尝试")
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info("蓝心API调用成功")
                    return result
                elif response.status_code == 429:  # 频率限制
                    wait_time = (attempt + 1) * 2
                    logger.warning(f"API频率限制，等待{wait_time}秒后重试")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"蓝心API调用失败: {response.status_code} - {response.text}")
                    if attempt == retry_count - 1:
                        return {"error": f"API调用失败: {response.status_code}"}
                    continue
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"网络请求异常: {str(e)}")
                if attempt == retry_count - 1:
                    return {"error": f"网络请求异常: {str(e)}"}
                time.sleep(1)
                continue
            except Exception as e:
                logger.error(f"API调用异常: {str(e)}")
                if attempt == retry_count - 1:
                    return {"error": f"API调用异常: {str(e)}"}
                time.sleep(1)
                continue
        
        return {"error": "所有重试都失败了"}
    
    def _extract_json_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """从文本中提取JSON内容"""
        try:
            # 尝试直接解析
            return json.loads(text)
        except json.JSONDecodeError:
            # 尝试提取JSON部分
            json_pattern = r'\{.*\}'
            matches = re.findall(json_pattern, text, re.DOTALL)
            if matches:
                try:
                    return json.loads(matches[0])
                except json.JSONDecodeError:
                    pass
            return None
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """分析文本情感"""
        positive_words = ['好', '棒', '优秀', '满意', '推荐', '值得', '不错', '喜欢']
        negative_words = ['差', '烂', '失望', '不推荐', '不值', '问题', '不好', '讨厌']
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            score = positive_count / (positive_count + negative_count + 1)
        elif negative_count > positive_count:
            sentiment = 'negative'
            score = negative_count / (positive_count + negative_count + 1)
        else:
            sentiment = 'neutral'
            score = 0.5
        
        return {
            'sentiment': sentiment,
            'score': score,
            'positive_count': positive_count,
            'negative_count': negative_count
        }
    
    def analyze_reviews(self, reviews: List[str], product_name: str = "", 
                       include_sentiment: bool = True) -> Dict[str, Any]:
        """
        分析商品差评，返回AI分析结果
        
        Args:
            reviews: 差评列表
            product_name: 商品名称
            include_sentiment: 是否包含情感分析
            
        Returns:
            分析结果字典
        """
        if not reviews:
            return {
                "summary": "暂无差评数据",
                "suggestions": [],
                "risk_level": "low",
                "key_issues": [],
                "sentiment_analysis": {
                    "overall_sentiment": "neutral",
                    "positive_ratio": 0.0,
                    "negative_ratio": 0.0
                },
                "statistics": {
                    "total_reviews": 0,
                    "analyzed_reviews": 0
                }
            }
        
        # 情感分析
        sentiment_results = []
        if include_sentiment:
            for review in reviews:
                sentiment = self._analyze_sentiment(review)
                sentiment_results.append(sentiment)
        
        # 统计情感分布
        if sentiment_results:
            positive_count = sum(1 for s in sentiment_results if s['sentiment'] == 'positive')
            negative_count = sum(1 for s in sentiment_results if s['sentiment'] == 'negative')
            total_count = len(sentiment_results)
            
            sentiment_summary = {
                "overall_sentiment": "positive" if positive_count > negative_count else "negative" if negative_count > positive_count else "neutral",
                "positive_ratio": positive_count / total_count if total_count > 0 else 0.0,
                "negative_ratio": negative_count / total_count if total_count > 0 else 0.0,
                "neutral_ratio": (total_count - positive_count - negative_count) / total_count if total_count > 0 else 0.0
            }
        else:
            sentiment_summary = {
                "overall_sentiment": "neutral",
                "positive_ratio": 0.0,
                "negative_ratio": 0.0,
                "neutral_ratio": 1.0
            }
        
        # 构建分析提示词
        reviews_text = "\n".join([f"{i+1}. {review}" for i, review in enumerate(reviews[:15])])  # 限制前15条
        
        prompt = f"""
        请分析以下商品差评，并提供专业的购物建议：

        商品名称：{product_name if product_name else "未知商品"}
        差评内容：
        {reviews_text}

        请从以下几个方面进行分析：
        1. 问题总结：主要问题类型和严重程度
        2. 风险等级：低/中/高
        3. 关键问题：最需要关注的问题点
        4. 购买建议：是否值得购买，如何避免问题
        5. 替代方案：如果有更好的选择
        6. 问题分类：将问题按类型分类（物流、质量、售后、功能、价格等）

        请用JSON格式返回结果，包含以下字段：
        {{
            "summary": "问题总结",
            "risk_level": "风险等级",
            "key_issues": ["关键问题1", "关键问题2"],
            "suggestions": ["建议1", "建议2"],
            "alternatives": ["替代方案1", "替代方案2"],
            "issue_categories": {{
                "物流": "问题描述",
                "质量": "问题描述",
                "售后": "问题描述",
                "功能": "问题描述",
                "价格": "问题描述"
            }},
            "confidence_score": 0.85
        }}
        """
        
        messages = [
            {"role": "system", "content": "你是一个专业的商品分析专家，擅长分析用户评价并提供购物建议。请确保返回有效的JSON格式。"},
            {"role": "user", "content": prompt}
        ]
        
        result = self._call_api(messages)
        
        if "error" in result:
            # API调用失败，返回模拟数据
            logger.warning("使用模拟数据")
            return self._get_enhanced_fallback_analysis(reviews, sentiment_summary)
        
        try:
            # 解析API返回的内容
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                
                # 尝试解析JSON格式的回复
                analysis = self._extract_json_from_text(content)
                if analysis:
                    # 添加情感分析和统计信息
                    analysis["sentiment_analysis"] = sentiment_summary
                    analysis["statistics"] = {
                        "total_reviews": len(reviews),
                        "analyzed_reviews": min(len(reviews), 15)
                    }
                    return analysis
                else:
                    # 如果不是JSON格式，进行文本解析
                    return self._parse_enhanced_text_analysis(content, sentiment_summary, len(reviews))
            else:
                return self._get_enhanced_fallback_analysis(reviews, sentiment_summary)
                
        except Exception as e:
            logger.error(f"解析API响应失败: {str(e)}")
            return self._get_enhanced_fallback_analysis(reviews, sentiment_summary)
    
    def _parse_text_analysis(self, content: str) -> Dict[str, Any]:
        """解析文本格式的分析结果"""
        return {
            "summary": content[:200] + "..." if len(content) > 200 else content,
            "risk_level": "medium",
            "key_issues": ["需要进一步分析"],
            "suggestions": ["建议仔细查看详细评价"],
            "alternatives": []
        }
    
    def _parse_enhanced_text_analysis(self, content: str, sentiment_summary: Dict[str, Any], 
                                    total_reviews: int) -> Dict[str, Any]:
        """解析增强的文本格式分析结果"""
        return {
            "summary": content[:300] + "..." if len(content) > 300 else content,
            "risk_level": "medium",
            "key_issues": ["需要进一步分析"],
            "suggestions": ["建议仔细查看详细评价"],
            "alternatives": [],
            "issue_categories": {
                "物流": "需要进一步分析",
                "质量": "需要进一步分析", 
                "售后": "需要进一步分析",
                "功能": "需要进一步分析",
                "价格": "需要进一步分析"
            },
            "confidence_score": 0.6,
            "sentiment_analysis": sentiment_summary,
            "statistics": {
                "total_reviews": total_reviews,
                "analyzed_reviews": min(total_reviews, 15)
            }
        }
    
    def _get_fallback_analysis(self, reviews: List[str]) -> Dict[str, Any]:
        """获取备用分析结果（当API调用失败时）"""
        # 简单的关键词分析
        keywords = {
            "物流": 0, "质量": 0, "售后": 0, "价格": 0, "功能": 0
        }
        
        for review in reviews:
            for keyword in keywords:
                if keyword in review:
                    keywords[keyword] += 1
        
        # 找出最多的问题
        max_issue = max(keywords.items(), key=lambda x: x[1])
        
        suggestions = []
        if max_issue[0] == "物流":
            suggestions = ["选择官方旗舰店", "查看物流评分", "选择就近仓库"]
        elif max_issue[0] == "质量":
            suggestions = ["查看详细参数", "对比同类产品", "选择知名品牌"]
        elif max_issue[0] == "售后":
            suggestions = ["选择官方渠道", "查看售后政策", "保留购买凭证"]
        else:
            suggestions = ["仔细查看评价", "对比多家店铺", "选择高评分卖家"]
        
        return {
            "summary": f"主要问题集中在{max_issue[0]}方面，建议谨慎购买。",
            "risk_level": "medium",
            "key_issues": [max_issue[0]],
            "suggestions": suggestions,
            "alternatives": []
        }
    
    def _get_enhanced_fallback_analysis(self, reviews: List[str], sentiment_summary: Dict[str, Any]) -> Dict[str, Any]:
        """获取增强的备用分析结果（当API调用失败时）"""
        # 简单的关键词分析
        keywords = {
            "物流": 0, "质量": 0, "售后": 0, "价格": 0, "功能": 0, "包装": 0, "尺寸": 0
        }
        
        for review in reviews:
            for keyword in keywords:
                if keyword in review:
                    keywords[keyword] += 1
        
        # 找出最多的问题
        max_issue = max(keywords.items(), key=lambda x: x[1])
        
        # 构建问题分类
        issue_categories = {}
        for category, count in keywords.items():
            if count > 0:
                issue_categories[category] = f"发现{count}个相关问题"
            else:
                issue_categories[category] = "暂无相关问题"
        
        suggestions = []
        if max_issue[0] == "物流":
            suggestions = ["选择官方旗舰店", "查看物流评分", "选择就近仓库", "选择京东自营"]
        elif max_issue[0] == "质量":
            suggestions = ["查看详细参数", "对比同类产品", "选择知名品牌", "查看质检报告"]
        elif max_issue[0] == "售后":
            suggestions = ["选择有保障的商家", "查看售后政策", "保留购买凭证", "选择延保服务"]
        elif max_issue[0] == "价格":
            suggestions = ["对比多个平台", "关注促销活动", "使用比价工具", "选择性价比高的产品"]
        elif max_issue[0] == "功能":
            suggestions = ["仔细阅读产品说明", "查看用户评测", "选择功能齐全的产品", "考虑实际需求"]
        else:
            suggestions = ["仔细查看详细评价", "对比同类产品", "选择知名品牌"]
        
        return {
            "summary": f"主要问题集中在{max_issue[0]}方面，共发现{max_issue[1]}个相关问题",
            "risk_level": "medium" if max_issue[1] < 5 else "high",
            "key_issues": [f"{max_issue[0]}问题", "需要进一步了解"],
            "suggestions": suggestions,
            "alternatives": ["考虑其他品牌", "选择替代产品"],
            "issue_categories": issue_categories,
            "confidence_score": 0.7,
            "sentiment_analysis": sentiment_summary,
            "statistics": {
                "total_reviews": len(reviews),
                "analyzed_reviews": min(len(reviews), 15)
            }
        }
    
    def get_product_recommendation(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        基于用户偏好获取商品推荐
        
        Args:
            user_preferences: 用户偏好信息
            
        Returns:
            推荐结果
        """
        prompt = f"""
        基于以下用户偏好，推荐合适的商品：

        用户偏好：
        - 预算：{user_preferences.get('budget', '不限')}
        - 品牌偏好：{user_preferences.get('brands', '不限')}
        - 使用场景：{user_preferences.get('scenarios', '通用')}
        - 特殊需求：{user_preferences.get('requirements', '无')}

        请推荐3-5个商品，并说明推荐理由。
        返回JSON格式：
        {{
            "recommendations": [
                {{
                    "name": "商品名称",
                    "reason": "推荐理由",
                    "price_range": "价格区间",
                    "pros": ["优点1", "优点2"],
                    "cons": ["缺点1", "缺点2"]
                }}
            ]
        }}
        """
        
        messages = [
            {"role": "system", "content": "你是一个专业的商品推荐专家，了解各种数码产品和消费电子。"},
            {"role": "user", "content": prompt}
        ]
        
        result = self._call_api(messages)
        
        if "error" in result:
            return self._get_fallback_recommendations(user_preferences)
        
        try:
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                return json.loads(content)
            else:
                return self._get_fallback_recommendations(user_preferences)
        except Exception as e:
            logger.error(f"解析推荐结果失败: {str(e)}")
            return self._get_fallback_recommendations(user_preferences)
    
    def _get_fallback_recommendations(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """获取备用推荐结果"""
        budget = user_preferences.get('budget', '不限')
        
        if '1000' in str(budget) or '1000以下' in str(budget):
            return {
                "recommendations": [
                    {
                        "name": "Redmi Pad",
                        "reason": "性价比高，适合预算有限的用户",
                        "price_range": "1000-1500元",
                        "pros": ["价格实惠", "屏幕素质好", "续航不错"],
                        "cons": ["性能一般", "不支持手写笔"]
                    }
                ]
            }
        else:
            return {
                "recommendations": [
                    {
                        "name": "iPad Air",
                        "reason": "性能强劲，适合专业用户",
                        "price_range": "4000-5000元",
                        "pros": ["性能优秀", "生态完善", "支持手写笔"],
                        "cons": ["价格较高", "配件昂贵"]
                    }
                ]
            }
    
    def analyze_price_trend(self, product_name: str, price_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析商品价格走势
        
        Args:
            product_name: 商品名称
            price_history: 价格历史数据
            
        Returns:
            价格分析结果
        """
        if not price_history:
            return {
                "trend": "stable",
                "recommendation": "暂无价格数据",
                "best_time": "未知"
            }
        
        prompt = f"""
        分析以下商品的价格走势：

        商品：{product_name}
        价格历史：{json.dumps(price_history, ensure_ascii=False)}

        请分析：
        1. 价格趋势（上涨/下跌/稳定）
        2. 最佳购买时机
        3. 价格预测
        4. 购买建议

        返回JSON格式：
        {{
            "trend": "上涨/下跌/稳定",
            "recommendation": "购买建议",
            "best_time": "最佳购买时机",
            "prediction": "价格预测"
        }}
        """
        
        messages = [
            {"role": "system", "content": "你是一个价格分析专家，擅长分析商品价格走势。"},
            {"role": "user", "content": prompt}
        ]
        
        result = self._call_api(messages)
        
        if "error" in result:
            return self._get_fallback_price_analysis()
        
        try:
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                return json.loads(content)
            else:
                return self._get_fallback_price_analysis()
        except Exception as e:
            logger.error(f"解析价格分析失败: {str(e)}")
            return self._get_fallback_price_analysis()
    
    def _get_fallback_price_analysis(self) -> Dict[str, Any]:
        """获取备用价格分析结果"""
        return {
            "trend": "stable",
            "recommendation": "价格相对稳定，可以随时购买",
            "best_time": "当前",
            "prediction": "短期内价格变化不大"
        }
    
    def chat_with_ai(self, message: str, context: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        与AI进行对话
        
        Args:
            message: 用户消息
            context: 对话历史上下文
            
        Returns:
            对话结果
        """
        messages = [
            {"role": "system", "content": "你是蓝心易购的智能购物助手，专门帮助用户解决购物问题，提供商品推荐和购物建议。"}
        ]
        
        if context:
            messages.extend(context)
        
        messages.append({"role": "user", "content": message})
        
        result = self._call_api(messages, temperature=0.8)
        
        if "error" in result:
            return {
                "response": "抱歉，我现在无法回答您的问题，请稍后再试。",
                "error": result["error"]
            }
        
        try:
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                return {
                    "response": content,
                    "success": True
                }
            else:
                return {
                    "response": "抱歉，我无法理解您的问题，请重新描述。",
                    "success": False
                }
        except Exception as e:
            logger.error(f"解析对话结果失败: {str(e)}")
            return {
                "response": "抱歉，处理您的消息时出现错误。",
                "success": False
            }
    
    def compare_products(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        比较多个商品
        
        Args:
            products: 商品列表，每个商品包含name, price, features等信息
            
        Returns:
            比较结果
        """
        if len(products) < 2:
            return {
                "error": "至少需要2个商品进行比较"
            }
        
        products_info = []
        for i, product in enumerate(products):
            info = f"商品{i+1}: {product.get('name', '未知')}\n"
            info += f"价格: {product.get('price', '未知')}\n"
            info += f"特点: {', '.join(product.get('features', []))}\n"
            products_info.append(info)
        
        prompt = f"""
        请比较以下商品，并提供购买建议：

        {chr(10).join(products_info)}

        请从以下方面进行分析：
        1. 性价比对比
        2. 功能特点对比
        3. 适用场景
        4. 推荐指数
        5. 最终建议

        返回JSON格式：
        {{
            "comparison": [
                {{
                    "product_name": "商品名称",
                    "pros": ["优点1", "优点2"],
                    "cons": ["缺点1", "缺点2"],
                    "recommendation_score": 8.5,
                    "best_for": "适用场景"
                }}
            ],
            "overall_recommendation": "整体推荐",
            "best_choice": "最佳选择"
        }}
        """
        
        messages = [
            {"role": "system", "content": "你是一个专业的商品比较专家，擅长分析不同商品的优缺点。"},
            {"role": "user", "content": prompt}
        ]
        
        result = self._call_api(messages)
        
        if "error" in result:
            return self._get_fallback_comparison(products)
        
        try:
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                comparison = self._extract_json_from_text(content)
                if comparison:
                    return comparison
                else:
                    return self._get_fallback_comparison(products)
            else:
                return self._get_fallback_comparison(products)
        except Exception as e:
            logger.error(f"解析比较结果失败: {str(e)}")
            return self._get_fallback_comparison(products)
    
    def _get_fallback_comparison(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """获取备用比较结果"""
        comparison = []
        for product in products:
            comparison.append({
                "product_name": product.get('name', '未知商品'),
                "pros": ["性价比不错", "功能齐全"],
                "cons": ["需要进一步了解"],
                "recommendation_score": 7.0,
                "best_for": "通用场景"
            })
        
        return {
            "comparison": comparison,
            "overall_recommendation": "建议根据个人需求选择",
            "best_choice": "需要更多信息才能确定"
        }
    
    def analyze_shopping_behavior(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析用户购物行为
        
        Args:
            user_data: 用户数据，包含浏览历史、购买记录等
            
        Returns:
            行为分析结果
        """
        prompt = f"""
        分析以下用户的购物行为数据：

        用户数据：
        {json.dumps(user_data, ensure_ascii=False, indent=2)}

        请分析：
        1. 购物偏好
        2. 消费习惯
        3. 兴趣领域
        4. 购买力水平
        5. 个性化推荐

        返回JSON格式：
        {{
            "preferences": ["偏好1", "偏好2"],
            "consumption_habit": "消费习惯描述",
            "interest_areas": ["兴趣领域1", "兴趣领域2"],
            "purchasing_power": "高/中/低",
            "personalized_recommendations": ["推荐1", "推荐2"],
            "shopping_pattern": "购物模式描述"
        }}
        """
        
        messages = [
            {"role": "system", "content": "你是一个用户行为分析专家，擅长分析购物行为和提供个性化建议。"},
            {"role": "user", "content": prompt}
        ]
        
        result = self._call_api(messages)
        
        if "error" in result:
            return self._get_fallback_behavior_analysis(user_data)
        
        try:
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                analysis = self._extract_json_from_text(content)
                if analysis:
                    return analysis
                else:
                    return self._get_fallback_behavior_analysis(user_data)
            else:
                return self._get_fallback_behavior_analysis(user_data)
        except Exception as e:
            logger.error(f"解析行为分析失败: {str(e)}")
            return self._get_fallback_behavior_analysis(user_data)
    
    def _get_fallback_behavior_analysis(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """获取备用行为分析结果"""
        return {
            "preferences": ["数码产品", "性价比优先"],
            "consumption_habit": "理性消费，注重性价比",
            "interest_areas": ["科技", "数码"],
            "purchasing_power": "中",
            "personalized_recommendations": ["关注促销活动", "对比多个平台"],
            "shopping_pattern": "谨慎型购物者"
        }
    
    def generate_shopping_guide(self, category: str, budget: str = "不限") -> Dict[str, Any]:
        """
        生成购物指南
        
        Args:
            category: 商品类别
            budget: 预算范围
            
        Returns:
            购物指南
        """
        prompt = f"""
        为{category}类别生成购物指南，预算范围：{budget}

        请包含以下内容：
        1. 选购要点
        2. 品牌推荐
        3. 价格区间建议
        4. 购买渠道建议
        5. 注意事项
        6. 常见陷阱

        返回JSON格式：
        {{
            "category": "{category}",
            "budget_range": "{budget}",
            "key_points": ["要点1", "要点2"],
            "brand_recommendations": ["品牌1", "品牌2"],
            "price_suggestions": ["价格建议1", "价格建议2"],
            "purchase_channels": ["渠道1", "渠道2"],
            "precautions": ["注意事项1", "注意事项2"],
            "common_traps": ["陷阱1", "陷阱2"],
            "expert_tips": ["专家建议1", "专家建议2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "你是一个专业的购物指南专家，了解各种商品的选购要点和注意事项。"},
            {"role": "user", "content": prompt}
        ]
        
        result = self._call_api(messages)
        
        if "error" in result:
            return self._get_fallback_shopping_guide(category, budget)
        
        try:
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                guide = self._extract_json_from_text(content)
                if guide:
                    return guide
                else:
                    return self._get_fallback_shopping_guide(category, budget)
            else:
                return self._get_fallback_shopping_guide(category, budget)
        except Exception as e:
            logger.error(f"解析购物指南失败: {str(e)}")
            return self._get_fallback_shopping_guide(category, budget)
    
    def _get_fallback_shopping_guide(self, category: str, budget: str) -> Dict[str, Any]:
        """获取备用购物指南"""
        return {
            "category": category,
            "budget_range": budget,
            "key_points": ["选择知名品牌", "查看用户评价", "对比价格"],
            "brand_recommendations": ["知名品牌A", "知名品牌B"],
            "price_suggestions": ["根据预算选择合适价位"],
            "purchase_channels": ["官方旗舰店", "大型电商平台"],
            "precautions": ["注意售后服务", "保留购买凭证"],
            "common_traps": ["虚假宣传", "价格陷阱"],
            "expert_tips": ["货比三家", "理性消费"]
        }

# 创建全局实例
lixin_ai = LixinAI()

def analyze_reviews(reviews: List[str]) -> Dict[str, Any]:
    """
    分析商品差评的便捷函数
    
    Args:
        reviews: 差评列表
        
    Returns:
        分析结果
    """
    return lixin_ai.analyze_reviews(reviews)

def get_product_recommendation(user_preferences: Dict[str, Any]) -> Dict[str, Any]:
    """
    获取商品推荐的便捷函数
    
    Args:
        user_preferences: 用户偏好
        
    Returns:
        推荐结果
    """
    return lixin_ai.get_product_recommendation(user_preferences)

def analyze_price_trend(product_name: str, price_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析价格走势的便捷函数
    
    Args:
        product_name: 商品名称
        price_history: 价格历史
        
    Returns:
        价格分析结果
    """
    return lixin_ai.analyze_price_trend(product_name, price_history) 