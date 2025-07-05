// 主题色列表
const themeColors = ['#3a5cff', '#4caf50', '#ffb300', '#e040fb', '#00bcd4', '#bdbdbd'];

// 读取本地设置
function getSetting(key, def) {
  return localStorage.getItem(key) || def;
}
function setSetting(key, val) {
  localStorage.setItem(key, val);
}

// 字体大小
const fontBtns = document.querySelectorAll('.setting-group button');
fontBtns.forEach(btn => {
  btn.onclick = () => {
    fontBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    setSetting('fontSize', btn.textContent);
    applySettings();
  };
});

// 主题色
const colorDots = document.querySelectorAll('.color-dot');
colorDots.forEach((dot, idx) => {
  dot.onclick = () => {
    setSetting('themeColor', themeColors[idx]);
    applySettings();
  };
});

// 深色模式
const darkSwitch = document.querySelectorAll('.setting-group input[type=checkbox]')[0];
darkSwitch.onchange = function() {
  setSetting('darkMode', this.checked ? '1' : '0');
  applySettings();
};

// 通知提醒
const notifySwitch = document.querySelectorAll('.setting-group input[type=checkbox]')[1];
notifySwitch.onchange = function() {
  setSetting('notify', this.checked ? '1' : '0');
};

// 应用设置到页面
function applySettings() {
  // 字体大小
  const size = getSetting('fontSize', '中');
  document.documentElement.style.setProperty('--font-size', size === '小' ? '14px' : size === '大' ? '18px' : '16px');
  // 主题色
  const color = getSetting('themeColor', '#3a5cff');
  document.documentElement.style.setProperty('--theme-color', color);
  // 深色模式
  const dark = getSetting('darkMode', '0') === '1';
  if(dark) document.body.classList.add('dark');
  else document.body.classList.remove('dark');
}

// 页面加载时应用
applySettings();
// 设置按钮高亮
(function syncBtns() {
  const size = getSetting('fontSize', '中');
  fontBtns.forEach(b => b.classList.toggle('active', b.textContent === size));
})(); 