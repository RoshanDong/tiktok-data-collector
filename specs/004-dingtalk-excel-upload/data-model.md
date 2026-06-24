# Data Model: DingTalk Excel Auto-Upload

## 实体定义

### DingTalkConfig

钉钉应用凭证配置。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appkey | string | 是 | 钉钉应用的 Client ID |
| appsecret | string | 是 | 钉钉应用的 Client Secret |
| access_token | string | 否 | 当前有效的 access_token |
| token_expires_at | number | 否 | token 过期时间戳 |

### UploadRequest

上传请求。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file_path | string | 是 | 本地 Excel 文件路径 |
| date | string | 是 | 数据日期 (YYYY-MM-DD) |

### UploadResult

上传结果。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| errcode | number | 是 | 错误码，0 表示成功 |
| errmsg | string | 是 | 错误消息 |
| media_id | string | 是 | 上传成功后返回的媒体 ID |
| created_at | number | 是 | 上传时间戳 |
| type | string | 是 | 媒体类型 (file) |

## 日志记录

每次上传操作记录:
- 时间戳
- 文件路径
- 日期
- media_id (成功时)
- 错误信息 (失败时)
