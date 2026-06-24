# Feature Specification: Feishu Bitable Auto-Upload

**Feature Branch**: `005-feishu-bitable-upload`

**Created**: 2026-06-17

**Status**: Draft

**Input**: User description: "1.请参考飞书下的所有接口文档，实现创建飞书多维表格、新增表格多条记录接口。2.参考自建应用获取tenant access token.md，我会配合提供凭证信息。3.修改export_video_performance.py脚本，新增将本地excel文件上传飞书多维表格的功能。3.1. 上传时需先调用创建多维表格接口，再反复调用新增表格多条记录接口（单次最多1000条），直到记录全部上传完毕，并校验总数量一致。3.2. 保留原上传钉钉文档功能作为独立选项，默认上传飞书多维表格。"

## User Scenarios & Testing

### User Story 1 - Automated Daily Upload to Feishu (Priority: P1)

The system automatically uploads the generated Excel file to a Feishu Bitable after the daily video performance data fetch completes via cron job at 06:00.

**Why this priority**: This is the core automated workflow that eliminates manual intervention.

**Independent Test**: Can be tested by running the modified cron job and verifying the bitable URL is logged.

**Acceptance Scenarios**:

1. **Given** daily video data fetch completes successfully, **When** the Excel file is generated, **Then** the system creates a new Feishu Bitable and uploads all records
2. **Given** the upload completes, **Then** the system logs the Bitable URL and record count
3. **Given** the upload fails, **Then** the system logs the error and continues without blocking
4. **Given** the record count exceeds 1000, **When** uploading, **Then** the system makes multiple batch_create calls until all records are uploaded

---

### User Story 2 - Manual Upload Trigger (Priority: P2)

Admin can manually trigger upload of a specific date's Excel file to Feishu Bitable.

**Why this priority**: Provides flexibility for backfill or retry scenarios.

**Independent Test**: Can be tested by running the script with specific date parameter.

**Acceptance Scenarios**:

1. **Given** a valid Excel file exists for a specific date, **When** admin runs upload command with that date, **Then** the file is uploaded to Feishu Bitable

---

### Edge Cases

- What happens when the Excel file is missing or corrupted?
- What happens when Feishu API returns an error (auth, quota, network)?
- What happens when access_token is expired?
- What happens when record count exceeds 20,000 (Feishu limit)?

## Requirements

### Functional Requirements

- **FR-001**: System MUST create a new Feishu Bitable using the bitable/v1/apps API
- **FR-002**: System MUST use tenant_access_token for Feishu API authentication
- **FR-003**: System MUST batch records in groups of up to 1000 per API call
- **FR-004**: System MUST continue calling batch_create until all records are uploaded
- **FR-005**: System MUST verify total uploaded record count matches Excel row count
- **FR-006**: System MUST log Bitable URL on successful creation
- **FR-007**: System MUST support manual trigger via CLI parameter
- **FR-008**: Original DingTalk upload functionality MUST be preserved as separate option

### Key Entities

- **Feishu Credentials**: app_id, app_secret, tenant_access_token
  - Token obtained via `POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal`
  - Token valid for 2 hours (7200 seconds), to be cached and refreshed
- **Bitable Info**: app_token, table_id, name, url
- **Video Performance Excel**: The exported Excel file with columns: Video ID, Title, Username, Creator info, GMV, GPM, Views, etc.
- **Upload Log**: Record of upload timestamp, bitable_url, record_count, errors

## Success Criteria

### Measurable Outcomes

- **SC-001**: Created Bitable contains exact same number of records as Excel rows
- **SC-002**: Bitable URL is logged for each successful upload
- **SC-003**: Manual upload completes within 300 seconds for files up to 5000 records
- **SC-004**: Daily cron job completes without blocking on upload failures

## Assumptions

- Excel files contain fewer than 20,000 records (Feishu limit)
- Batch size of 1000 records per call is optimal for performance
- User will provide Feishu app_id and app_secret when prompted
- Bitable will be created in root folder (no folder_token specified)
- Default table fields will be used initially
- Feishu API rate limit (50 calls/second) won't be hit with 1000-record batches
