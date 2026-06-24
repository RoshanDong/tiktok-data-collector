# Quickstart: Orders API Test Automation

## Overview

此指南用于验证 Orders API 测试脚本能正确调用 TikTok Shop Orders 3 个核心 API 接口。

## Prerequisites

1. Python 3.9+
2. 已安装依赖：
   ```bash
   pip install requests tenacity
   ```
3. 有效的 TikTok Partner Center 配置（`.kol-agent/tiktok-config.json`）

## Setup

确保 `tiktok-config.json` 包含有效配置：

```json
{
  "tiktok_api": {
    "client_key": "YOUR_CLIENT_KEY",
    "client_secret": "YOUR_CLIENT_SECRET",
    "access_token": "YOUR_ACCESS_TOKEN",
    "refresh_token": "YOUR_REFRESH_TOKEN",
    "shop_cipher": "YOUR_SHOP_CIPHER"
  }
}
```

## Running the Test

```bash
cd /Users/yuelnn/RoshanProgram/Cursor/First-CC
python3 .kol-agent/scripts/orders_api_tester.py
```

## Expected Output

脚本应按顺序测试 3 个核心 API：

### 1. Get Order List (202309)
```
[INFO] T015: 测试 Get Order List API
[INFO] ← Status: 200, Code: 0, Message: Success
[INFO] ✓ Get Order List 成功，获取 20 条订单
```

### 2. Get Order Detail (202507)
```
[INFO] T016: 测试 Get Order Detail API
[INFO] ← Status: 200, Code: 0, Message: Success
[INFO] ✓ Get Order Detail 成功
```

### 3. Get Price Detail (202407)
```
[INFO] T017: 测试 Get Price Detail API
[INFO] ← Status: 200, Code: 0, Message: Success
[INFO] ✓ Get Price Detail 成功
```

## Success Criteria

- 所有 3 个核心 API 调用返回 code=0
- 响应时间总计不超过 60 秒
- 日志包含每个 API 的请求参数和响应信息

## Error Handling

如果某个 API 调用失败：

1. 检查日志中的错误码和错误信息
2. 验证 `tiktok-config.json` 中的配置是否有效
3. 确保 `access_token` 未过期
4. 常见错误码：
   - 401: token 无效，需刷新
   - 400: 请求参数错误
   - 106001: 签名错误
   - 105005: App 权限不足

## Debugging

启用详细日志模式：

```bash
python3 -c "import logging; logging.basicConfig(level=logging.DEBUG)"
```

## API 范围

| API | 版本 | 状态 |
|-----|------|------|
| Get Order List | 202309 | ✅ 已测试 |
| Get Order Detail | 202507 | ✅ 已测试 |
| Get Price Detail | 202407 | ✅ 已测试 |
