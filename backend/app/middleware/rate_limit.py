import time
from collections import defaultdict
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_hits: dict[str, list[float]] = defaultdict(list)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - self.window
        _hits[ip] = [t for t in _hits[ip] if t > window_start]
        _hits[ip].append(now)

        if len(_hits[ip]) > self.max_requests:
            return Response("Too many requests", status_code=429)

        return await call_next(request)
