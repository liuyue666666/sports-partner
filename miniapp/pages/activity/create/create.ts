import { createActivity } from '../../services/activity';
import { getSportTags, SportTag } from '../../services/user';
import { getCurrentLocation } from '../../utils/location';
import { isLoggedIn, loginWithWechat } from '../../utils/auth';

Page({
  data: {
    sportTags: [] as SportTag[],
    sportTagIndex: 0,
    title: '',
    description: '',
    address: '',
    maxParticipants: 4,
    genderIndex: 0,
    genderOptions: ['不限', '仅男', '仅女'],
    startDate: '',
    startTime: '',
    deadlineDate: '',
    deadlineTime: '',
    latitude: 0,
    longitude: 0,
    submitting: false,
  },

  onLoad() {
    this.init();
  },

  async init() {
    if (!isLoggedIn()) {
      wx.showModal({
        title: '需要登录',
        content: '发布活动需要先登录',
        success: async (res) => {
          if (res.confirm) {
            await loginWithWechat();
            this.loadTags();
          } else {
            wx.navigateBack();
          }
        },
      });
      return;
    }
    this.loadTags();
    try {
      const loc = await getCurrentLocation();
      this.setData({ latitude: loc.latitude, longitude: loc.longitude });
    } catch {
      wx.showToast({ title: '请授权位置信息', icon: 'none' });
    }
  },

  async loadTags() {
    const sportTags = await getSportTags();
    this.setData({ sportTags });
  },

  onTitleInput(e: WechatMiniprogram.Input) {
    this.setData({ title: e.detail.value });
  },

  onDescInput(e: WechatMiniprogram.Input) {
    this.setData({ description: e.detail.value });
  },

  onAddressInput(e: WechatMiniprogram.Input) {
    this.setData({ address: e.detail.value });
  },

  onMaxInput(e: WechatMiniprogram.Input) {
    this.setData({ maxParticipants: Number(e.detail.value) || 2 });
  },

  onSportTagChange(e: WechatMiniprogram.PickerChange) {
    this.setData({ sportTagIndex: Number(e.detail.value) });
  },

  onGenderChange(e: WechatMiniprogram.PickerChange) {
    this.setData({ genderIndex: Number(e.detail.value) });
  },

  onStartDateChange(e: WechatMiniprogram.PickerChange) {
    this.setData({ startDate: e.detail.value as string });
  },

  onStartTimeChange(e: WechatMiniprogram.PickerChange) {
    this.setData({ startTime: e.detail.value as string });
  },

  onDeadlineDateChange(e: WechatMiniprogram.PickerChange) {
    this.setData({ deadlineDate: e.detail.value as string });
  },

  onDeadlineTimeChange(e: WechatMiniprogram.PickerChange) {
    this.setData({ deadlineTime: e.detail.value as string });
  },

  buildIso(date: string, time: string): string {
    return new Date(`${date}T${time}:00`).toISOString();
  },

  async handleSubmit() {
    const {
      title, sportTags, sportTagIndex, startDate, startTime,
      deadlineDate, deadlineTime, latitude, longitude,
    } = this.data;

    if (!title.trim()) {
      wx.showToast({ title: '请输入标题', icon: 'none' });
      return;
    }
    if (!startDate || !startTime || !deadlineDate || !deadlineTime) {
      wx.showToast({ title: '请选择时间', icon: 'none' });
      return;
    }
    if (!latitude || !longitude) {
      wx.showToast({ title: '需要位置信息', icon: 'none' });
      return;
    }

    this.setData({ submitting: true });
    try {
      const startIso = this.buildIso(startDate, startTime);
      const endDate = new Date(startIso);
      endDate.setHours(endDate.getHours() + 2);
      const activity = await createActivity({
        title: title.trim(),
        description: this.data.description.trim(),
        sport_tag_id: sportTags[sportTagIndex].id,
        start_time: startIso,
        end_time: endDate.toISOString(),
        latitude,
        longitude,
        address: this.data.address.trim(),
        max_participants: this.data.maxParticipants,
        gender_requirement: this.data.genderIndex,
        registration_deadline: this.buildIso(deadlineDate, deadlineTime),
      });
      wx.showToast({ title: '发布成功', icon: 'success' });
      setTimeout(() => {
        wx.redirectTo({ url: `/pages/activity/detail/detail?id=${activity.id}` });
      }, 500);
    } catch (err) {
      wx.showToast({
        title: err instanceof Error ? err.message : '发布失败',
        icon: 'none',
      });
    } finally {
      this.setData({ submitting: false });
    }
  },
});
