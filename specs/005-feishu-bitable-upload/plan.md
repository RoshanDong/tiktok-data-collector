# Implementation Plan: Feishu Bitable Auto-Upload

**Branch**: `005-feishu-bitable-upload` | **Date**: 2026-06-17 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification for Feishu Bitable auto-upload

## Summary

为 `export_video_performance.py` 添加飞书多维表格上传功能。每日视频数据拉取完成后，自动创建飞书多维表格并分批上传记录（每批最多1000条）。保留钉钉上传作为独立选项。

## Technical Context

**Language/Version**: Python 3.9

**Primary Dependencies**:
- `requests` (已有)
- `openpyxl` (已有)
- Feishu API: `auth/v3/tenant_access_token`, `bitable/v1/apps`

**Storage**: 本地文件系统 (`.kol-agent/tiktok-data/exports/`)

**Testing**: 手动 API 测试 + cron 验证

**Target Platform**: Linux/macOS (cron 定时任务)

**Project Type**: CLI 脚本扩展

**Performance Goals**: 上传完成时间 < 300 秒 (5000条记录)

**Scale/Scope**: 每日单次上传，最多 20,000 条记录

## Constitution Check

✅ **GATE PASSED**:
- 简单优先: 仅添加必要功能，不引入额外复杂度
- 外科手术式改动: 只修改 `export_video_performance.py`，新增独立模块
- 目标驱动: 成功标准已明确定义 (bitable URL 记录、总数校验)

## Project Structure

### Documentation (this feature)

```text
specs/005-feishu-bitable-upload/
├── plan.md              # 本文件
├── spec.md              # 功能规范
├── research.md          # Phase 0 研究
├── data-model.md        # 数据模型
├── quickstart.md        # 快速验证指南
└── tasks.md             # 任务分解 (Phase 2)
```

### Source Code (.kol-agent/scripts/)

```text
.kol-agent/scripts/
├── export_video_performance.py    # 主脚本 (修改)
├── feishu_uploader.py             # 新增: 飞书上件模块
├── feishu_token.py               # 新增: 飞书 Token 获取
├── dingtalk_uploader.py           # 已有
├── dingtalk_token.py             # 已有
├── tiktok_api_client.py           # 已有
└── ...
```

**Structure Decision**: 在现有 `.kol-agent/scripts/` 下新增两个 Python 模块:
- `feishu_token.py`: 独立的 Token 获取脚本
- `feishu_uploader.py`: 飞书多维表格上传模块

## Phase 0: Research

### 技术调研

**Feishu API 端点**:

1. **获取 tenant_access_token**
   - URL: `POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal`
   - 请求体: `{"app_id": "xxx", "app_secret": "xxx"}`
   - 响应: `{"code": 0, "tenant_access_token": "xxx", "expire": 7200}`

2. **创建多维表格**
   - URL: `POST https://open.feishu.cn/open-apis/bitable/v1/apps`
   - 请求体: `{"name": "多维表格名称"}`
   - 响应: `{"code": 0, "data": {"app_token": "xxx", "default_table_id": "xxx", "url": "xxx"}}`

3. **批量新增记录**
   - URL: `POST https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/batch_create`
   - 请求体: `{"records": [{"fields": {...}}, ...]}`
   - 限制: 每批最多 1000 条记录

### 待用户确认
- [ ] 提供 Feishu app_id 和 app_secret

## Phase 1: Design

### data-model.md

**实体**:

| 实体 | 字段 | 说明 |
|------|------|------|
| FeishuConfig | app_id, app_secret | 凭证配置 |
| BitableInfo | app_token, table_id, name, url | 创建的多维表格信息 |
| UploadResult | record_count, bitable_url, errors | 上传结果 |

### quickstart.md

1. 配置飞书凭证到 `tiktok-config.json`
2. 运行 `python3 feishu_token.py` 测试 token 获取
3. 运行 `python3 export_video_performance.py` 测试上传
4. 验证日志中的 bitable_url

## Phase 2: Tasks

详见 `tasks.md`

### Task List (概要)

1. **feishu_token.py**: 创建 Token 获取模块
   - 调用 `POST /open-apis/auth/v3/tenant_access_token/internal`
   - 缓存 token 到配置文件

2. **feishu_uploader.py**: 创建上传模块
   - `create_bitable()`: 创建多维表格
   - `upload_batch()`: 分批上传记录
   - 校验上传总数与 Excel 行数一致

3. **export_video_performance.py**: 集成上传
   - 拉取完成后调用飞书上件
   - 添加 `--feishu` 参数启用飞书上件
   - 添加 `--dingtalk` 参数启用钉钉上件

4. **测试验证**
   - 手动上件测试
   - 验证 bitable URL 和记录数

## Complexity Tracking

无需追踪 - 无 Constitution 违规
