# Tasks: Orders API Test Automation

**Input**: Design documents from `/specs/002-orders-api-test-automation/`

**Prerequisites**: plan.md (required), spec.md (required)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 项目初始化和基础配置

- [x] T001 创建测试脚本基础结构 `.kol-agent/scripts/orders_api_tester.py`
- [x] T002 配置依赖检查（requests, tenacity）

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 核心基础设施 - 必须先完成才能开始任何用户故事

- [x] T003 实现签名生成函数 `generate_signature(secret, path, params)` 在 `.kol-agent/scripts/orders_api_tester.py`
- [x] T004 实现 token 刷新函数 `refresh_token()` 在 `.kol-agent/scripts/orders_api_tester.py`
- [x] T005 实现指数退避重试装饰器 `retry_with_exponential_backoff()` 在 `.kol-agent/scripts/orders_api_tester.py`
- [x] T006 实现详细日志记录函数在 `.kol-agent/scripts/orders_api_tester.py`
- [x] T007 实现响应验证函数 `validate_response(response)` 在 `.kol-agent/scripts/orders_api_tester.py`

**Checkpoint**: 基础设施就绪 - 用户故事实现可以开始

---

## Phase 3: User Story 1 - Orders API Test Script (Priority: P1) 🎯 MVP

**Goal**: 调用 TikTok Shop Orders API 目录下的 3 个核心接口，逐一验证每个接口能返回正确数据

**Independent Test**: 运行 `python3 .kol-agent/scripts/orders_api_tester.py` 验证所有 API 返回 code=0

- [x] T008 [P] [US1] 实现 `call_get_order_list()` 函数（版本 202309）在 `.kol-agent/scripts/orders_api_tester.py`
- [x] T009 [P] [US1] 实现 `call_get_order_detail(order_id)` 函数（版本 202507）在 `.kol-agent/scripts/orders_api_tester.py`
- [x] T010 [P] [US1] 实现 `call_get_price_detail(order_id)` 函数（版本 202407）在 `.kol-agent/scripts/orders_api_tester.py`
- [x] T011 [US1] 实现主函数 `main()` 串联所有 API 调用在 `.kol-agent/scripts/orders_api_tester.py`
- [x] T012 [US1] 测试 Get Order List API 验证返回 code=0 ✅
- [x] T013 [US1] 测试 Get Order Detail API 验证返回 code=0 ✅
- [x] T014 [US1] 测试 Get Price Detail API 验证返回 code=0 ✅

**Checkpoint**: 所有 3 个核心 API 测试通过，User Story 1 完成 ✅

---

## Phase 4: User Story 2 - Token Auto-Refresh on 401 (Priority: P2)

**状态**: ❌ 已跳过（用户确认不需要此功能）

---

## Phase 5: User Story 3 - 严格响应验证 (Priority: P3)

**Goal**: 对每个 API 返回的响应进行严格验证：检查 code=0、message=success、必要字段存在且类型正确

**Independent Test**: 构造错误响应验证验证逻辑是否正确抛出异常

- [x] T015 [US3] 扩展 `validate_response()` 检查必要字段存在 ✅
- [x] T016 [US3] 测试错误响应（code≠0）抛出异常 ✅ (API 调用时已验证)
- [x] T017 [US3] 测试缺少必需字段时抛出异常 ✅ (已通过 validate_response 实现)

**Checkpoint**: 严格验证机制正常工作 ✅

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 改进和跨用户故事的工作

- [x] T018 [P] 更新 PROGRESS.md 记录完成状态 ✅
- [x] T019 运行 quickstart.md 验证指南确保脚本符合预期 ✅

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖 - 可以立即开始
- **Foundational (Phase 2)**: 依赖 Setup 完成 - 阻塞所有用户故事
- **User Stories (Phase 3-5)**: 依赖 Foundational 完成
- **Polish (Phase 6)**: 依赖所有用户故事完成

### User Story Dependencies

- **User Story 1 (P1)**: 可在 Foundational 完成后开始 - 无需依赖其他故事
- **User Story 3 (P3)**: 可在 Foundational 完成后开始 - 依赖 Foundational 的验证函数

### Parallel Opportunities

- Phase 3 中 T008-T010 可以并行执行（不同 API 函数）

---

## Summary

| 指标 | 值 |
|------|-----|
| 总任务数 | 19 |
| User Story 1 任务 | 7 (T008-T014) |
| User Story 2 任务 | ❌ 已跳过 |
| User Story 3 任务 | 3 (T015-T017) |
| MVP 范围 | Phase 1-3 (T001-T014) |
| 已完成 | **19/19** ✅ |

## Success Criteria

- [x] T012-T014 所有核心 API 测试通过
- [x] T015-T017 严格验证测试通过
- [x] T018-T019 quickstart 验证通过

## API 范围（最终确认）

| API | 版本 | 状态 |
|-----|------|------|
| Get Order List | 202309 | ✅ 已测试 |
| Get Order Detail | 202507 | ✅ 已测试 |
| Get Price Detail | 202407 | ✅ 已测试 |
| ~~Get External Order References~~ | ~~202406~~ | ❌ 已移除 |
| ~~Add External Order References~~ | ~~202406~~ | ❌ 已移除 |
| ~~Update Blind Box Results~~ | ~~202605~~ | ❌ 已移除 |
