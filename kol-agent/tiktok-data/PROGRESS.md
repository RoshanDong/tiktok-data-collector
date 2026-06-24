# TikTok Data Fetch - 进度记录

**最后更新**: 2026-06-18
**状态**: ✅ 飞书多维表格上传功能已完成

---

## 已完成

### Orders API 测试 (specs/002-orders-api-test-automation)

| 阶段 | 任务 | 状态 |
|------|------|------|
| Phase 1-3 | 基础设施 + 核心 API | ✅ 完成 |
| Phase 5 | 严格响应验证 | ✅ 完成 |
| Phase N | Polish | ✅ 完成 |

**API 测试进度**: 17/19 任务完成

### 核心 API 测试结果

| API | 版本 | 状态 |
|-----|------|------|
| Get Order List | 202309 | ✅ 成功 |
| Get Order Detail | 202507 | ✅ 成功 |
| Get Price Detail | 202407 | ✅ 成功 |

### Video Performance API 测试 (specs/003-video-performance-exporter)

| 阶段 | 任务 | 状态 |
|------|------|------|
| Phase 1 | Setup | ✅ 完成 |
| Phase 2 | Foundational | ✅ 完成 |
| Phase 3 | US1: Daily Export | ✅ 完成 |
| Phase 4 | US2: Directory Structure | ✅ 完成 |
| Phase 5 | US3: Progress & Error Reporting | ✅ 完成 |
| Phase N | Polish | ✅ 完成 |

**视频数据导出**: ✅ 已完成 (18/18 任务)

### Video Performance Exporter

| API | 版本 | 状态 |
|-----|------|------|
| Get Shop Video Performance | 202605 | ✅ 成功 |

---

## 飞书多维表格上传功能 ✅

### 功能完成时间
2026-06-18

### 新增/修改的脚本

| 脚本 | 说明 | 状态 |
|------|------|------|
| `feishu_token.py` | 获取 Feishu tenant_access_token | ✅ 完成 |
| `feishu_uploader.py` | 飞书多维表格上传模块 | ✅ 完成 |
| `feishu_refresh_token.py` | user_access_token 刷新脚本 | ✅ 完成 |

### 飞书 OAuth 配置

| 配置项 | 值 |
|--------|-----|
| app_id | `cli_a925c3bd4ef8dbdb` |
| app_secret | `已配置` |
| user_access_token | ✅ 已获取并保存 |
| refresh_token | ✅ 已获取并保存（有效期7天） |
| folder_token | `JMyuwo75xiH7czksrQLcGGO9nPS` |

### 授权 Scope

```
offline_access base:app:create base:app:copy base:app:read base:app:update
base:field:create base:field:delete base:field:read base:field:update
base:record:create base:record:delete base:record:retrieve base:record:update
base:workspace:list base:table:create base:table:delete base:table:read base:table:update
```

### feishu_uploader.py 功能

| 功能 | 状态 |
|------|------|
| 创建多维表格 | ✅ |
| 同步字段（删除默认字段 + 创建自定义字段） | ✅ |
| 删除空白记录（新建表格自带10条） | ✅ |
| 批量上传记录（每批1000条） | ✅ |
| 复用 feishu_refresh_token.py 刷新逻辑 | ✅ |

### feishu_refresh_token.py 功能

| 功能 | 状态 |
|------|------|
| 使用 refresh_token 刷新 user_access_token | ✅ |
| 保存新的 refresh_token（一次性） | ✅ |
| HTTP 错误处理 | ✅ |
| 日志记录 | ✅ |

### 测试结果

| 测试项 | 结果 |
|--------|------|
| 授权码获取 → user_access_token | ✅ 成功 |
| refresh_token 刷新 | ✅ 成功 |
| 刷新后保存新 refresh_token | ✅ 成功 |
| 上传 3479 条记录 | ✅ 成功 |
| 删除 10 条空白记录 | ✅ 成功 |

---

## API 授权状态

### TikTok API

| 步骤 | 状态 | 说明 |
|------|------|------|
| Step 1: 获取 auth_code | ✅ | 已完成 |
| Step 2: 获取 access_token | ✅ | 已完成 |
| Step 3: Token 刷新机制 | ✅ | 已配置 Cron |

### 飞书 API

| 步骤 | 状态 | 说明 |
|------|------|------|
| 获取授权码 | ✅ | 需在浏览器完成 |
| 获取 user_access_token | ✅ | 已完成 |
| 刷新 user_access_token | ✅ | feishu_refresh_token.py |

### 授权信息

| 字段 | TikTok | 飞书 |
|------|--------|------|
| Seller/用户 | VEYESBEAUTY | 董思渊 |
| Region | US | - |
| Granted Scopes | seller.order.info, seller.finance.info, data.shop_analytics.public.read, data.bestselling.public.read | bitable 全部权限 |

---

## 已创建/更新的文件

```
.kol-agent/
├── tiktok-config.json          # ✅ 已配置 (含 TikTok + DingTalk + Feishu access_token)
├── tiktok-data/
│   ├── logs/                   # 日志目录
│   ├── exports/                # 导出数据目录
│   └── PROGRESS.md            # 本文件
└── scripts/
    ├── export_video_performance.py  # ✅ 视频数据导出 + 自动上传钉钉/飞书
    ├── dingtalk_uploader.py        # ✅ 钉钉文件上传模块
    ├── dingtalk_token.py           # ✅ DingTalk Token 获取
    ├── feishu_uploader.py          # ✅ 飞书多维表格上传模块
    ├── feishu_token.py             # ✅ Feishu Token 获取
    ├── feishu_refresh_token.py     # ✅ Feishu user_access_token 刷新
    ├── refresh_token.py            # TikTok Token 刷新
    └── ... (其他模块)
```

