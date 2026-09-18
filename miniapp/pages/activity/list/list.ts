import { listActivities, Activity } from '../../services/activity';
import { getCurrentLocation } from '../../utils/location';
import { formatDateTime, statusText } from '../../utils/format';
import { formatDistance } from '../../utils/location';

Page({
  data: {
    activities: [] as Activity[],
    loading: true,
  },

  onShow() {
    this.loadActivities();
  },

  async loadActivities() {
    this.setData({ loading: true });
    try {
      let params: { lat?: number; lng?: number; radius?: number } = {};
      try {
        const loc = await getCurrentLocation();
        params = { lat: loc.latitude, lng: loc.longitude, radius: 5000 };
      } catch {
        // location optional for list
      }
      const activities = await listActivities(params);
      this.setData({
        activities: activities.map((a) => ({
          ...a,
          startText: formatDateTime(a.start_time),
          statusText: statusText(a.status),
          distanceText: a.distance_meters != null ? formatDistance(a.distance_meters) : '',
          slotsText: `${a.current_participants}/${a.max_participants}人`,
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

  goCreate() {
    wx.navigateTo({ url: '/pages/activity/create/create' });
  },

  goMy() {
    wx.navigateTo({ url: '/pages/activity/my/my' });
  },

  goDetail(e: WechatMiniprogram.TouchEvent) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({ url: `/pages/activity/detail/detail?id=${id}` });
  },
});
