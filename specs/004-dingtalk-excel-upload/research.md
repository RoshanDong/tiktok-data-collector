# Research: DingTalk Excel Auto-Upload

**Date**: 2026-06-17
**Feature**: DingTalk Excel Auto-Upload

## 技术调研

### DingTalk API 端点

**1. 获取 access_token**
- URL: `GET https://oapi.dingtalk.com/gettoken`
- 参数: `appkey`, `appsecret` (query string)
- 响应:
```json
{
  "errcode": 0,
  "access_token": "xxx",
  "errmsg": "ok",
  "expires_in": 7200
}
```
- Token 有效期: 7200 秒 (2小时)

**2. 上传媒体文件**
- URL: `POST https://oapi.dingtalk.com/media/upload`
- Content-Type: `multipart/form-data;charset=utf-8`
- 参数 (form-data):
  - `access_token`: 应用凭证
  - `type`: 媒体类型 (`image`, `voice`, `video`, `file`)
  - `media`: 文件
- 响应:
```json
{
  "errcode": 0,
  "errmsg": "ok",
  "media_id": "xxx",
  "created_at": 1599556098964,
  "type": "file"
}
```

### 关键决策

| 决策 | 选择 | 理由 |
|------|------|------|
| Token 管理 | 独立脚本 `dingtalk_token.py` | 复用现有 config 结构 |
| Token 存储 | 缓存到 tiktok-config.json | 简单，符合项目风格 |
| 上传触发 | 集成到 export_video_performance.py | 自动执行 |
| 手动触发 | 添加 `--upload` CLI 参数 | 支持重试和回填 |

### 待用户提供

- DingTalk appkey
- DingTalk appsecret

## 备选方案

| 方案 | 优点 | 缺点 |
|------|------|------|
| A: 复用现有 token 刷新逻辑 | 代码复用 | 需要钉钉单独的凭证 |
| B: 新增钉钉 token 脚本 (已选) | 独立管理，清晰 | 新增一个脚本 |
| C: 每次上传前获取 token | 无状态 | API 调用频繁 |
