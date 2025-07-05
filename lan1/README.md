# 蓝心易购

## 项目简介
蓝心易购是一个基于大模型智能分析的移动端购物推荐平台，前端采用 HTML/CSS/JS，后端采用 Python（Flask），可自动爬取购物平台差评，调用蓝心大模型分析，为用户提供商品推荐和购物建议。

## 目录结构
```
lan1/
├── backend/                  # Python后端
│   ├── app.py                # 主后端服务入口
│   ├── requirements.txt      # 后端依赖
│   ├── crawler/              # 爬虫模块
│   │   └── review_spider.py
│   ├── lixin_ai/             # 蓝心大模型API调用模块
│   │   └── lixin_api.py
│   ├── recommender/          # 商品推荐与分析逻辑
│   │   └── recommend.py
│   ├── models/               # 数据模型
│   └── utils/                # 工具类
│
├── frontend/                 # 前端
│   ├── index.html            # 主页面
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   └── api.js
│   ├── assets/               # 图片、图标等资源
│   └── pages/                # 其他页面
│       ├── settings.html
│       ├── detail.html
│       └── ...
│
├── README.md                 # 项目说明
└── .gitignore
```

## 启动方式
1. 后端：
   - 进入 backend 目录，安装依赖 `pip install -r requirements.txt`
   - 运行 `python app.py`
2. 前端：
   - 直接用浏览器打开 frontend/index.html

## 主要功能
- 差评爬取与分析
- 蓝心大模型智能推荐
- 商品筛选、详情、设置、消息等移动端页面
- 个性化购物建议 