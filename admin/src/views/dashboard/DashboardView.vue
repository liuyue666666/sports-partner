<template>
  <div>
    <h2>仪表盘</h2>
    <el-row :gutter="16" style="margin-top: 24px">
      <el-col :span="6">
        <el-card shadow="hover"><el-statistic title="用户数" :value="0" /></el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"><el-statistic title="活动数" :value="0" /></el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"><el-statistic title="公共区域" :value="0" /></el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"><el-statistic title="今日活跃" :value="0" /></el-card>
      </el-col>
    </el-row>
    <el-alert
      style="margin-top: 24px"
      title="Phase 0 骨架 — 数据统计将在后续阶段接入"
      type="info"
      :closable="false"
    />
  </div>
</template>

<script setup lang="ts"></script>
