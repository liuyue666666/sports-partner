Page({
  data: {
    partners: [] as unknown[],
    loading: true,
  },

  onShow() {
    this.setData({ loading: false });
  },
});
