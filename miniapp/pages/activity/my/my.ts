import { listMyCreated, listMyJoined, Activity } from '../../../services/activity';
import { formatDateTime, statusText } from '../../../utils/format';

Page({
  data: {
    tab: 'joined' as 'joined' | 'created',
    activities: [] as Activity[],
    loading: true,
  },

  onShow() {
    this.loadData();
  },

  switchTab(e: WechatMiniprogram.TouchEvent) {
    this.setData({ tab: e.currentTarget.dataset.tab as 'joined' | 'created' });
    this.loadData();
  },

  async loadData() {
    this.setData({ loading: true });
    try {
      const list = this.data.tab === 'joined' ? await listMyJoined() : await listMyCreated();
      this.setData({
        activities: list.map((a) => ({
          ...a,
          startText: formatDateTime(a.start_time),
          statusText: statusText(a.status),
        })),
        loading: false,
      });
    } catch (err) {
      wx.showToast({
        title: err instanceof Error ? err.message : '加载失败',
        icon: 'none',
      });
      this.setData({ loading: false });
    }
  },

  goDetail(e: WechatMiniprogram.TouchEvent) {
    wx.navigateTo({ url: `/pages/activity/detail/detail?id=${e.currentTarget.dataset.id}` });
  },
});
