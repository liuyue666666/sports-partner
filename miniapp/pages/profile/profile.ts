Page({
  data: {
    isLoggedIn: false,
    nickname: '',
  },

  onShow() {
    const token = wx.getStorageSync('access_token');
    this.setData({ isLoggedIn: !!token });
  },

  goLogin() {
    wx.showToast({ title: '微信登录 — Phase 1', icon: 'none' });
  },
});
