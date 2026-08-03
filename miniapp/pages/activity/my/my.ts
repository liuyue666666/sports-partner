Page({
  data: {
    tab: 'joined' as 'joined' | 'created',
  },

  switchTab(e: WechatMiniprogram.TouchEvent) {
    this.setData({ tab: e.currentTarget.dataset.tab });
  },
});
