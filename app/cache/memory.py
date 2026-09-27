import time
from typing import Any


class InMemoryCache:
    def __init__(self, ttl: int = 60):
        self.ttl = ttl
        self._cache: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Any | None:
        if key not in self._cache:
            return None

        value, timestamp = self._cache[key]

        if time.monotonic() - timestamp >= self.ttl:
            del self._cache[key]
            return None

        return value

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = (value, time.monotonic())

    def clear(self) -> None:
        self._cache.clear()