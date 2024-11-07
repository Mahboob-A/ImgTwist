from time import time
from typing import Any
from django.http import JsonResponse
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured

import json 
import logging
import redis

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
        f'''[XX Rate Limit Redis Error XX]: Redis configuration error. Please check if redis is working.
        You can ignore redis and continue to use local cache instead. 
        Exception: {str(e)}'''
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
        "refill_rate": 1.0 / (20 * 1000), # 1 token per 20000 milliseconds. 3 requests per minute. 3 reqeust as burst by default. 
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
            tokens, last_request_time = redis_client.hmget(rate_limit_key, "tokens", "last_request_time")
        except redis.ConnectionError as err:
            logger.error(
                f"\n[XX Rate Limit Redis Error XX]: Redis connection failed. Falling bak to local app cache.\nException: {err}"
            )
            bucket = cache.get(rate_limit_key)
            tokens = bucket.get("tokens") if bucket else None 
            last_request_time = bucket.get("last_request_time") if bucket else None 

        curr_time = int(time() * 1000)  # in milis 

        if tokens is None or last_request_time is None:
            tokens = self.bucket_size["max_tokens"]
            last_request_time = curr_time
        else: 
                elapsed_time = (curr_time - int(last_request_time)) / 1000
                new_tokens = elapsed_time * self.bucket_size["refill_rate"]
                tokens = min(self.bucket_size["max_tokens"], new_tokens + float(tokens))
                last_request_time = curr_time

        if tokens >= 1:
            tokens -= 1 
            
            # how long it will take to add max_tokens when a single tokan is added in every refil_rater frequency (millis)
            expiration = int(self.bucket_size["max_tokens"] * (1 / self.bucket_size["refill_rate"]))
            try:
                redis_client.hmset(rate_limit_key, {"tokens": tokens, "last_request_time": curr_time})
                redis_client.expire(rate_limit_key, expiration)
            except redis.ConnectionError as err:
                logger.error(
                    f"\n[XX Rate Limit Redis Error XX]: Redis connection failed. Falling bak to local app cache.\nException: {err}"
                )
                cache.set(rate_limit_key, {"tokens": tokens, "last_request_time": curr_time}, timeout=expiration)
        else:
            wait_time = (1 - tokens) / self.bucket_size["refill_rate"] / 1000
            reset_time = int(curr_time + wait_time * 1000)

            logger.warning(f"[XX Rate Limit Warning XX]: Rate Limit Exceed for IP: {client_ip}")
            response = JsonResponse(
                {
                    "message": "Rate Limit Exceed",
                    "wait_time": f"{wait_time:.2f} seconds",
                },
                status=429,
            )
            response["X-RateLimit-Limit"] = str(self.bucket_size["max_tokens"])
            response["X-RateLimit-Remaining"] = str(int(tokens))
            response["X-RateLimit-Reset"] = str(reset_time)

            return response

        return None