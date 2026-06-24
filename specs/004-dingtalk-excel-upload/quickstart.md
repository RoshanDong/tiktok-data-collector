# Quickstart: DingTalk Excel Auto-Upload

## 前置条件

1. 已配置钉钉应用 (appkey + appsecret)
2. Python 3.9+ 环境
3. 依赖: `requests`, `openpyxl`

## 验证步骤

### 步骤 1: 配置钉钉凭证

在 `tiktok-config.json` 中添加:

```json
{
  "dingtalk": {
    "appkey": "your_appkey",
    "appsecret": "your_appsecret"
  }
}
```

### 步骤 2: 测试 Token 获取

```bash
python3 .kol-agent/scripts/dingtalk_token.py
```

**预期输出**:
```
[时间] INFO - Token 获取成功
[时间] INFO -   access_token: xxx
[时间] INFO -   过期时间: 7200 秒
```

### 步骤 3: 测试文件上传

```bash
python3 .kol-agent/scripts/export_video_performance.py --days 1 --upload
```

**预期输出**:
```
[时间] INFO - 导出完成
[时间] INFO -   成功: 1 天
[时间] INFO -   视频数据已上传至钉钉
[时间] INFO -   media_id: $xxx
```

### 验证上传结果

1. 检查日志: `tiktok-data/logs/` 目录
2. 钉钉后台查看媒体文件

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| errcode: 40004 | 文件类型不支持 | 确认 type=file |
| errcode: 40078 | token 无效 | 重新获取 token |
| errcode: 10003 | 频率限制 | 等待后重试 |
