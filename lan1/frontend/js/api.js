// 与后端API通信模块
const API_BASE = 'http://localhost:5000/api';

// 获取商品推荐
export async function fetchRecommendations(user = 'default') {
    try {
        const res = await fetch(`${API_BASE}/recommend?user=${user}`);
        return await res.json();
    } catch (error) {
        console.error('获取推荐失败:', error);
        return { recommendations: [], count: 0 };
    }
}

// 获取商品差评
export async function fetchReviews(product) {
    try {
        const res = await fetch(`${API_BASE}/review?product=${encodeURIComponent(product)}`);
        return await res.json();
    } catch (error) {
        console.error('获取差评失败:', error);
        return { reviews: [], count: 0 };
    }
}

// AI分析差评
export async function analyzeReviews(reviews) {
    try {
        const res = await fetch(`${API_BASE}/ai_analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ reviews })
        });
        return await res.json();
    } catch (error) {
        console.error('AI分析失败:', error);
        return { summary: '分析失败', suggest: '请稍后重试' };
    }
}

// 获取商品详情
export async function fetchProductDetail(productId) {
    try {
        const res = await fetch(`${API_BASE}/product/${productId}`);
        return await res.json();
    } catch (error) {
        console.error('获取商品详情失败:', error);
        return null;
    }
}

// 测试后端连通性
export async function testConnection() {
    try {
        const res = await fetch(`${API_BASE}/hello`);
        return await res.json();
    } catch (error) {
        console.error('后端连接失败:', error);
        return { msg: '后端连接失败' };
    }
} 