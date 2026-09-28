import time

from app.cache.memory import InMemoryCache


def test_cache_set_and_get():
    cache = InMemoryCache(ttl=60)

    cache.set("test_key", "test_value")

    assert cache.get("test_key") == "test_value"


def test_cache_clear():
    cache = InMemoryCache(ttl=60)

    cache.set("test_key", "test_value")
    cache.clear()

    assert cache.get("test_key") is None


def test_cache_expires_after_ttl():
    cache = InMemoryCache(ttl=1)

    cache.set("test_key", "test_value")

    assert cache.get("test_key") == "test_value"

    time.sleep(2)

    assert cache.get("test_key") is None