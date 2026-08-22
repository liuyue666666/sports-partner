# API 文档（Phase 1）

Swagger：http://localhost:8000/docs

## 认证

### POST /api/v1/auth/wechat/login

微信登录。未配置 `WECHAT_APP_ID` 时使用开发模式（code 哈希生成 mock openid）。

```json
{ "code": "wx_login_code" }
```

响应：

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer",
  "is_new_user": true
}
```

### POST /api/v1/auth/refresh

刷新 Token。

## 用户

请求头：`Authorization: Bearer <access_token>`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/users/me | 当前用户资料 |
| PUT | /api/v1/users/me | 更新资料 |
| POST | /api/v1/users/location | 上报 GPS 位置 |
| GET | /api/v1/users/{id} | 公开资料 |

### PUT /api/v1/users/me 示例

```json
{
  "nickname": "小明",
  "gender": 1,
  "bio": "喜欢徒步",
  "sport_tag_ids": [1, 2, 5]
}
```

性别：`0` 未知 · `1` 男 · `2` 女

### POST /api/v1/users/location 示例

```json
{ "latitude": 22.5431, "longitude": 114.0579 }
```

## 运动标签

### GET /api/v1/sport-tags

返回全部运动标签（无需登录）。
