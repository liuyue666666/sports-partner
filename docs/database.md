# 数据库设计

Phase 0 仅初始化 Alembic，表结构在 Phase 1 起逐步迁移。

## 核心表（规划）

- `users` — 用户
- `sport_tags` / `user_sport_tags` — 运动标签
- `activities` / `activity_participants` — 活动与报名
- `regions` — 公共活动区域
- `messages` — 站内消息（Phase 1+）
- `admins` — 管理员

## 迁移命令

```bash
cd backend
alembic upgrade head
alembic revision --autogenerate -m "describe change"
```

## Redis 结构（规划）

| Key | 类型 | 用途 |
|-----|------|------|
| `user:geo` | GEO | 用户实时位置 |
| `activity:geo:recruiting` | GEO | 招募中活动 |
| `user:online:{id}` | STRING | 在线状态 TTL 5min |
