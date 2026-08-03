Page({
  data: {
    activities: [] as unknown[],
    loading: true,
  },

  onShow() {
    this.setData({ loading: false });
  },

  goCreate() {
    wx.navigateTo({ url: '/pages/activity/create/create' });
  },

  goMy() {
    wx.navigateTo({ url: '/pages/activity/my/my' });
  },
});
