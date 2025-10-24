import time
from collections import defaultdict, deque
from typing import Deque, Dict

from fastapi import HTTPException, status

from .config import get_settings

settings = get_settings()


class MemoryRateLimiter:
    def __init__(self, max_calls: int, window_seconds: int) -> None:
        self.max_calls = max_calls
        self.window = window_seconds
        self.calls: Dict[str, Deque[float]] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time.time()
        queue = self.calls[key]
        while queue and now - queue[0] > self.window:
            queue.popleft()
        if len(queue) >= self.max_calls:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
        queue.append(now)


rate_limiter = MemoryRateLimiter(settings.rate_limit_per_minute, 60)
