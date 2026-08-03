Page({
  data: {
    activityId: '',
  },

  onLoad(options: Record<string, string | undefined>) {
    this.setData({ activityId: options.id || '' });
  },
});
