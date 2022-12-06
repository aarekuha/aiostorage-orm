from __future__ import annotations
import redis.asyncio as redis


class MockedRedis(redis.Redis):
    calls_count: int
    set_calls_count: int
    execute_calls_count: int
    delete_calls_count: int
    _pipe: MockedRedis
    connection: None = None

    def __init__(self, is_pipe: bool = False) -> None:
        self.calls_count = 0
        self.set_calls_count = 0
        self.execute_calls_count = 0
        self.delete_calls_count = 0
        if not is_pipe:
            self._pipe = self.__class__(is_pipe=True)

    async def mset(self, **_) -> None:
        self.calls_count += 1

    async def set(self, *args, **_) -> None:
        self.set_calls_count += 1

    async def execute(self, **_) -> None:
        self.execute_calls_count += 1

    def pipeline(self, **_) -> MockedRedis:
        return self._pipe

    async def delete(self, *_) -> None:
        self.delete_calls_count += 1

    def __repr__(self) -> str:
        return self.__class__.__name__

    @classmethod
    async def ping(cls) -> bool:
        return True
