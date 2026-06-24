# TikTok Data Collector

TikTok 视频数据采集与自动上传工具，支持将每日视频表现数据导出到 Excel 并自动上传至钉钉和飞书多维表格。

## 功能特性

- **视频数据采集**: 从 TikTok API 获取全量视频表现数据（播放量、点赞、评论、分享、收藏等）
- **Excel 导出**: 批量导出近N天每天的数据，支持按日期目录存储
- **钉钉上传**: 自动将 Excel 文件上传至钉钉群
- **飞书上传**: 自动将数据上传至飞书多维表格
- **定时任务**: 支持 Cron 定时执行，每日自动运行

## 项目结构

```
.
├── .kol-agent/
│   ├── scripts/                 # 核心脚本
│   │   ├── export_video_performance.py  # 主脚本：数据导出 + 上传
│   │   ├── dingtalk_uploader.py         # 钉钉上传模块
│   │   ├── dingtalk_token.py           # 钉钉 Token 获取
│   │   ├── feishu_uploader.py           # 飞书上传模块
│   │   ├── feishu_token.py              # 飞书 Token 获取
│   │   ├── feishu_refresh_token.py      # 飞书 Token 刷新
│   │   └── refresh_token.py            # TikTok Token 刷新
│   ├── tiktok-data/
│   │   ├── exports/            # 导出的 Excel 文件
│   │   ├── logs/                # 日志文件
│   │   └── PROGRESS.md          # 开发进度记录
│   └── tiktok-config.json       # 配置文件（包含 API 凭证）
├── specs/                       # Speckit 实施计划文档
│   ├── 001-tiktok-data-fetch/
│   ├── 002-orders-api-test-automation/
│   ├── 003-video-performance-exporter/
│   ├── 004-dingtalk-excel-upload/
│   └── 005-feishu-bitable-upload/
├── api官方文档/                  # TikTok API 参考文档
├── CLAUDE.md                    # Claude 项目说明
└── requirements.txt             # Python 依赖
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置凭证

编辑 `.kol-agent/tiktok-config.json`：

```json
{
  "tiktok_api": {
    "client_key": "你的 client_key",
    "client_secret": "你的 client_secret",
    "access_token": "你的 access_token",
    "refresh_token": "你的 refresh_token"
  },
  "dingtalk": {
    "appkey": "钉钉 appkey",
    "appsecret": "钉钉 appsecret"
  },
  "feishu": {
    "app_id": "飞书 app_id",
    "app_secret": "飞书 app_secret",
    "folder_token": "飞书文件夹 token"
  }
}
```

### 3. 运行脚本

```bash
# 导出视频数据并上传到钉钉（默认行为）
python3 .kol-agent/scripts/export_video_performance.py

# 仅导出不上传
python3 .kol-agent/scripts/export_video_performance.py --no-upload

# 上传指定日期的 Excel 到钉钉
python3 .kol-agent/scripts/export_video_performance.py --upload-only 2026-06-15

# 上传 Excel 到飞书多维表格
python3 .kol-agent/scripts/feishu_uploader.py <excel文件路径> <日期>

# 刷新 TikTok Token
python3 .kol-agent/scripts/refresh_token.py

# 刷新飞书 Token
python3 .kol-agent/scripts/feishu_refresh_token.py
```

## 定时任务配置

```bash
# 视频数据抓取 + 上传钉钉（每天 06:00）
0 6 * * * cd /path/to/project && python3 .kol-agent/scripts/export_video_performance.py >> logs/cron.log 2>&1

# TikTok Token 刷新（每周一 04:00）
0 4 * * 1 python3 .kol-agent/scripts/refresh_token.py >> logs/cron.log 2>&1

# 飞书 Token 刷新（每小时）
0 * * * * python3 .kol-agent/scripts/feishu_refresh_token.py >> logs/cron.log 2>&1
```

## API 数据字段

导出的 Excel 包含以下字段：

| 字段 | 说明 |
|------|------|
| 日期 | 数据日期 |
| 视频ID | 视频唯一标识 |
| 视频标题 | 视频标题 |
| 播放量 | 视频播放次数 |
| 点赞数 | 点赞次数 |
| 评论数 | 评论次数 |
| 分享数 | 分享次数 |
| 收藏数 | 收藏次数 |
| 关注数 | 关注增量 |
| 播放完成率 | 完播率 |

## 技术栈

- Python 3
- TikTok Open API v2
- 钉钉开放平台 API
- 飞书开放平台 API
- openpyxl (Excel 处理)
- requests (HTTP 请求)
- tenacity (重试机制)

## 开发进度

详见 [PROGRESS.md](.kol-agent/tiktok-data/PROGRESS.md)

## 许可证

MIT License
