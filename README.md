# TikTok Data Collector

> 自动化采集 TikTok 视频表现数据，支持导出 Excel 并上传至钉钉群和飞书多维表格。

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 功能特性

| 功能 | 说明 |
|------|------|
| 视频数据采集 | 从 TikTok Open API 拉取全量视频表现数据（播放量、GMV、GPM、订单等） |
| Excel 导出 | 批量导出指定日期范围数据，支持分目录存储 |
| 钉钉上传 | 自动将 Excel 文件推送至钉钉群机器人 |
| 飞书上传 | 自动创建飞书多维表格并同步字段、上传数据（含空白记录清理） |
| Token 管理 | 自动刷新 TikTok / 钉钉 / 飞书 access_token |
| 定时任务 | Cron 配置，每日自动执行 |

## 项目结构

```
.
├── kol-agent/
│   ├── scripts/
│   │   ├── export_video_performance.py      # 主脚本：数据导出 + 上传
│   │   ├── dingtalk_uploader.py             # 钉钉上传模块
│   │   ├── dingtalk_token.py                # 钉钉 access_token 获取
│   │   ├── feishu_uploader.py               # 飞书多维表格上传
│   │   ├── feishu_token.py                  # 飞书 access_token 获取
│   │   ├── feishu_refresh_token.py          # 飞书 access_token 刷新
│   │   ├── refresh_token.py                 # TikTok access_token 刷新
│   │   ├── tiktok_api_client.py             # TikTok API 客户端
│   │   ├── models.py                        # 数据模型
│   │   ├── excel_writer.py                  # Excel 写入工具
│   │   ├── order_aggregator.py              # 订单数据聚合
│   │   ├── logger.py                        # 日志工具
│   │   ├── retry_handler.py                 # 重试机制
│   │   └── get_shop_video_performance_api_tester.py  # API 测试脚本
│   ├── templates/                            # 邮件回复模板（KOL 联系）
│   │   ├── reply_interested.md
│   │   ├── reply_paid_only.md
│   │   └── reply_rejection.md
│   ├── tiktok-config.example.json            # 配置模板
│   └── tiktok-data/
│       └── PROGRESS.md                      # 开发进度记录
├── specs/                                    # Speckit 实施计划
│   ├── 001-tiktok-data-fetch/
│   ├── 002-orders-api-test-automation/
│   ├── 003-video-performance-exporter/
│   ├── 004-dingtalk-excel-upload/
│   └── 005-feishu-bitable-upload/
├── api官方文档/                               # API 参考文档
│   ├── 飞书/                                 # 飞书多维表格 API 文档
│   └── ...
├── requirements.txt
├── CLAUDE.md
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置凭证

复制配置模板并填写真实凭证：

```bash
cp kol-agent/tiktok-config.example.json kol-agent/tiktok-config.json
# 编辑 kol-agent/tiktok-config.json，填入你的 API 凭证
```

**所需凭证：**

| 平台 | 凭证 | 获取方式 |
|------|------|----------|
| TikTok | `client_key`, `client_secret`, `access_token`, `refresh_token` | TikTok Partner Center App |
| 钉钉 | `appkey`, `appsecret` | 钉钉开放平台 → 应用详情 |
| 飞书 | `app_id`, `app_secret`, `folder_token` | 飞书开放平台 → 应用详情 |

### 3. 运行脚本

```bash
# 导出视频数据并上传到钉钉（默认行为）
python3 kol-agent/scripts/export_video_performance.py

# 仅导出，不上传
python3 kol-agent/scripts/export_video_performance.py --no-upload

# 仅上传指定日期的 Excel 到钉钉（不拉取数据）
python3 kol-agent/scripts/export_video_performance.py --upload-only 2026-06-15

# 上传 Excel 到飞书多维表格
python3 kol-agent/scripts/feishu_uploader.py kol-agent/tiktok-data/exports/video_performance_2026-06-15.xlsx 2026-06-15

# 手动刷新 TikTok Token
python3 kol-agent/scripts/refresh_token.py

# 手动刷新飞书 Token
python3 kol-agent/scripts/feishu_refresh_token.py
```

## 定时任务（Cron）

```bash
# 视频数据抓取 + 上传钉钉（每天 06:00 北京时间）
0 6 * * * cd /path/to/tiktok-data-collector && python3 kol-agent/scripts/export_video_performance.py >> kol-agent/tiktok-data/logs/cron.log 2>&1

# TikTok Token 刷新（每周一 04:00）
0 4 * * 1 cd /path/to/tiktok-data-collector && python3 kol-agent/scripts/refresh_token.py >> kol-agent/tiktok-data/logs/cron.log 2>&1

# 飞书 Token 刷新（每小时，user_access_token 有效期 2 小时）
0 * * * * cd /path/to/tiktok-data-collector && python3 kol-agent/scripts/feishu_refresh_token.py >> kol-agent/tiktok-data/logs/cron.log 2>&1
```

## 导出的 Excel 字段

| 字段 | 说明 |
|------|------|
| Video ID | 视频唯一标识 |
| Title | 视频标题 |
| Username | 创作者用户名 |
| Creator User Name | 创作者姓名 |
| Creator Nick Name | 创作者昵称 |
| Creator Author Type | 作者类型 |
| Video Post Time | 发布时间 |
| Duration (sec) | 视频时长（秒） |
| Hashtags | 话题标签 |
| GMV Amount | 商品成交总额 |
| GMV Currency | 货币单位 |
| GPM Amount | 千次播放成交额 |
| GPM Currency | GPM 货币单位 |
| Avg Customers | 平均客户数 |
| SKU Orders | SKU 订单数 |
| Items Sold | 已售商品数 |
| Views | 播放量 |
| Click Through Rate | 点击率 |
| Products | 商品数 |

## 技术栈

- **Python 3** — 主语言
- **openpyxl** — Excel 文件生成
- **urllib** — HTTP 请求（无外部依赖）
- **TikTok Open API v2** — 数据来源
- **钉钉开放平台 API** — 钉钉推送
- **飞书开放平台 API** — 飞书多维表格

## 相关文档

- [TikTok API 官方文档](https://open.tiktokapis.com/)
- [钉钉开放平台](https://open.dingtalk.com/)
- [飞书开放平台](https://open.feishu.cn/)

## 许可证

MIT License
