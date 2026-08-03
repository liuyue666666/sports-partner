# 架构说明

详见项目 README 与 Phase 0 设计文档。

## 模块

| 模块 | 路径 | 说明 |
|------|------|------|
| 后端 API | `backend/app/api/v1/` | REST 接口 |
| 业务逻辑 | `backend/app/services/` | Service 层 |
| 数据访问 | `backend/app/repositories/` | Repository 层 |
| 小程序 | `miniapp/` | 微信原生 + TS |
| 管理后台 | `admin/` | Vue3 + Element Plus |

## 匹配算法（已确认）

```
匹配度 = 0.4 × 距离分 + 0.4 × 兴趣分 + 0.2 × 时间分
默认搜索半径：5km
```

距离计算：Haversine 公式（`backend/app/utils/geo.py`）

## MVP 约束

- 无地图 SDK，仅 GPS 经纬度
- 无微信订阅消息，站内消息存数据库
- 活动发布无需审核，直接上线
