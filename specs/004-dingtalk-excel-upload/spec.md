# Feature Specification: DingTalk Excel Auto-Upload

**Feature Branch**: `004-dingtalk-excel-upload`

**Created**: 2026-06-17

**Status**: Draft

**Input**: User description: "1.请参考上传媒体文件.md接口文档，实现钉钉文档上传接口。2.我会配合提供凭证、access_token等信息，当你需要时向我提问，然后完成接口的文件上传测试。3.修改export_video_performance.py脚本，新增将本地excel文件上传钉钉文档的功能，实现每日拉取完视频数据后，自动将excel文件上传至钉钉文档。"

## User Scenarios & Testing

### User Story 1 - Automated Daily Upload (Priority: P1)

The system automatically uploads the generated Excel file to DingTalk after the daily video performance data fetch completes via cron job at 06:00.

**Why this priority**: This is the core automated workflow that eliminates manual intervention.

**Independent Test**: Can be tested by running the modified cron job and verifying the file appears in DingTalk.

**Acceptance Scenarios**:

1. **Given** daily video data fetch completes successfully, **When** the Excel file is generated, **Then** the system uploads it to DingTalk automatically
2. **Given** the upload succeeds, **Then** the system logs success with media_id
3. **Given** the upload fails, **Then** the system logs the error and continues without blocking

---

### User Story 2 - Manual Upload Trigger (Priority: P2)

Admin can manually trigger upload of a specific Excel file to DingTalk.

**Why this priority**: Provides flexibility for backfill or retry scenarios.

**Independent Test**: Can be tested by running the script with a specific date parameter.

**Acceptance Scenarios**:

1. **Given** a valid Excel file exists for a specific date, **When** admin runs upload command with that date, **Then** the file is uploaded to DingTalk

---

### Edge Cases

- What happens when the Excel file is missing or corrupted?
- What happens when DingTalk API returns an error (network, auth, quota)?
- What happens when access_token is expired?

## Requirements

### Functional Requirements

- **FR-001**: System MUST upload Excel files to DingTalk using the media/upload API
- **FR-002**: System MUST use multipart/form-data format for file upload
- **FR-003**: System MUST set type="file" for Excel files per DingTalk API specification
- **FR-004**: System MUST log upload success with returned media_id
- **FR-005**: System MUST log upload failures with error details
- **FR-006**: Upload MUST happen automatically after daily video data fetch completes
- **FR-007**: System MUST support manual trigger via CLI parameter
- **FR-008**: System MUST support upload retry on failure

### Key Entities

- **DingTalk Credentials**: App credentials including appkey, appsecret, and access_token
  - Token obtained via `GET https://oapi.dingtalk.com/gettoken?appkey=xxx&appsecret=xxx`
  - Token valid for 7200 seconds (2 hours), to be cached and refreshed as needed
- **Video Performance Excel**: The exported Excel file with columns: Video ID, Title, Username, Creator info, GMV, GPM, Views, etc.
- **Upload Log**: Record of upload timestamp, file, media_id, and status

## Success Criteria

### Measurable Outcomes

- **SC-001**: Uploaded files appear in DingTalk media library with correct file size and type
- **SC-002**: Daily cron job completes without errors in 95% of runs over a 30-day period
- **SC-003**: Failed uploads are logged with sufficient detail for debugging within 24 hours
- **SC-004**: Manual upload completes within 60 seconds for files up to 20MB

## Assumptions

- Excel files are within DingTalk's 20MB size limit
- File type "file" is appropriate for Excel (.xlsx) uploads per DingTalk API docs
- User will provide DingTalk appkey and appsecret for token acquisition
- Token will be obtained via `GET https://oapi.dingtalk.com/gettoken?appkey=xxx&appsecret=xxx`
- Token valid for 7200 seconds (2 hours), to be cached and refreshed as needed
- media_id returned by DingTalk can be logged for audit purposes
- Duplicate upload detection is not implemented (each run may re-upload)
- User will provide appkey/secret for DingTalk when prompted during implementation
