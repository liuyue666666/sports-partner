# 部署指南

## 本地开发

1. 启动 MySQL + Redis：`docker compose up -d`
2. 复制环境变量：`cp .env.example .env`
3. 后端：`cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload`
4. 管理后台：`cd admin && npm install && npm run dev`
5. 小程序：微信开发者工具打开 `miniapp/`

## 生产部署（免费优先）

### 方案 A：单机 Docker

- 云服务器试用（阿里云/腾讯云新用户）
- Docker Compose 运行 MySQL、Redis、FastAPI、Nginx 静态托管 admin 构建产物

### 方案 B：本地服务器 + 内网穿透

- 适合面试演示
- 使用 frp / ngrok 暴露 API（注意微信小程序域名白名单）

## 环境变量

生产环境务必修改：

- `APP_SECRET_KEY`
- `JWT_SECRET_KEY`
- `MYSQL_PASSWORD`
- `ADMIN_DEFAULT_PASSWORD`
