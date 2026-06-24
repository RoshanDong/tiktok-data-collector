# Research: Feishu Bitable Auto-Upload

**Date**: 2026-06-17
**Feature**: Feishu Bitable Auto-Upload

## 技术调研

### Feishu API 端点

**1. 获取 tenant_access_token**
- URL: `POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal`
- Content-Type: `application/json`
- 请求体:
```json
{
  "app_id": "cli_xxx",
  "app_secret": "xxx"
}
```
- 响应:
```json
{
  "code": 0,
  "tenant_access_token": "xxx",
  "expire": 7200
}
```
- Token 有效期: 7200 秒 (2小时)

**2. 创建多维表格**
- URL: `POST https://open.feishu.cn/open-apis/bitable/v1/apps`
- Authorization: `Bearer {tenant_access_token}`
- Content-Type: `application/json`
- 请求体:
```json
{
  "name": "视频数据_2026-06-15"
}
```
- 响应:
```json
{
  "code": 0,
  "data": {
    "app": {
      "app_token": "S404bxxx",
      "default_table_id": "tblxxx",
      "name": "视频数据_2026-06-15",
      "url": "https://feishu.cn/base/xxx"
    }
  }
}
```

**3. 批量新增记录**
- URL: `POST https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/batch_create`
- Authorization: `Bearer {tenant_access_token}`
- Content-Type: `application/json`
- 请求体:
```json
{
  "records": [
    {
      "fields": {
        "Video ID": "7583962391013035294",
        "Title": "Your sign to try brown lashes",
        "GMV": 3696.00
      }
    }
  ]
}
```
- 限制: 每批最多 1000 条记录
- 错误码 1254104: 单次添加记录数量超限

### 关键决策

| 决策 | 选择 | 理由 |
|------|------|------|
| Token 管理 | 独立脚本 `feishu_token.py` | 独立管理飞书凭证 |
| Token 存储 | 缓存到 tiktok-config.json | 简单，符合项目风格 |
| 上传触发 | 集成到 export_video_performance.py | 自动执行 |
| 默认平台 | 飞书多维表格 | 用户指定 |

### 待用户提供

- Feishu app_id
- Feishu app_secret

## 备选方案

| 方案 | 优点 | 缺点 |
|------|------|------|
| A: 每次上传前获取 token | 无状态 | API 调用频繁 |
| B: 新增飞书 token 脚本 (已选) | 独立管理，清晰 | 新增一个脚本 |
