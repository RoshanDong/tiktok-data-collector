# Data Model: Feishu Bitable Auto-Upload

## 实体定义

### FeishuConfig

飞书应用凭证配置。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| app_id | string | 是 | 飞书应用的 Client ID |
| app_secret | string | 是 | 飞书应用的 Client Secret |
| tenant_access_token | string | 否 | 当前有效的 tenant_access_token |
| token_expires_at | number | 否 | token 过期时间戳 |

### BitableInfo

创建的多维表格信息。

| 字段 | 类型 | 说明 |
|------|------|------|
| app_token | string | 多维表格的唯一标识 |
| table_id | string | 默认数据表的 ID |
| name | string | 多维表格名称 |
| url | string | 多维表格 URL |

### UploadRecord

单条上传记录 (对应 Excel 一行)。

| 字段 | 类型 | 说明 |
|------|------|------|
| video_id | string | 视频 ID |
| title | string | 视频标题 |
| username | string | 用户名 |
| creator_user_name | string | 创作者用户名 |
| creator_nick_name | string | 创作者昵称 |
| creator_author_type | string | 创作者类型 |
| video_post_time | string | 发布时间 |
| duration | number | 时长 (秒) |
| hash_tags | string | 话题标签 |
| gmv_amount | number | GMV 金额 |
| gmv_currency | string | GMV 货币 |
| gpm_amount | number | GPM 金额 |
| gpm_currency | string | GPM 货币 |
| avg_customers | number | 平均客户数 |
| sku_orders | number | SKU 订单数 |
| items_sold | number | 商品销量 |
| views | number | 观看数 |
| click_through_rate | string | 点击率 |
| products | string | 关联商品 |

### UploadResult

上传结果。

| 字段 | 类型 | 说明 |
|------|------|------|
| success | boolean | 是否成功 |
| bitable_url | string | 多维表格 URL |
| record_count | number | 上传记录数 |
| error | string | 错误信息 (失败时) |

## 日志记录

每次上传操作记录:
- 时间戳
- 数据日期
- Bitable URL
- 上传记录数
- 错误信息 (失败时)
