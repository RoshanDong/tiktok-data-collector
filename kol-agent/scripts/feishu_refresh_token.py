#!/usr/bin/env python3
import json
import time
import urllib.request
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "tiktok-config.json"
LOG_PATH = Path(__file__).parent.parent / "tiktok-data" / "logs" / "feishu_token.log"
REFRESH_URL = "https://open.feishu.cn/open-apis/authen/v2/oauth/token"

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def log_message(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = "[{}] {}".format(ts, msg)
    print(line)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")

def main():
    log_message("开始刷新 user_access_token...")
    config = load_config()
    feishu = config.get("feishu", {})
    try:
        result = refresh_user_access_token(feishu["app_id"], feishu["app_secret"], feishu["refresh_token"])
        if result["code"] == 0:
            config["feishu"]["user_access_token"] = result["access_token"]
            config["feishu"]["user_access_token_expires_at"] = int(time.time()) + result.get("expires_in", 7200)
            if result.get("refresh_token"):
                config["feishu"]["refresh_token"] = result["refresh_token"]
            if result.get("refresh_token_expires_in"):
                config["feishu"]["refresh_token_expires_in"] = result["refresh_token_expires_in"]
            save_config(config)
            log_message("Token 刷新成功")
            log_message("expires_in: " + str(result.get("expires_in", 7200)) + " 秒")
            return 0
        else:
            log_message("ERROR: code=" + str(result.get("code")))
            return 1
    except Exception as e:
        log_message("ERROR: " + str(e))
        return 1

def refresh_user_access_token(app_id, app_secret, refresh_token):
    import urllib.error
    payload = json.dumps({"grant_type": "refresh_token", "client_id": app_id, "client_secret": app_secret, "refresh_token": refresh_token}).encode()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    req = urllib.request.Request(REFRESH_URL, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise Exception(f"HTTP {e.code}: {error_body}")

if __name__ == "__main__":
    exit(main())
