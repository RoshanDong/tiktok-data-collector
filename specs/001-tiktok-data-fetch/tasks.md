# Tasks: TikTok Shop Data Fetch Automation

**Input**: Design documents from `/specs/001-tiktok-data-fetch/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create directory structure `.kol-agent/tiktok-data/logs/` and `.kol-agent/scripts/`
- [x] T002 [P] Create `requirements.txt` with dependencies: requests, openpyxl, python-crontab, tenacity, pytest, pytest-mock
- [x] T003 [P] Create `.kol-agent/tiktok-config.json` template with placeholder for TikTok API credentials

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create `.kol-agent/scripts/tiktok-fetch.py` with basic structure: imports, config loading, argument parsing
- [x] T005 [P] Implement API client module in `.kol-agent/scripts/tiktok_api_client.py` (authentication, request handling)
- [x] T006 [P] Implement data models in `.kol-agent/scripts/models.py` (DailySalesData, ProductSummary, FetchLog classes)
- [x] T007 Implement logging module in `.kol-agent/scripts/logger.py` (JSONL log writing, log rotation)
- [x] T008 Implement retry logic with exponential backoff in `.kol-agent/scripts/retry_handler.py` (using tenacity)
- [x] T009 Create main entry point with date calculation and error handling framework

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Daily Sales Data Sync (Priority: P1) 🎯 MVP

**Goal**: Fetch daily sales data from TikTok Shop API and store in Excel file

**Independent Test**: Verify that after running the script, an Excel file exists at `.kol-agent/tiktok-data/tiktok-sales-YYYY-MM.xlsx` with correct date, order count, revenue, and top products

### Implementation for User Story 1

- [x] T010 [P] [US1] Implement Excel writer module in `.kol-agent/scripts/excel_writer.py` (openpyxl-based, monthly sheet naming)
- [x] T011 [P] [US1] Implement order aggregation logic in `.kol-agent/scripts/order_aggregator.py` (calculate orderCount, totalRevenue, topProducts by quantity)
- [x] T012 [US1] Implement date range calculation in `.kol-agent/scripts/tiktok-fetch.py` (yesterday's date, timezone handling)
- [x] T013 [US1] Integrate TikTok API client with order aggregator and Excel writer
- [x] T014 [US1] Add validation: ensure Excel output matches data-model.md schema (Date, Order Count, Total Revenue, Top Products columns)
- [x] T015 [US1] Add console output with timestamps per quickstart.md format

**Checkpoint**: User Story 1 should be fully functional - script can fetch data and write to Excel independently

---

## Phase 4: User Story 2 - Historical Data Retention (Priority: P2)

**Goal**: Ensure monthly data accumulation with consistent file naming pattern

**Independent Test**: Verify that running the script multiple times appends data to the correct monthly file and creates new files for new months

### Implementation for User Story 2

- [x] T016 [P] [US2] Implement monthly file management in `.kol-agent/scripts/excel_writer.py` (check if file exists, create if not, append to existing sheet)
- [x] T017 [P] [US2] Add month detection logic to use correct YYYY-MM naming for file and sheet
- [x] T018 [US2] Verify file naming pattern `tiktok-sales-YYYY-MM.xlsx` is followed consistently

**Checkpoint**: User Stories 1 AND 2 should both work - data accumulates correctly across months

---

## Phase 5: User Story 3 - Error Notification (Priority: P3)

**Goal**: Log execution results with task summary and error details on failure

**Independent Test**: Verify that failed runs produce JSONL log entries with status, error message, and retry count

### Implementation for User Story 3

- [x] T019 [P] [US3] Implement FetchLog entity serialization in `.kol-agent/scripts/logger.py`
- [x] T020 [P] [US3] Add log entry writing to `.kol-agent/tiktok-data/logs/YYYY-MM-DD.jsonl` after each execution
- [x] T021 [US3] Integrate logging into main script flow (start, success/failure/partial, end)
- [x] T022 [US3] Verify log format matches data-model.md schema (timestamp, status, dateQueried, orderCount, totalRevenue, errorMessage, retryCount)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T023 [P] Add API rate limit handling (429 response → exponential backoff per FR-006)
- [x] T024 [P] Add zero orders day handling (create file with zero values, don't skip)
- [x] T025 Add cron scheduling integration (configured in .claude/scheduled_tasks.json + system crontab)
- [ ] T026 Run quickstart.md validation (requires API credentials to be configured)
- [x] T027 Update CLAUDE.md with TikTok data fetch workflow reference

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses same Excel writer as US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses same logging infrastructure as US1

### Within Each User Story

- Models before services
- Services before main integration
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- T002 and T003 can run in parallel (different files)
- T005 and T006 can run in parallel (different modules)
- T010 and T011 can run in parallel (different modules)
- T016 and T017 can run in parallel (same module, different functions)
- T019 and T020 can run in parallel (same module, different functions)
- T023 and T024 can run in parallel (different concerns)

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Implement Excel writer module in .kol-agent/scripts/excel_writer.py"
Task: "Implement order aggregation logic in .kol-agent/scripts/order_aggregator.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1: Setup | T001-T003 | Project initialization, dependencies, config |
| Phase 2: Foundational | T004-T009 | Core infrastructure (API client, models, logging, retry) |
| Phase 3: US1 (P1) | T010-T015 | Daily sales data sync - MVP |
| Phase 4: US2 (P2) | T016-T018 | Historical data retention |
| Phase 5: US3 (P3) | T019-T022 | Error notification logging |
| Phase 6: Polish | T023-T027 | Rate limiting, edge cases, cron, validation |

**Total Tasks**: 27
**Parallelizable Tasks**: 14 (marked with [P])

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP scope: Phase 1 + Phase 2 + Phase 3 (User Story 1)