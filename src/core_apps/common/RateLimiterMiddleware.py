import json
import logging
from time import time
from typing import Any

import redis
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse

logger = logging.getLogger(__name__)


try:
    redis_client = redis.Redis(
        host="dev-imgtwist-redis",
        port=6379,
        db=0,
    )
    redis_client.ping()
except (redis.ConnectionError, ImproperlyConfigured, Exception) as e:
    logger.error(
        f"""[XX Rate Limit Redis Error XX]: Redis configuration error. Please check if redis is working.
        You can ignore redis and continue to use local cache instead. 
        Exception: {str(e)}"""
    )
    raise ImproperlyConfigured("RateLimitRedisERROR: Redis is not properly configured.")


class TokenBucketRateLimitMiddleware:
    """Global Rate Limit using Token Bucket Algorithm.
    Algorithm:
        - Token Bucket Algorithm
    Conditions:
        - For each 20 seconds, a new token is added.
    """

    bucket_size = {
        "max_tokens": 3,
        "refill_rate": 1.0
        / (
            20 * 1000
        ),  # 1 token per 20000 milliseconds. 3 requests per minute. 3 reqeust as burst by default.
    }

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request, *args: Any, **kwds: Any) -> Any:
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip_addr = x_forwarded_for.split(",")[0]
        else:
            ip_addr = request.META.get("REMOTE_ADDR")

        return ip_addr

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Just basic implementation with IP. However, Key should be unique adding other user factors.
        client_ip = self.get_client_ip(request=request)
        rate_limit_key = f"api_rate_limit:{client_ip}"

        try:
            bucket = redis_client.get(rate_limit_key)
        except redis.ConnectionError as err:
            logger.error(
                f"\n[XX Rate Limit Redis Error XX]: Redis connection failed. Falling bak to local app cache.\nException: {err}"
            )
            bucket = cache.get(rate_limit_key)

        curr_time = int(time() * 1000)  # in milis

        if bucket is None:
            bucket = {
                "tokens": self.bucket_size["max_tokens"],
                "last_request_time": curr_time,
            }
        else:
            bucket = json.loads(bucket)
            elapsed_time = curr_time - bucket["last_request_time"]
            new_tokens = elapsed_time * self.bucket_size["refill_rate"]
            bucket["tokens"] = min(
                self.bucket_size["max_tokens"], new_tokens + bucket["tokens"]
            )
            bucket["last_request_time"] = curr_time

        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            try:
                redis_client.set(rate_limit_key, json.dumps(bucket), ex=60)
            except redis.ConnectionError as err:
                logger.error(
                    f"\n[XX Redis Error XX]: Redis connection failed. Falling bak to local app cache.\nException: {err}"
                )
                cache.set(rate_limit_key, json.dumps(bucket), timeout=60)
        else:
            wait_time = (1 - bucket["tokens"]) / self.bucket_size["refill_rate"] / 1000

            logger.warning(
                f"[XX Rate Limit Warning XX]: Rate Limit Exceed for IP: {client_ip}"
            )
            response = JsonResponse(
                {
                    "message": "Rate Limit Exceed",
                    "wait_time": f"{wait_time:.2f} seconds",
                },
                status=429,
            )
            response["X-RateLimit-Limit"] = str(self.bucket_size["max_tokens"])
            response["X-RateLimit-Remaining"] = str(bucket["tokens"])
            response["X-RateLimit-Reset"] = str(int(bucket["last_request_time"] + 60))

            return response

        return None
