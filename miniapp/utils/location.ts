export interface LocationResult {
  latitude: number;
  longitude: number;
}

export function getCurrentLocation(): Promise<LocationResult> {
  return new Promise((resolve, reject) => {
    wx.getLocation({
      type: 'gcj02',
      success(res) {
        resolve({ latitude: res.latitude, longitude: res.longitude });
      },
      fail(err) {
        reject(new Error(err.errMsg || '获取位置失败'));
      },
    });
  });
}

export function formatDistance(meters: number): string {
  if (meters < 1000) {
    return `${Math.round(meters)}m`;
  }
  return `${(meters / 1000).toFixed(1)}km`;
}
