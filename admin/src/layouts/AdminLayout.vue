<template>
  <el-container class="layout">
    <el-aside width="220px" class="aside">
      <div class="logo">运动搭子</div>
      <el-menu :default-active="route.path" router background-color="#001529" text-color="#fff">
        <el-menu-item index="/dashboard">仪表盘</el-menu-item>
        <el-menu-item index="/regions">公共区域</el-menu-item>
        <el-menu-item index="/users">用户管理</el-menu-item>
        <el-menu-item index="/activities">活动管理</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span>管理后台</span>
        <el-button link type="primary" @click="logout">退出</el-button>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

function logout() {
  localStorage.removeItem('admin_token');
  router.push('/login');
}
</script>

<style scoped>
.layout {
  height: 100vh;
}

.aside {
  background: #001529;
}

.logo {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  padding: 20px 16px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #eee;
  background: #fff;
}
</style>
