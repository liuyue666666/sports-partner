<template>
  <div class="login-page">
    <el-card class="login-card">
      <h2>运动搭子 · 管理后台</h2>
      <p class="hint">Phase 4 接入管理员登录 API</p>
      <el-form @submit.prevent="handleLogin">
        <el-form-item label="用户名">
          <el-input v-model="username" placeholder="admin" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="password" type="password" placeholder="admin123" show-password />
        </el-form-item>
        <el-button type="primary" native-type="submit" style="width: 100%">登录（演示）</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('admin');
const password = ref('');

function handleLogin() {
  localStorage.setItem('admin_token', 'demo-token');
  router.push('/dashboard');
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f2f5;
}

.login-card {
  width: 400px;
}

.hint {
  color: #999;
  font-size: 13px;
  margin-bottom: 24px;
}
</style>
