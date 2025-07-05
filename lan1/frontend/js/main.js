// 导入API模块
import { fetchRecommendations, testConnection } from './api.js';

// 模拟商品数据（备用）
const products = [
  {
    name: 'Redmi Pad 4GB+128GB',
    price: 1299,
    img: 'https://img14.360buyimg.com/n7/jfs/t1/123456/1.jpg',
    desc: '优点：性价比高，屏幕素质好，系统流畅，适合学习娱乐\n缺点：不支持手写笔，性能一般',
    brand: '小米',
    material: '金属',
    type: '简约'
  },
  {
    name: '荣耀平板V7 6GB+128GB',
    price: 1499,
    img: 'https://img14.360buyimg.com/n7/jfs/t1/654321/2.jpg',
    desc: '优点：大屏护眼，支持多窗口，适合记笔记\n缺点：处理器一般，重量略大',
    brand: '华为',
    material: '塑料',
    type: '科技感'
  }
];

// 页面切换
const pages = {
  home: document.querySelector('.container'),
  settings: null,
  detail: null,
  message: null,
  mine: null
};

function switchTab(tab) {
  // 根据tab名称跳转到对应页面
  switch(tab) {
    case '首页':
      window.location.href = 'index.html';
      break;
    case '交流圈':
      window.location.href = 'pages/community.html';
      break;
    case '搜索':
      window.location.href = 'pages/search.html';
      break;
    case '贴吧':
      window.location.href = 'pages/tieba.html';
      break;
    case '我的':
      window.location.href = 'pages/mine.html';
      break;
    default:
      alert('该页面开发中，敬请期待！');
  }
}
document.querySelectorAll('.tabbar a').forEach(a => {
  a.onclick = () => switchTab(a.textContent);
});

// 商品卡片渲染
function renderProducts(list) {
  const box = document.querySelector('.recommend-list');
  box.innerHTML = '';
  list.forEach((p, idx) => {
    const card = document.createElement('div');
    card.className = 'recommend-card';
    card.innerHTML = `
      <img src="${p.img}" alt="${p.name}">
      <div class="info">
        <div class="title">${p.name}</div>
        <div class="price">¥${p.price}</div>
        <div class="desc">${p.desc.replace(/\n/g, '<br>')}</div>
      </div>
    `;
    card.onclick = () => {
      // 跳转到详情页，带商品索引参数
      window.location.href = `pages/detail.html?idx=${idx}`;
    };
    box.appendChild(card);
  });
}
// 初始化：测试后端连接并加载推荐商品
async function init() {
  try {
    // 测试后端连接
    const connection = await testConnection();
    console.log('后端连接状态:', connection.msg);
    
    // 获取推荐商品
    const recommendData = await fetchRecommendations();
    if (recommendData.recommendations && recommendData.recommendations.length > 0) {
      renderProducts(recommendData.recommendations);
    } else {
      // 如果后端无数据，使用本地数据
      renderProducts(products);
    }
  } catch (error) {
    console.error('初始化失败:', error);
    // 使用本地数据作为备用
    renderProducts(products);
  }
}

// 筛选交互
const filterGroups = document.querySelectorAll('.filter-group');
let filterState = { brand: '全部', material: '全部', type: '全部' };
filterGroups.forEach((group, idx) => {
  group.addEventListener('click', e => {
    if(e.target.classList.contains('filter-btn')) {
      group.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
      e.target.classList.add('active');
      if(idx === 0) filterState.brand = e.target.textContent;
      if(idx === 1) filterState.material = e.target.textContent;
      if(idx === 2) filterState.type = e.target.textContent;
      filterProducts();
    }
  });
});
function filterProducts() {
  let list = products.filter(p => {
    let b = filterState.brand === '全部' || p.brand === filterState.brand;
    let m = filterState.material === '全部' || p.material === filterState.material;
    let t = filterState.type === '全部' || p.type === filterState.type;
    return b && m && t;
  });
  renderProducts(list);
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init); 