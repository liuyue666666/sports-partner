<template>
  <div>
    <h2>活动管理</h2>
    <el-table :data="[]" empty-text="暂无数据 — Phase 4 接入" style="margin-top: 16px">
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="creator" label="发起人" />
      <el-table-column prop="start_time" label="开始时间" />
      <el-table-column prop="status" label="状态" />
      <el-table-column label="操作" />
    </el-table>
  </div>
</template>

<script setup lang="ts"></script>
