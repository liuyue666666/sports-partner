import axios from 'axios';

const request = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,
});

request.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.message || error.message || '请求失败';
    return Promise.reject(new Error(message));
  },
);

export default request;
