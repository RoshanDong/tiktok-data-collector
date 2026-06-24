#!/usr/bin/env python3
"""
DingTalk 文件上传模块
将 Excel 文件上传至钉钉媒体库
"""

import json
import os
import time
import urllib.request
import urllib.parse
import mimetypes
from pathlib import Path

# Configuration path
SCRIPT_DIR = Path(__file__).parent.resolve()
CONFIG_PATH = SCRIPT_DIR.parent / "tiktok-config.json"
UPLOAD_URL = "https://oapi.dingtalk.com/media/upload"


class DingTalkUploader:
    """钉钉文件上传器"""

    def __init__(self, config_path: str = CONFIG_PATH):
        with open(config_path, "r") as f:
            self.config = json.load(f)

        dingtalk_config = self.config.get("dingtalk", {})
        self.appkey = dingtalk_config.get("appkey")
        self.appsecret = dingtalk_config.get("appsecret")
        self.access_token = dingtalk_config.get("access_token")
        self.token_expires_at = dingtalk_config.get("token_expires_at", 0)

    def is_token_valid(self) -> bool:
        """检查 token 是否有效（提前 60 秒刷新）"""
        if not self.access_token:
            return False
        return time.time() < self.token_expires_at - 60

    def get_access_token(self) -> str:
        """获取有效的 access_token"""
        if not self.is_token_valid():
            self._refresh_token()
        return self.access_token

    def _refresh_token(self):
        """刷新 access_token"""
        params = {
            "appkey": self.appkey,
            "appsecret": self.appsecret
        }

        url = "https://oapi.dingtalk.com/gettoken?" + urllib.parse.urlencode(params)

        with urllib.request.urlopen(url, timeout=30) as response:
            result = json.loads(response.read().decode())

        if result.get("errcode") == 0:
            self.access_token = result.get("access_token")
            expires_in = result.get("expires_in", 7200)
            self.token_expires_at = int(time.time()) + expires_in

            # 保存到配置
            self.config["dingtalk"]["access_token"] = self.access_token
            self.config["dingtalk"]["token_expires_at"] = self.token_expires_at

            with open(CONFIG_PATH, "w") as f:
                json.dump(self.config, f, indent=2)
        else:
            raise Exception(f"Token 刷新失败: {result.get('errmsg')}")

    def upload_file(self, file_path: str) -> dict:
        """
        上传文件到钉钉

        Args:
            file_path: 本地文件路径

        Returns:
            dict: 包含 errcode, errmsg, media_id 等
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        token = self.get_access_token()

        # 构建请求
        boundary = "----FormBoundary7MA4YWxkTrZu0gW"

        # 读取文件
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_data = f.read()

        # 构建 multipart/form-data 请求
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="access_token"\r\n\r\n'
            f"{token}\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="type"\r\n\r\n'
            f"file\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="media"; filename="{file_name}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        }

        req = urllib.request.Request(
            UPLOAD_URL,
            data=body,
            headers=headers,
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode())

        return result


def upload_excel(file_path: str, date: str = None) -> dict:
    """
    上传 Excel 文件到钉钉

    Args:
        file_path: Excel 文件路径
        date: 数据日期 (用于日志)

    Returns:
        dict: 上传结果
    """
    uploader = DingTalkUploader()

    print(f"[DingTalk] 开始上传文件: {file_path}")
    if date:
        print(f"[DingTalk] 数据日期: {date}")

    try:
        result = uploader.upload_file(file_path)

        if result.get("errcode") == 0:
            media_id = result.get("media_id")
            created_at = result.get("created_at")
            file_type = result.get("type")

            print(f"[DingTalk] ✓ 上传成功")
            print(f"[DingTalk]   media_id: {media_id}")
            print(f"[DingTalk]   type: {file_type}")
            print(f"[DingTalk]   created_at: {created_at}")

            return {
                "success": True,
                "media_id": media_id,
                "date": date,
                "file_path": file_path
            }
        else:
            print(f"[DingTalk] ✗ 上传失败: {result.get('errmsg')}")
            return {
                "success": False,
                "error": result.get("errmsg"),
                "date": date,
                "file_path": file_path
            }

    except Exception as e:
        print(f"[DingTalk] ✗ 上传异常: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "date": date,
            "file_path": file_path
        }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python3 dingtalk_uploader.py <file_path>")
        sys.exit(1)

    result = upload_excel(sys.argv[1])
    sys.exit(0 if result.get("success") else 1)
