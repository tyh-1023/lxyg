# 蓝心易购后端服务

## 快速启动

### Windows用户
双击运行 `start.bat` 文件，或在命令行中执行：
```bash
start.bat
```

### Linux/Mac用户
在终端中执行：
```bash
chmod +x start.sh
./start.sh
```

### 通用方式
```bash
python start_server.py
```

## 功能测试

启动服务器后，运行测试脚本验证所有功能：
```bash
python test_all.py
```

## 启动脚本说明

### start_server.py
主启动脚本，包含以下功能：
- ✅ Python版本检查（需要3.7+）
- ✅ 依赖包自动安装
- ✅ 配置文件检查
- ✅ Flask服务器启动

**命令行参数：**
- `--help`: 显示帮助信息
- `--check`: 仅检查环境
- `--install`: 仅安装依赖

### start.bat (Windows)
Windows批处理文件，自动检查Python并启动服务器。

### start.sh (Linux/Mac)
Shell脚本，自动检查Python版本并启动服务器。

## API接口

### 基础接口
- `GET /`: 服务器状态
- `GET /api/status`: 服务状态检查

### AI功能接口
- `POST /api/ai/analyze`: 差评分析
- `POST /api/ai/recommend`: 商品推荐
- `POST /api/ai/price`: 价格分析
- `POST /api/ai/chat`: AI对话

### 商品接口
- `GET /api/products`: 商品列表
- `GET /api/products/{id}`: 商品详情

### 爬虫接口
- `GET /api/reviews/jd`: 京东差评爬取

## 配置说明

### 环境变量配置
创建 `.env` 文件或设置环境变量：
```bash
# 蓝心大模型API配置
LIXIN_APP_ID=你的AppID
LIXIN_APP_KEY=你的AppKEY
LIXIN_API_URL=https://api.lixin.com/v1/chat/completions
LIXIN_MODEL=lixin-v1
LIXIN_MAX_TOKENS=2000
LIXIN_TEMPERATURE=0.7

# 服务器配置
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
DEBUG=False
SECRET_KEY=your-secret-key-here
```

### 直接配置
编辑 `config.py` 文件，修改默认值：
```python
def get_lixin_config():
    return {
        'APP_ID': '你的AppID',
        'APP_KEY': '你的AppKEY',
        # ... 其他配置
    }
```

## 故障排除

### 1. Python版本问题
确保安装Python 3.7或更高版本：
```bash
python --version
```

### 2. 依赖安装失败
手动安装依赖：
```bash
pip install -r requirements.txt
```

### 3. 配置文件问题
运行配置检查：
```bash
python start_server.py --check
```

### 4. 端口占用
修改端口号：
```bash
# 在config.py中修改SERVER_PORT
# 或设置环境变量
export SERVER_PORT=5001
```

### 5. API调用失败
检查网络连接和API配置：
```bash
python test_all.py
```

## 开发说明

### 项目结构
```
backend/
├── app.py                 # Flask主应用
├── config.py              # 配置文件
├── requirements.txt       # 依赖列表
├── start_server.py        # 启动脚本
├── start.bat             # Windows启动脚本
├── start.sh              # Linux/Mac启动脚本
├── test_all.py           # 功能测试脚本
├── lixin_ai/             # AI模块
│   └── lixin_api.py      # 蓝心API调用
├── crawler/              # 爬虫模块
│   └── negative_reviews.py # 差评爬虫
└── recommender/          # 推荐模块
    └── recommend.py      # 推荐算法
```

### 添加新功能
1. 在相应模块中添加功能代码
2. 在 `app.py` 中注册API路由
3. 在 `test_all.py` 中添加测试用例
4. 更新文档

## 许可证

本项目仅供学习和研究使用。 