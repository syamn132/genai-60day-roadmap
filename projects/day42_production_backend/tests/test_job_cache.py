
from redis.exceptions import ConnectionError as RedisConnectionError

from app.services import job_cache


class FakeRedis:

    def __init__(self):
        self.data = {}
        self.expirations = {}

    def set(self, key, value, ex=None):
        self.data[key] = value
        self.expirations[key] = ex
        return True

    def get(self, key):
        return self.data.get(key)


class BrokenRedis:

    def set(self, *args, **kwargs):
        raise RedisConnectionError("Redis unavailable")

    def get(self, key):
        raise RedisConnectionError("Redis unavailable")


def test_cache_round_trip(monkeypatch):

    fake = FakeRedis()

    monkeypatch.setattr(
        job_cache,
        "redis_client",
        fake,
    )

    job_cache.cache_job_status(
        job_id=42,
        status="completed",
        result="Demo result",
    )

    cached = job_cache.get_cached_job_status(42)

    assert cached == {
        "status": "completed",
        "result": "Demo result",
    }

    assert fake.expirations[
        "day42:job:42:status"
    ] == 60


def test_cache_miss(monkeypatch):

    fake = FakeRedis()

    monkeypatch.setattr(
        job_cache,
        "redis_client",
        fake,
    )

    cached = job_cache.get_cached_job_status(999)

    assert cached is None


def test_redis_failure_is_safe(monkeypatch):

    monkeypatch.setattr(
        job_cache,
        "redis_client",
        BrokenRedis(),
    )

    # Neither operation should crash.
    job_cache.cache_job_status(
        job_id=42,
        status="running",
        result=None,
    )

    assert job_cache.get_cached_job_status(42) is None


def test_invalid_cached_json(monkeypatch):

    fake = FakeRedis()

    fake.data[
        "day42:job:42:status"
    ] = "not-valid-json"

    monkeypatch.setattr(
        job_cache,
        "redis_client",
        fake,
    )

    assert job_cache.get_cached_job_status(42) is None
