const TOKEN_KEY = 'access_token';

interface RequestOptions {
  url: string;
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  data?: Record<string, unknown>;
  auth?: boolean;
}

interface ApiResponse<T = unknown> {
  code?: string;
  message?: string;
  data?: T;
}

function getBaseUrl(): string {
  const app = getApp<{ globalData: { apiBaseUrl: string } }>();
  return app.globalData.apiBaseUrl;
}

export function request<T = unknown>(options: RequestOptions): Promise<T> {
  const { url, method = 'GET', data, auth = true } = options;
  const header: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (auth) {
    const token = wx.getStorageSync(TOKEN_KEY);
    if (token) {
      header.Authorization = `Bearer ${token}`;
    }
  }

  return new Promise((resolve, reject) => {
    wx.request({
      url: `${getBaseUrl()}${url}`,
      method,
      data,
      header,
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data as T);
        } else {
          const body = res.data as ApiResponse;
          reject(new Error(body.message || `HTTP ${res.statusCode}`));
        }
      },
      fail(err) {
        reject(new Error(err.errMsg || 'Network error'));
      },
    });
  });
}

export function setToken(token: string): void {
  wx.setStorageSync(TOKEN_KEY, token);
}

export function clearToken(): void {
  wx.removeStorageSync(TOKEN_KEY);
}

export function getToken(): string {
  return wx.getStorageSync(TOKEN_KEY) || '';
}
