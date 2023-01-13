from time import monotonic
import asyncio

from aiostorage_orm import AIORedisORM
from aiostorage_orm import AIORedisItem
from aiostorage_orm import AIOStorageORM

COUNT: int = 1000


class TestItem(AIORedisItem):
    attr1: int
    attr2: str

    class Meta:
        table = "param1.{param1}.param2.{param2}"


async def main():
    # Write test
    start_time: float = monotonic()
    redis_orm: AIOStorageORM = AIORedisORM(host="localhost", port=6379, db=1)
    await redis_orm.bulk_create([
        TestItem(attr1=i, attr2=str(i), param1=i % 5, param2=i % 3) for i in range(COUNT)
    ])
    total_time: float = monotonic() - start_time
    print(f"AIOStorageORM (write) -> Objects count: {COUNT}, total time: {total_time}")
    # Load test (direct)
    start_time = monotonic()
    items: list[TestItem] = await TestItem.filter(param1=1, param2=1)
    total_time = monotonic() - start_time
    print(f"AIOStorageORM (load, direct) -> Objects count: {COUNT}, total time: {total_time}")
    # Load test (use parameter __in)
    start_time = monotonic()
    items = await TestItem.filter(param1__in=[1, 2, 3, 4, 5, 6, 7], param2=1)
    total_time = monotonic() - start_time
    print(f"AIOStorageORM (load, use __in = [1-7]) -> Objects count: {COUNT}, total time: {total_time}")


asyncio.run(main())
