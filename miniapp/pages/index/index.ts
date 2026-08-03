Page({
  data: {
    loading: true,
  },

  onLoad() {
    this.setData({ loading: false });
  },

  goCreateActivity() {
    wx.navigateTo({ url: '/pages/activity/create/create' });
  },

  goRegion() {
    wx.navigateTo({ url: '/pages/region/region' });
  },
});
