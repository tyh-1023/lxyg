import requests
import time
import random

def fetch_jd_negative_reviews(product_id, max_count=20):
    """
    爬取京东商品的差评（1-2星）
    :param product_id: 商品ID
    :param max_count: 最大评论数
    :return: 差评列表
    """
    url = "https://club.jd.com/comment/productPageComments.action"
    page = 0
    reviews = []
    while len(reviews) < max_count:
        params = {
            "productId": product_id,
            "score": 1,  # 1=差评, 2=中评, 3=好评
            "sortType": 5,
            "page": page,
            "pageSize": 10,
            "isShadowSku": 0,
            "fold": 1
        }
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            if resp.status_code != 200:
                break
            data = resp.json()
            comments = data.get("comments", [])
            if not comments:
                break
            for c in comments:
                reviews.append({
                    "user": c.get("nickname", ""),
                    "content": c.get("content", ""),
                    "date": c.get("creationTime", ""),
                    "score": c.get("score", 1),
                    "product_id": product_id
                })
                if len(reviews) >= max_count:
                    break
            page += 1
            time.sleep(random.uniform(0.5, 1.5))
        except Exception as e:
            break
    return reviews 