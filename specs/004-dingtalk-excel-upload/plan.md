# Implementation Plan: DingTalk Excel Auto-Upload

**Branch**: `004-dingtalk-excel-upload` | **Date**: 2026-06-17 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification for DingTalk Excel auto-upload

## Summary

为 `export_video_performance.py` 添加钉钉文档上传功能。每日视频数据拉取完成后，自动将 Excel 文件上传至钉钉。使用独立的 token 获取脚本管理钉钉 access_token。

## Technical Context

**Language/Version**: Python 3.9

**Primary Dependencies**:
- `requests` (已有)
- `openpyxl` (已有)
- DingTalk API: `media/upload` + `gettoken`

**Storage**: 本地文件系统 (`.kol-agent/tiktok-data/exports/`)

**Testing**: 手动 API 测试 + cron 验证

**Target Platform**: Linux/macOS (cron 定时任务)

**Project Type**: CLI 脚本扩展

**Performance Goals**: 上传完成时间 < 60 秒

**Scale/Scope**: 每日单文件上传 (最大 20MB)

## Constitution Check

✅ **GATE PASSED**: 
- 简单优先: 仅添加必要功能，不引入额外复杂度
- 外科手术式改动: 只修改 `export_video_performance.py`，新增独立模块
- 目标驱动: 成功标准已明确定义 (media_id 记录、上传日志)

## Project Structure

### Documentation (this feature)

```text
specs/004-dingtalk-excel-upload/
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
├── dingtalk_uploader.py          # 新增: 钉钉上传模块
├── dingtalk_token.py             # 新增: 钉钉 Token 获取
├── tiktok_api_client.py           # 已有
├── excel_writer.py                # 已有
└── ...
```

**Structure Decision**: 在现有 `.kol-agent/scripts/` 下新增两个 Python 模块:
- `dingtalk_token.py`: 独立的 Token 获取脚本
- `dingtalk_uploader.py`: 钉钉上传功能模块

## Phase 0: Research

### 技术调研

**DingTalk API 端点**:
- Token: `GET https://oapi.dingtalk.com/gettoken?appkey=xxx&appsecret=xxx`
- 上传: `POST https://oapi.dingtalk.com/media/upload`

**上传参数**:
- `access_token`: 查询参数
- `type`: "file" (Excel)
- `media`: multipart/form-data 文件

**响应**:
```json
{
  "errcode": 0,
  "errmsg": "ok",
  "media_id": "xxx",
  "created_at": 1599556098964,
  "type": "file"
}
```

### 待用户确认
- [ ] 提供 DingTalk appkey 和 appsecret

## Phase 1: Design

### data-model.md

**实体**:

| 实体 | 字段 | 说明 |
|------|------|------|
| DingTalkConfig | appkey, appsecret | 凭证配置 |
| UploadRequest | file_path, media_id, timestamp | 上传请求/响应 |
| UploadResult | errcode, errmsg, media_id, created_at | 上传结果 |

### quickstart.md

1. 配置钉钉凭证到 `tiktok-config.json`
2. 运行 `python3 dingtalk_token.py` 获取/刷新 token
3. 运行 `python3 export_video_performance.py --upload` 测试上传
4. 验证日志中的 media_id

## Phase 2: Tasks

详见 `tasks.md`

### Task List (概要)

1. **dingtalk_token.py**: 创建 Token 获取模块
   - 调用 `gettoken` API
   - 缓存 token 到配置文件
   - 支持 refresh

2. **dingtalk_uploader.py**: 创建上传模块
   - `upload_file()`: 上传单个文件
   - `upload_excel()`: 上传 Excel 并记录 media_id

3. **export_video_performance.py**: 集成上传
   - 拉取完成后调用上传
   - 添加 `--upload` 参数支持手动触发

4. **测试验证**
   - 手动上传测试
   - 验证 media_id 返回

## Complexity Tracking

无需追踪 - 无 Constitution 违规
