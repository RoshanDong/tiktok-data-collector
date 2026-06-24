#!/usr/bin/env python3
"""
TikTok Get Shop Video Performance API Tester
调用 TikTok Shop Video Performance API 进行测试验证
"""

import json
import time
import hmac
import hashlib
import logging
from typing import Optional, Dict, Any, List
from functools import wraps

import requests

# Configuration path
CONFIG_PATH = ".kol-agent/tiktok-config.json"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ============================================================================
# 依赖检查
# ============================================================================
def check_dependencies():
    """检查依赖是否已安装"""
    try:
        import requests
        import tenacity
        logger.info("✓ 依赖检查通过: requests, tenacity")
        return True
    except ImportError as e:
        logger.error(f"✗ 依赖缺失: {e}")
        logger.error("请运行: pip install requests tenacity")
        return False


# ============================================================================
# 签名生成函数
# ============================================================================
def generate_signature(secret: str, path: str, params: dict) -> str:
    """
    生成 TikTok API 签名
    签名算法: secret + path + 按字母排序的 query 参数 + secret
    """
    sign_str = secret + path
    for k in sorted(params.keys()):
        sign_str += k + str(params[k])
    sign_str += secret

    logger.debug(f"Sign string: {sign_str}")

    signature = hmac.new(
        secret.encode('utf-8'),
        sign_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return signature


# ============================================================================
# Token 刷新函数
# ============================================================================
def refresh_token(config: dict) -> dict:
    """
    使用 refresh_token 刷新 access_token
    """
    api_config = config.get("tiktok_api", {})

    params = {
        "app_key": api_config.get("client_key"),
        "app_secret": api_config.get("client_secret"),
        "refresh_token": api_config.get("refresh_token"),
        "grant_type": "refresh_token"
    }

    url = "https://auth.tiktok-shops.com/api/v2/token/refresh?" + "&".join(
        f"{k}={v}" for k, v in params.items()
    )

    logger.info("刷新 access_token...")

    try:
        resp = requests.get(url, timeout=30)
        result = resp.json()

        if result.get("code") == 0:
            data = result.get("data", {})
            api_config["access_token"] = data.get("access_token")
            api_config["refresh_token"] = data.get("refresh_token")
            api_config["token_expire_in"] = data.get("access_token_expire_in")

            # Save updated config
            with open(CONFIG_PATH, "w") as f:
                json.dump(config, f, indent=2)

            logger.info("✓ Token 刷新成功")
            return config
        else:
            logger.error(f"✗ Token 刷新失败: {result.get('message')}")
            return None

    except Exception as e:
        logger.error(f"✗ Token 刷新异常: {e}")
        return None


# ============================================================================
# 指数退避重试装饰器
# ============================================================================
def retry_with_exponential_backoff(max_attempts: int = 3, initial_delay: float = 1.0, max_delay: float = 30.0):
    """
    指数退避重试装饰器
    - 初始延迟 1 秒，每次重试翻倍，最高 30 秒
    - 最多 3 次尝试
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        logger.info(f"✓ 重试成功 (第 {attempt} 次尝试)")
                    return result

                except Exception as e:
                    last_exception = e
                    logger.warning(f"✗ 调用失败 (第 {attempt}/{max_attempts} 次): {e}")

                    if attempt < max_attempts:
                        logger.info(f"  等待 {delay:.1f} 秒后重试...")
                        time.sleep(delay)
                        delay = min(delay * 2, max_delay)
                    else:
                        logger.error(f"✗ 超过最大重试次数 ({max_attempts})")

            raise last_exception

        return wrapper
    return decorator


# ============================================================================
# 详细日志记录
# ============================================================================
def log_request(method: str, url: str, headers: dict, body: Any = None):
    """记录请求详情"""
    logger.info(f"→ {method} {url}")
    logger.debug(f"  Headers: {headers}")
    if body:
        logger.debug(f"  Body: {body}")


def log_response(status_code: int, response: dict, elapsed: float):
    """记录响应详情"""
    code = response.get("code")
    message = response.get("message")
    logger.info(f"← Status: {status_code}, Code: {code}, Message: {message}, Time: {elapsed:.2f}s")
    if code != 0:
        logger.warning(f"  错误详情: {response}")


# ============================================================================
# 响应验证函数
# ============================================================================
class APIError(Exception):
    """API 调用错误异常"""
    def __init__(self, code: int, message: str, request_id: str = None):
        self.code = code
        self.message = message
        self.request_id = request_id
        super().__init__(f"API Error {code}: {message}")


def validate_response(response: dict, required_fields: List[str] = None) -> bool:
    """
    验证 API 响应
    - 检查 code == 0
    - 检查 message == "success"
    - 可选：检查必需字段存在
    """
    code = response.get("code")
    message = response.get("message")
    request_id = response.get("request_id")

    if code != 0:
        raise APIError(code, message, request_id)

    if message and message.lower() != "success":
        logger.warning(f"响应消息异常: {message}")

    # Check required fields
    if required_fields:
        data = response.get("data", {})
        for field in required_fields:
            if field not in data:
                raise APIError(0, f"缺少必需字段: {field}", request_id)

    return True


# ============================================================================
# Get Shop Video Performance API 客户端
# ============================================================================
class VideoPerformanceAPIClient:
    """TikTok Shop Video Performance API 客户端"""

    BASE_URL = "https://open-api.tiktokglobalshop.com"

    def __init__(self, config_path: str = CONFIG_PATH):
        with open(config_path, "r") as f:
            self.config = json.load(f)

        api_config = self.config.get("tiktok_api", {})
        self.app_key = api_config.get("client_key")
        self.app_secret = api_config.get("client_secret")
        self.access_token = api_config.get("access_token")
        self.shop_cipher = api_config.get("shop_cipher")

    def _make_request(self, method: str, path: str, query_params: dict = None) -> dict:
        """
        基础 API 请求方法
        GET /analytics/202605/shop_videos/performance
        """
        timestamp = int(time.time())

        # Build query params
        params = query_params.copy() if query_params else {}
        params["app_key"] = self.app_key
        params["timestamp"] = timestamp

        # Generate signature - secret + path + sorted query params + secret
        sign_str = self.app_secret + path
        for k in sorted(params.keys()):
            sign_str += k + str(params[k])
        sign_str += self.app_secret

        sign = hmac.new(self.app_secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest()

        # Build URL
        url = f"{self.BASE_URL}{path}?app_key={self.app_key}&"

        if query_params:
            for k, v in query_params.items():
                url += f"{k}={v}&"

        url += f"timestamp={timestamp}&sign={sign}"

        # Headers
        headers = {
            "Content-Type": "application/json",
            "x-tts-access-token": self.access_token
        }

        log_request(method, url, headers)

        # Make GET request
        start_time = time.time()
        resp = requests.get(url, headers=headers)
        elapsed = time.time() - start_time

        result = resp.json()
        log_response(resp.status_code, result, elapsed)

        return result

    @retry_with_exponential_backoff()
    def call_get_shop_video_performance(self, start_date_ge: str, end_date_lt: str,
                                        sort_field: str = "gmv", currency: str = "USD",
                                        page_size: int = 10, sort_order: str = "DESC",
                                        account_type: str = "ALL",
                                        page_token: str = None) -> dict:
        """
        Get Shop Video Performance List (版本 202605)
        GET /analytics/202605/shop_videos/performance

        Args:
            start_date_ge: 开始时间 (格式: YYYY-MM-DD)
            end_date_lt: 结束时间 (格式: YYYY-MM-DD)
            sort_field: 排序字段 (gmv, gpm, views, etc.)
            currency: 货币类型 (USD)
            page_size: 每页数量
            sort_order: 排序方向 (DESC, ASC)
            account_type: 账户类型 (ALL, BUSINESS, PERSONAL)
            page_token: 分页 token
        """
        path = "/analytics/202605/shop_videos/performance"

        query_params = {
            "shop_cipher": self.shop_cipher,
            "start_date_ge": start_date_ge,
            "end_date_lt": end_date_lt,
            "sort_field": sort_field,
            "currency": currency,
            "page_size": page_size,
            "sort_order": sort_order,
            "account_type": account_type,
        }

        if page_token:
            query_params["page_token"] = page_token

        result = self._make_request("GET", path, query_params)
        validate_response(result, required_fields=["videos", "total_count"])
        return result


# ============================================================================
# 主函数
# ============================================================================
def main():
    """主函数 - 测试 Get Shop Video Performance API"""
    logger.info("=" * 60)
    logger.info("TikTok Shop Video Performance API Tester")
    logger.info("=" * 60)

    # 检查依赖
    if not check_dependencies():
        return

    # 初始化客户端
    client = VideoPerformanceAPIClient()

    # 测试 Get Shop Video Performance
    logger.info("\n" + "=" * 40)
    logger.info("测试 Get Shop Video Performance API")
    logger.info("=" * 40)

    # 使用最近 7 天数据 (相对于今天 2026-06-12)
    end_date = "2026-06-12"
    start_date = "2026-06-05"

    try:
        result = client.call_get_shop_video_performance(
            start_date_ge=start_date,
            end_date_lt=end_date,
            sort_field="gmv",
            currency="USD",
            page_size=10,
            sort_order="DESC",
            account_type="ALL"
        )

        data = result.get("data", {})
        videos = data.get("videos", [])
        total_count = data.get("total_count", 0)
        latest_available_date = data.get("latest_available_date", "N/A")
        next_page_token = data.get("next_page_token")

        logger.info(f"✓ Get Shop Video Performance 成功")
        logger.info(f"  视频总数: {total_count}")
        logger.info(f"  本次返回: {len(videos)} 条")
        logger.info(f"  最新可用日期: {latest_available_date}")

        if next_page_token:
            logger.info(f"  下一页 token: {next_page_token}")

        if videos:
            first_video = videos[0]
            logger.info(f"\n  首个视频信息:")
            logger.info(f"    ID: {first_video.get('id')}")
            logger.info(f"    标题: {first_video.get('title')}")
            logger.info(f"    用户名: {first_video.get('username')}")
            logger.info(f"    发布时间: {first_video.get('video_post_time')}")
            logger.info(f"    时长: {first_video.get('duration')} 秒")
            logger.info(f"    GMV: {first_video.get('gmv')}")
            logger.info(f"    GPM: {first_video.get('gpm')}")
            logger.info(f"    观看数: {first_video.get('views')}")
            logger.info(f"    点击率: {first_video.get('click_through_rate')}")
            logger.info(f"    SKU 订单数: {first_video.get('sku_orders')}")
            logger.info(f"    商品销量: {first_video.get('items_sold')}")

            # 显示标签
            hash_tags = first_video.get("hash_tags", [])
            if hash_tags:
                logger.info(f"    标签: {', '.join(hash_tags)}")

            # 显示关联商品
            products = first_video.get("products", [])
            if products:
                logger.info(f"    关联商品数: {len(products)}")

            # 显示创作者信息
            creator = first_video.get("creator", {})
            if creator:
                logger.info(f"    创作者: {creator.get('user_name')} ({creator.get('nick_name')})")
                logger.info(f"    作者类型: {creator.get('author_type')}")

        # 打印完整响应 (截取前 1000 字符)
        logger.info(f"\n  完整响应 (前 1000 字符):")
        logger.info(f"  {json.dumps(result, indent=2)[:1000]}")

    except APIError as e:
        logger.error(f"✗ Get Shop Video Performance 失败: {e}")
    except Exception as e:
        logger.error(f"✗ 请求异常: {e}")

    # 总结
    logger.info("\n" + "=" * 60)
    logger.info("测试完成")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()