# Tasks: Video Performance Data Exporter

**Input**: Design documents from `/specs/003-video-performance-exporter/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, quickstart.md

**Tests**: Not requested — manual validation only

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify dependencies and create output directory

- [x] T001 Check openpyxl is installed (`pip install openpyxl`)
- [x] T002 [P] Create output directory `.kol-agent/tiktok-data/exports/` if not exists

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core utilities that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create API client class with pagination support in `.kol-agent/scripts/export_video_performance.py`
- [x] T004 Implement token refresh logic in `.kol-agent/scripts/export_video_performance.py`
- [x] T005 Implement exponential backoff retry decorator in `.kol-agent/scripts/export_video_performance.py`
- [x] T006 Implement response validation with missing-field handling in `.kol-agent/scripts/export_video_performance.py`

**Checkpoint**: Foundation ready — API client, retry, and validation are available for all user stories

---

## Phase 3: User Story 1 - Daily Video Performance Export (Priority: P1) 🎯 MVP

**Goal**: Fetch and export all video performance data for each of the last 7 days to separate Excel files

**Independent Test**: Run script and verify 7 Excel files are created in output directory, each containing all video records for that day

### Implementation for User Story 1

- [x] T007 [P] [US1] Implement date range calculation (last 7 days) in `.kol-agent/scripts/export_video_performance.py`
- [x] T008 [P] [US1] Implement pagination loop to fetch ALL videos for a single day in `.kol-agent/scripts/export_video_performance.py`
- [x] T009 [US1] Implement Excel writer with all columns per data-model.md schema in `.kol-agent/scripts/export_video_performance.py`
- [x] T010 [US1] Implement main export loop (iterate 7 days, fetch data, write Excel) in `.kol-agent/scripts/export_video_performance.py`
- [x] T011 [US1] Add logging for each day's progress and record count

**Checkpoint**: At this point, User Story 1 should be fully functional — run script, verify 7 Excel files created

---

## Phase 4: User Story 2 - Export Directory Structure (Priority: P2)

**Goal**: Ensure all exported files are organized in a single directory

**Independent Test**: Verify all 7 Excel files exist in the same output directory

### Implementation for User Story 2

- [x] T012 [P] [US2] Add `--output-dir` CLI argument support in `.kol-agent/scripts/export_video_performance.py`
- [x] T013 [US2] Validate output directory is writable before starting export

**Checkpoint**: User Story 1 AND 2 should both work — files land in configured directory

---

## Phase 5: User Story 3 - Progress and Error Reporting (Priority: P3)

**Goal**: Provide clear progress indicators and continue on errors

**Independent Test**: Observe console output shows day-by-day progress and errors don't stop entire export

### Implementation for User Story 3

- [x] T014 [P] [US3] Add per-day progress logging (date being processed, record count)
- [x] T015 [P] [US3] Implement error handling that logs failure and continues to next day (do not stop entire export)
- [x] T016 [US3] Add final summary log (total files created, total records exported, any errors)

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and documentation

- [x] T017 [P] Run quickstart.md validation — execute script and verify output files open in Excel without corruption
- [x] T018 [P] Update PROGRESS.md with new script location and usage

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1, US2, US3 can proceed in parallel after Phase 2
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Phase 2 — core MVP, all other stories depend on its API client
- **User Story 2 (P2)**: Starts after Phase 2 — adds CLI argument, independent of US1 internals
- **User Story 3 (P3)**: Starts after Phase 2 — adds logging/error handling, independent of US1/US2 internals

### Parallel Opportunities

- T001 and T002 can run in parallel
- T007 and T008 can run in parallel (different functions within US1)
- T014 and T015 can run in parallel (different logging functions within US3)
- T017 and T018 can run in parallel (different files)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test script, verify 7 Excel files created correctly
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Polish → Final validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence