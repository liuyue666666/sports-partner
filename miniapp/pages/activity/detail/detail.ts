import {
  cancelActivity,
  cancelJoin,
  getActivity,
  joinActivity,
  ActivityDetail,
} from '../../services/activity';
import { getMe } from '../../services/user';
import { formatDateTime, genderRequirementText, statusText } from '../../utils/format';

Page({
  data: {
    activityId: 0,
    activity: null as ActivityDetail | null,
    loading: true,
    acting: false,
    isCreator: false,
  },

  onLoad(options: Record<string, string | undefined>) {
    this.setData({ activityId: Number(options.id || 0) });
    this.loadDetail();
  },

  async loadDetail() {
    if (!this.data.activityId) return;
    this.setData({ loading: true });
    try {
      const [activity, me] = await Promise.all([
        getActivity(this.data.activityId),
        isLoggedIn() ? getMe() : Promise.resolve(null),
      ]);
      this.setData({
        activity: {
          ...activity,
          startText: formatDateTime(activity.start_time),
          deadlineText: formatDateTime(activity.registration_deadline),
          statusText: statusText(activity.status),
          genderText: genderRequirementText(activity.gender_requirement),
          slotsText: `${activity.current_participants}/${activity.max_participants}人`,
        },
        isCreator: me ? me.id === activity.creator.id : false,
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

  async ensureLogin(): Promise<boolean> {
    if (isLoggedIn()) return true;
    try {
      await loginWithWechat();
      return true;
    } catch {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return false;
    }
  },

  async handleJoin() {
    if (!(await this.ensureLogin())) return;
    this.setData({ acting: true });
    try {
      await joinActivity(this.data.activityId);
      wx.showToast({ title: '报名成功', icon: 'success' });
      this.loadDetail();
    } catch (err) {
      wx.showToast({ title: err instanceof Error ? err.message : '报名失败', icon: 'none' });
    } finally {
      this.setData({ acting: false });
    }
  },

  async handleCancelJoin() {
    this.setData({ acting: true });
    try {
      await cancelJoin(this.data.activityId);
      wx.showToast({ title: '已取消报名', icon: 'none' });
      this.loadDetail();
    } catch (err) {
      wx.showToast({ title: err instanceof Error ? err.message : '操作失败', icon: 'none' });
    } finally {
      this.setData({ acting: false });
    }
  },

  async handleCancelActivity() {
    wx.showModal({
      title: '确认取消',
      content: '取消后所有参与者将收到通知',
      success: async (res) => {
        if (!res.confirm) return;
        this.setData({ acting: true });
        try {
          await cancelActivity(this.data.activityId);
          wx.showToast({ title: '活动已取消', icon: 'none' });
          this.loadDetail();
        } catch (err) {
          wx.showToast({ title: err instanceof Error ? err.message : '操作失败', icon: 'none' });
        } finally {
          this.setData({ acting: false });
        }
      },
    });
  },
});