---

## Cron 配置汇总

| 任务 | 执行时间 | 脚本 |
|------|----------|------|
| 视频数据抓取 + 上传钉钉 | 每天 06:00 | `.kol-agent/scripts/export_video_performance.py` |
| DingTalk Token 刷新 | 每周一 04:00 | `.kol-agent/scripts/dingtalk_token.py` |
| TikTok Token 刷新 | 每周一 04:00 | `.kol-agent/scripts/refresh_token.py` |
| **飞书 Token 刷新** | **每小时** | `.kol-agent/scripts/feishu_refresh_token.py` |

> ⚠️ 飞书 user_access_token 有效期 2 小时，refresh_token 有效期 7 天。建议每小时刷新一次。

---

## 快速测试

```bash
# 导出视频数据并自动上传到钉钉（默认行为）
python3 .kol-agent/scripts/export_video_performance.py

# 仅导出不上传
python3 .kol-agent/scripts/export_video_performance.py --no-upload

# 导出并上传到飞书多维表格
python3 .kol-agent/scripts/feishu_uploader.py <excel文件路径> <日期>

# 手动上传指定日期的 Excel 到钉钉
python3 .kol-agent/scripts/export_video_performance.py --upload-only 2026-06-15

# 手动上传指定日期的 Excel 到飞书
python3 .kol-agent/scripts/feishu_uploader.py .kol-agent/tiktok-data/exports/video_performance_2026-06-15.xlsx 2026-06-15

# DingTalk Token 获取/刷新
python3 .kol-agent/scripts/dingtalk_token.py

# 飞书 user_access_token 刷新
python3 .kol-agent/scripts/feishu_refresh_token.py
```

---

## 历史问题排查

### 2026-06-11: invalid_client 错误
错误原因：使用了错误的授权流程。
解决：Partner Center → App → 授权链接 → 获取 auth_code → Step 2 获取 token

### 2026-06-12: 签名算法修复
问题：POST 请求签名格式错误
解决：POST 请求不包含 body 在签名中

---

## 2026-06-18: 飞书 user_access_token 集成

### 完成的功能

1. **OAuth 授权流程**
   - 生成授权 URL（含 offline_access scope）
   - 获取授权码 → user_access_token + refresh_token
   - 保存到配置文件

2. **Token 刷新机制**
   - feishu_refresh_token.py 独立脚本
   - feishu_uploader.py 复用刷新逻辑
   - 每次刷新保存新的 refresh_token（一次性）

3. **多维表格上传**
   - 创建多维表格
   - 同步字段（删除默认字段 + 创建19个自定义字段）
   - **删除空白记录**（新建表格自带10条）
   - 批量上传（每批1000条）

### 待优化
- [ ] 集成到 export_video_performance.py（添加 --feishu 参数）
- [ ] 配置飞书定时刷新 cron
- [ ] TikTok API SSL 连接不稳定问题（网络问题）

---

## 2026-06-17: 定时任务与导出逻辑优化

### 问题修复
| 问题 | 解决 |
|------|------|
| Cron 配置错误 | cron 指向 tiktok-fetch.py（订单）→ 已改为 export_video_performance.py |
| TikTok 数据延迟 | 默认抓取昨天，但 API 最新只有前天数据 |

### 新逻辑
| 功能 | 说明 |
|------|------|
| 获取最新日期 | 调用 API `latest_available_date` 字段 |
| 默认只抓取1天 | 不再默认抓取7天 |
| 检查已存在文件 | 存在则跳过并记录日志 |
| Cron 时间 | 每天 06:00 执行 (视频), 每周一 04:00 执行 (Token 刷新) |

---

## 2026-06-17: DingTalk Excel 自动上传

### 功能说明
每日视频数据拉取完成后，自动将 Excel 文件上传至钉钉。

### 新增脚本
| 脚本 | 说明 |
|------|------|
| `dingtalk_token.py` | 获取 DingTalk access_token |
| `dingtalk_uploader.py` | 钉钉文件上传模块 |

### 新增 CLI 参数
| 参数 | 说明 |
|------|------|
| `--upload` | 导出后上传到钉钉（默认开启） |
| `--no-upload` | 禁用上传到钉钉 |
| `--upload-only` | 仅上传指定日期的 Excel（不拉取数据） |

### 验证结果
| 测试项 | 状态 |
|--------|------|
| Token 获取 | ✅ 成功 |
| 文件上传 | ✅ 成功 |
| media_id | `@lAzPM23c8f5Lp0vOGz8g0c5NlJ_0` |

---

## 2026-06-17: 飞书多维表格上传功能 (开发中)

### 功能说明
每日视频数据拉取完成后，自动将 Excel 数据上传至飞书多维表格。

### 新增脚本
| 脚本 | 说明 |
|------|------|
| `feishu_token.py` | 获取 Feishu tenant_access_token |
| `feishu_uploader.py` | 飞书多维表格上传模块 |

### 飞书配置
| 配置项 | 值 |
|--------|-----|
| app_id | `cli_a925c3bd4ef8dbdb` |
| folder_token | `JMyuwo75xiH7czksrQLcGGO9nPS` |

### 开发进度
| 任务 | 状态 |
|------|------|
| T001 配置飞书凭证 | ✅ 完成 |
| T002 feishu_token.py | ✅ 完成 |
| T003 feishu_uploader.py | ✅ 完成 |
| T004 集成到 export_video_performance.py | ⏳ |
| T005 钉钉独立选项 | ⏳ |

### 待解决
- 飞书创建多维表格权限问题 (code 1254002)
- 需在飞书开放平台开通 `bitable:app` 或 `base:app:create` 权限并发布
