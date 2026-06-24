# Quickstart: Feishu Bitable Auto-Upload

## 前置条件

1. 已配置飞书应用 (app_id + app_secret)
2. Python 3.9+ 环境
3. 依赖: `requests`, `openpyxl`

## 验证步骤

### 步骤 1: 配置飞书凭证

在 `tiktok-config.json` 中添加:

```json
{
  "feishu": {
    "app_id": "cli_xxx",
    "app_secret": "xxx"
  }
}
```

### 步骤 2: 测试 Token 获取

```bash
python3 .kol-agent/scripts/feishu_token.py
```

**预期输出**:
```
[时间] INFO - Token 获取成功
[时间] INFO -   tenant_access_token: xxx
[时间] INFO -   过期时间: 7200 秒
```

### 步骤 3: 测试飞书上件

```bash
python3 .kol-agent/scripts/export_video_performance.py --feishu
```

**预期输出**:
```
[时间] INFO - 导出完成
[时间] INFO -   成功: 1 天
[时间] INFO -   视频数据已上传至飞书多维表格
[时间] INFO -   Bitable URL: https://feishu.cn/base/xxx
[时间] INFO -   记录数: 3479
```

### 步骤 4: 测试钉钉上件 (独立选项)

```bash
python3 .kol-agent/scripts/export_video_performance.py --dingtalk
```

**预期输出**:
```
[时间] INFO - 上传钉钉成功
[时间] INFO -   media_id: @lAzPMxxx
```

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| code: 99991663 | app_id/app_secret 错误 | 检查凭证配置 |
| code: 1254040 | app_token 不存在 | 检查 app_token 是否正确 |
| code: 1254104 | 单次添加超限 | 减少每批记录数 |
| code: 1254291 | 写冲突 | 添加延迟或设置 ignore_consistency_check |
