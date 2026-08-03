# sports-partner 运动搭子

微信小程序 + FastAPI 后端 + Vue3 管理后台，帮助用户发布运动活动、寻找附近运动伙伴。

## 技术栈

| 模块 | 技术 |
|------|------|
| 小程序 | 微信原生 + TypeScript |
| 后端 | Python FastAPI + SQLAlchemy + Alembic |
| 数据库 | MySQL 8.0 |
| 缓存 | Redis 7 |
| 管理后台 | Vue3 + Vite + Element Plus |

## 项目结构

```
sports-partner/
├── backend/      # FastAPI 后端
├── miniapp/      # 微信小程序
├── admin/        # Vue3 管理后台
├── tests/        # 集成测试
└── docs/         # 项目文档
```

## 快速开始

### 1. 启动基础设施

```bash
cp .env.example .env
docker compose up -d
```

### 2. 启动后端

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

健康检查：http://localhost:8000/health  
API 文档：http://localhost:8000/docs

### 3. 启动管理后台

```bash
cd admin
npm install
npm run dev
```

访问：http://localhost:5173

### 4. 小程序

使用微信开发者工具打开 `miniapp/` 目录，填入 AppID 后编译预览。

## 开发阶段

- [x] Phase 0 — 项目骨架
- [ ] Phase 1 — 用户系统
- [ ] Phase 2 — 活动模块
- [ ] Phase 3 — 匹配模块
- [ ] Phase 4 — 公共区域 + 管理后台
- [ ] Phase 5 — 完善与上线

## 许可证

MIT
