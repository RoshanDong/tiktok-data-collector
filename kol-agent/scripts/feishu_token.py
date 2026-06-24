#!/usr/bin/env python3
"""
Feishu Token 获取脚本
获取 tenant_access_token 并缓存到配置文件
"""

import json
import time
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

# Configuration path
SCRIPT_DIR = Path(__file__).parent.resolve()
CONFIG_PATH = SCRIPT_DIR.parent / "tiktok-config.json"
LOG_PATH = SCRIPT_DIR.parent / "tiktok-data" / "logs" / "feishu_token.log"
TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"


def load_config():
    """加载配置文件"""
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(config):
    """保存配置文件"""
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def log_message(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    print(log_line)

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(log_line + "\n")


def get_tenant_access_token(app_id, app_secret):
    """获取 Feishu tenant_access_token"""
    payload = json.dumps({
        "app_id": app_id,
        "app_secret": app_secret
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    req = urllib.request.Request(
        TOKEN_URL,
        data=payload,
        headers=headers,
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())


def main():
    log_message("开始获取 Feishu tenant_access_token...")

    config = load_config()
    feishu_config = config.get("feishu", {})

    app_id = feishu_config.get("app_id")
    app_secret = feishu_config.get("app_secret")

    if not app_id or not app_secret:
        log_message("ERROR: 缺少 feishu app_id 或 app_secret 配置")
        return 1

    try:
        result = get_tenant_access_token(app_id, app_secret)

        if result.get("code") == 0:
            token = result.get("tenant_access_token")
            expire = result.get("expire", 7200)

            # 保存到配置
            if "feishu" not in config:
                config["feishu"] = {}
            config["feishu"]["tenant_access_token"] = token
            config["feishu"]["token_expires_at"] = int(time.time()) + expire

            save_config(config)

            log_message("✓ Token 获取成功")
            log_message(f"  tenant_access_token: {token[:20]}...")
            log_message(f"  过期时间: {expire} 秒")
            return 0
        else:
            log_message(f"ERROR: Token 获取失败 - {result.get('msg')}")
            return 1

    except Exception as e:
        log_message(f"ERROR: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
