import { isLoggedIn, loginWithWechat, logout } from '../../utils/auth';
import { getMe, updateLocation, UserProfile } from '../../services/user';
import { getCurrentLocation } from '../../utils/location';

Page({
  data: {
    isLoggedIn: false,
    loading: false,
    user: null as UserProfile | null,
    genderText: '',
  },

  onShow() {
    this.refreshProfile();
  },

  async refreshProfile() {
    if (!isLoggedIn()) {
      this.setData({ isLoggedIn: false, user: null, genderText: '' });
      return;
    }

    this.setData({ loading: true, isLoggedIn: true });
    try {
      const user = await getMe();
      this.setData({
        user,
        genderText: this.formatGender(user.gender),
        loading: false,
      });
    } catch {
      this.setData({ isLoggedIn: false, user: null, loading: false });
    }
  },

  formatGender(gender: number): string {
    const map: Record<number, string> = { 0: '未知', 1: '男', 2: '女' };
    return map[gender] || '未知';
  },

  async handleLogin() {
    this.setData({ loading: true });
    try {
      await loginWithWechat();
      await this.refreshProfile();
      wx.showToast({ title: '登录成功', icon: 'success' });
    } catch (err) {
      wx.showToast({
        title: err instanceof Error ? err.message : '登录失败',
        icon: 'none',
      });
      this.setData({ loading: false });
    }
  },

  handleLogout() {
    logout();
    this.setData({ isLoggedIn: false, user: null, genderText: '' });
    wx.showToast({ title: '已退出', icon: 'none' });
  },

  goSettings() {
    wx.navigateTo({ url: '/pages/settings/settings' });
  },

  async reportLocation() {
    try {
      const loc = await getCurrentLocation();
      await updateLocation(loc.latitude, loc.longitude);
      wx.showToast({ title: '位置已更新', icon: 'success' });
      this.refreshProfile();
    } catch (err) {
      wx.showToast({
        title: err instanceof Error ? err.message : '定位失败',
        icon: 'none',
      });
    }
  },
});
