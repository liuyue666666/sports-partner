<template>
  <div>
    <div class="toolbar">
      <h2>公共区域管理</h2>
      <el-button type="primary" disabled>新增区域（Phase 4）</el-button>
    </div>
    <el-table :data="[]" empty-text="暂无数据 — Phase 4 接入">
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="sport_type" label="运动类型" />
      <el-table-column prop="sort_order" label="排序" />
      <el-table-column prop="is_visible" label="首页展示" />
      <el-table-column label="操作" />
    </el-table>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
</style>
