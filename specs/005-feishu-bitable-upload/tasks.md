# Tasks: Feishu Bitable Auto-Upload

**Input**: Design documents from `specs/005-feishu-bitable-upload/`

**Prerequisites**: plan.md, spec.md (user stories), research.md, data-model.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行执行（不同文件，无依赖）
- **[Story]**: 用户故事编号 (US1, US2)
- 描述中包含具体文件路径

---

## Phase 1: Setup (配置凭证)

**Purpose**: 配置飞书凭证

- [x] T001 在 `tiktok-config.json` 中添加 `feishu` 配置段，包含 `app_id` 和 `app_secret` 字段 ✅

---

## Phase 2: Foundational (核心模块)

**Purpose**: 创建飞书 Token 获取模块（US1 和 US2 都依赖此模块）

- [x] T002 创建 `.kol-agent/scripts/feishu_token.py` - Token 获取脚本 ✅
  - 调用 `POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal`
  - 将 token 和过期时间缓存到 `tiktok-config.json`
  - 添加日志记录

---

## Phase 3: User Story 1 - 自动化每日上传 (Priority: P1) 🎯 MVP

**Goal**: 每日视频数据拉取完成后，自动创建飞书多维表格并分批上传记录

**Independent Test**: 运行脚本，验证 bitable URL 和记录数

### Implementation for User Story 1

- [x] T003 [P] 创建 `.kol-agent/scripts/feishu_uploader.py` - 飞书上件模块 ✅ (待权限验证)
  - 实现 `create_bitable()`: 创建多维表格
  - 实现 `upload_batch()`: 分批上传记录（每批最多1000条）
  - 实现 `upload_all()`: 循环调用 batch_create 直到全部上传
  - 校验上传总数与 Excel 行数一致

- [ ] T004 修改 `.kol-agent/scripts/export_video_performance.py`
  - 在导出成功后调用 `feishu_uploader`
  - 添加 `--feishu` CLI 参数启用飞书上件（默认开启）
  - 添加上传成功/失败的日志记录
  - 添加 Bitable URL 记录

**Checkpoint**: 每日 06:00 cron 任务完成后，Excel 自动上传至飞书多维表格

---

## Phase 4: User Story 2 - 钉钉上件独立选项 (Priority: P2)

**Goal**: 保留钉钉上传作为独立选项

**Independent Test**: 运行 `--dingtalk` 参数，验证钉钉上传

### Implementation for User Story 2

- [ ] T005 修改 `.kol-agent/scripts/export_video_performance.py`
  - 添加 `--dingtalk` 参数启用钉钉上件（独立于飞书）
  - 修改默认行为：飞书优先，钉钉需显式指定

**Checkpoint**: 可独立使用 `--dingtalk` 参数上传钉钉

---

## Phase 5: Polish & 验证

**Purpose**: 验证和文档

- [ ] T006 运行 `python3 .kol-agent/scripts/feishu_token.py` 测试 token 获取
- [ ] T007 运行 `python3 .kol-agent/scripts/export_video_performance.py --feishu` 测试飞书上件
- [ ] T008 运行 `python3 .kol-agent/scripts/export_video_performance.py --dingtalk` 测试钉钉上件
- [ ] T009 验证 Bitable URL 和 media_id 正确记录

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

### MVP First (User Story 1 Only)

1. 完成 Phase 1: 配置飞书凭证
2. 完成 Phase 2: 创建 feishu_token.py
3. 完成 Phase 3: 创建 feishu_uploader.py + 集成
4. **验证**: Bitable URL 和记录数

### Incremental Delivery

1. Setup + Foundational → 基础就绪
2. 添加 US1 → 测试验证 → MVP 完成
3. 添加 US2 → 支持钉钉独立上传

---

## Notes

- 用户故事按优先级顺序执行
- MVP 范围: Phase 1 + Phase 2 + Phase 3
- US2 是增量功能
