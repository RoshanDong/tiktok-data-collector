# Tasks: DingTalk Excel Auto-Upload

**Input**: Design documents from `specs/004-dingtalk-excel-upload/`

**Prerequisites**: plan.md, spec.md (user stories), research.md, data-model.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行执行（不同文件，无依赖）
- **[Story]**: 用户故事编号 (US1, US2)
- 描述中包含具体文件路径

---

## Phase 1: Setup (基础配置)

**Purpose**: 配置钉钉凭证

- [x] T001 在 `tiktok-config.json` 中添加 `dingtalk` 配置段，包含 `appkey` 和 `appsecret` 字段 ✅

---

## Phase 2: Foundational (核心模块)

**Purpose**: 创建钉钉 Token 获取模块（US1 和 US2 都依赖此模块）

- [x] T002 创建 `.kol-agent/scripts/dingtalk_token.py` - Token 获取脚本 ✅
  - 调用 `GET https://oapi.dingtalk.com/gettoken?appkey=xxx&appsecret=xxx`
  - 将 token 和过期时间缓存到 `tiktok-config.json`
  - 添加日志记录

---

## Phase 3: User Story 1 - 自动化每日上传 (Priority: P1) 🎯 MVP

**Goal**: 每日视频数据拉取完成后，自动将 Excel 文件上传至钉钉

**Independent Test**: 运行 cron 任务，验证日志中显示 media_id

### Implementation for User Story 1

- [x] T003 [P] 创建 `.kol-agent/scripts/dingtalk_uploader.py` - 钉钉上传模块 ✅
  - 实现 `upload_file()` 函数
  - 使用 multipart/form-data 格式
  - 设置 type="file"
  - 记录返回的 media_id

- [x] T004 修改 `.kol-agent/scripts/export_video_performance.py` ✅
  - 在 `export_date()` 函数成功后调用 `dingtalk_uploader`
  - 添加 `--upload` CLI 参数（默认开启）
  - 添加上传成功/失败的日志记录

**Checkpoint**: 每日 06:00 cron 任务完成后，Excel 自动上传至钉钉

---

## Phase 4: User Story 2 - 手动上传触发 (Priority: P2)

**Goal**: 管理员可手动触发指定日期文件的上传

**Independent Test**: 运行 `python3 export_video_performance.py --date 2026-06-15 --upload-only`，验证上传

### Implementation for User Story 2

- [ ] T005 修改 `.kol-agent/scripts/export_video_performance.py`
  - 添加 `--upload-only` 参数（仅上传，不拉取数据）
  - 添加 `--date` 参数支持指定日期

**Checkpoint**: 手动传入日期参数，可上传历史数据

---

## Phase 5: Polish & 验证

**Purpose**: 验证和文档

- [x] T006 运行 `python3 .kol-agent/scripts/dingtalk_token.py` 测试 token 获取 ✅
- [x] T007 运行 `python3 .kol-agent/scripts/export_video_performance.py --upload-only` 测试上传 ✅
- [x] T008 验证日志中的 media_id 是否正确记录 ✅

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 无依赖
- **Phase 2 (Foundational)**: 依赖 Phase 1 完成
- **Phase 3 (US1)**: 依赖 Phase 2 完成
- **Phase 4 (US2)**: 依赖 Phase 3 完成
- **Phase 5 (Polish)**: 依赖 Phase 3 或 Phase 4 完成

### User Story Dependencies

- **User Story 1 (P1)**: 必须在 Phase 2 完成后开始
- **User Story 2 (P2)**: 必须在 Phase 3 完成后开始

### Parallel Opportunities

- Phase 2 的 T002 无并行任务（单一模块）
- Phase 3 的 T003 可在 T002 完成后独立进行
- Phase 5 的验证任务可并行执行

---

## Implementation Strategy

### MVP (User Story 1 Only)

1. 完成 Phase 1: 配置钉钉凭证
2. 完成 Phase 2: 创建 dingtalk_token.py
3. 完成 Phase 3: 创建 uploader + 集成
4. **验证**: 日志显示 media_id

### Incremental Delivery

1. Setup + Foundational → 基础就绪
2. 添加 US1 → 测试验证 → MVP 完成
3. 添加 US2 → 支持手动上传

---

## Notes

- 用户故事按优先级顺序执行
- MVP 范围: Phase 1 + Phase 2 + Phase 3
- US2 是增量功能
