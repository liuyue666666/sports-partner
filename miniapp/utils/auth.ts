import { request, setToken, clearToken } from './request';

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  is_new_user: boolean;
}

export function loginWithWechat(): Promise<TokenResponse> {
  return new Promise((resolve, reject) => {
    wx.login({
      success: async (res) => {
        if (!res.code) {
          reject(new Error('微信登录失败'));
          return;
        }
        try {
          const data = await request<TokenResponse>({
            url: '/auth/wechat/login',
            method: 'POST',
            data: { code: res.code },
            auth: false,
          });
          setToken(data.access_token);
          wx.setStorageSync('refresh_token', data.refresh_token);
          resolve(data);
        } catch (err) {
          reject(err);
        }
      },
      fail: (err) => reject(new Error(err.errMsg || '微信登录失败')),
    });
  });
}

export function logout(): void {
  clearToken();
  wx.removeStorageSync('refresh_token');
}

export function isLoggedIn(): boolean {
  return !!wx.getStorageSync('access_token');
}
