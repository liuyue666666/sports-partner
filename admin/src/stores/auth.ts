import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('admin_token') || '');

  function setToken(value: string) {
    token.value = value;
    localStorage.setItem('admin_token', value);
  }

  function clearToken() {
    token.value = '';
    localStorage.removeItem('admin_token');
  }

  return { token, setToken, clearToken };
});
