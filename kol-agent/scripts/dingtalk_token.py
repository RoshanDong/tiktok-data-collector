#!/usr/bin/env python3
"""
DingTalk Token 获取脚本
获取 access_token 并缓存到配置文件
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
LOG_PATH = SCRIPT_DIR.parent / "tiktok-data" / "logs" / "dingtalk_token.log"
TOKEN_URL = "https://oapi.dingtalk.com/gettoken"


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


def get_access_token(appkey, appsecret):
    """获取 DingTalk access_token"""
    params = {
        "appkey": appkey,
        "appsecret": appsecret
    }

    url = TOKEN_URL + "?" + urllib.parse.urlencode(params)

    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode())


def main():
    log_message("开始获取 DingTalk access_token...")

    config = load_config()
    dingtalk_config = config.get("dingtalk", {})

    appkey = dingtalk_config.get("appkey")
    appsecret = dingtalk_config.get("appsecret")

    if not appkey or not appsecret:
        log_message("ERROR: 缺少 dingtalk appkey 或 appsecret 配置")
        return 1

    try:
        result = get_access_token(appkey, appsecret)

        if result.get("errcode") == 0:
            access_token = result.get("access_token")
            expires_in = result.get("expires_in", 7200)

            # 保存到配置
            if "dingtalk" not in config:
                config["dingtalk"] = {}
            config["dingtalk"]["access_token"] = access_token
            config["dingtalk"]["token_expires_at"] = int(time.time()) + expires_in

            save_config(config)

            log_message("✓ Token 获取成功")
            log_message(f"  access_token: {access_token[:20]}...")
            log_message(f"  过期时间: {expires_in} 秒")
            return 0
        else:
            log_message(f"ERROR: Token 获取失败 - {result.get('errmsg')}")
            return 1

    except Exception as e:
        log_message(f"ERROR: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
