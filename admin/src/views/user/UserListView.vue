<template>
  <div>
    <h2>用户管理</h2>
    <el-table :data="[]" empty-text="暂无数据 — Phase 4 接入" style="margin-top: 16px">
      <el-table-column prop="id" label="ID" />
      <el-table-column prop="nickname" label="昵称" />
      <el-table-column prop="gender" label="性别" />
      <el-table-column prop="status" label="状态" />
      <el-table-column label="操作" />
    </el-table>
  </div>
</template>

<script setup lang="ts"></script>
