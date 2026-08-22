import { getMe, getSportTags, updateMe, SportTag, UserProfile } from '../../services/user';

Page({
  data: {
    loading: true,
    saving: false,
    nickname: '',
    bio: '',
    gender: 0,
    genderOptions: ['未知', '男', '女'],
    sportTags: [] as SportTag[],
    selectedTagIds: [] as number[],
  },

  onLoad() {
    this.loadData();
  },

  async loadData() {
    this.setData({ loading: true });
    try {
      const [user, sportTags] = await Promise.all([getMe(), getSportTags()]);
      this.setData({
        nickname: user.nickname,
        bio: user.bio,
        gender: user.gender,
        sportTags,
        selectedTagIds: user.sport_tags.map((t) => t.id),
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

  onNicknameInput(e: WechatMiniprogram.Input) {
    this.setData({ nickname: e.detail.value });
  },

  onBioInput(e: WechatMiniprogram.Input) {
    this.setData({ bio: e.detail.value });
  },

  onGenderChange(e: WechatMiniprogram.PickerChange) {
    this.setData({ gender: Number(e.detail.value) });
  },

  toggleTag(e: WechatMiniprogram.TouchEvent) {
    const id = Number(e.currentTarget.dataset.id);
    const selected = [...this.data.selectedTagIds];
    const index = selected.indexOf(id);
    if (index >= 0) {
      selected.splice(index, 1);
    } else {
      selected.push(id);
    }
    this.setData({ selectedTagIds: selected });
  },

  isTagSelected(id: number): boolean {
    return this.data.selectedTagIds.includes(id);
  },

  async handleSave() {
    if (!this.data.nickname.trim()) {
      wx.showToast({ title: '请输入昵称', icon: 'none' });
      return;
    }

    this.setData({ saving: true });
    try {
      await updateMe({
        nickname: this.data.nickname.trim(),
        bio: this.data.bio.trim(),
        gender: this.data.gender,
        sport_tag_ids: this.data.selectedTagIds,
      });
      wx.showToast({ title: '保存成功', icon: 'success' });
      setTimeout(() => wx.navigateBack(), 500);
    } catch (err) {
      wx.showToast({
        title: err instanceof Error ? err.message : '保存失败',
        icon: 'none',
      });
    } finally {
      this.setData({ saving: false });
    }
  },
});
