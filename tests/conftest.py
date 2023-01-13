from typing import Union
import asyncio

import pytest
import redis.asyncio as redis

from aiostorage_orm import AIORedisItem
from aiostorage_orm import AIORedisFrame


@pytest.fixture(scope="session")
def event_loop():
    """ Получает event_loop и не закрывает его до окончания тестов """
    yield asyncio.get_event_loop()


@pytest.fixture
def test_item(test_input_dict: dict) -> AIORedisItem:
    """ Тестовый экземплар класса """
    class TestItem(AIORedisItem):
        """ Тестовый пример класса """
        attr1: str
        attr2: int
        attr3: float
        attr4: bytes

        class Meta:
            # Префикс записи в БД
            table = "param1.{param1}.param2.{param2}"
            ttl = None
            frame_size = 100

    return TestItem(**test_input_dict)


@pytest.fixture
def test_input_dict() -> dict[str, Union[str, bytes, float, int]]:
    """ Тестовый словарь """
    return {
        "param1": "param_value_1",
        "param2": "param_value_2",
        "attr1": "attr_value_1",  # str
        "attr2": 19,  # int
        "attr3": 99.9,  # float
        "attr4": b"attr_value_4",  # bytes
    }


@pytest.fixture
def test_redis(pmr_redis_container, pmr_redis_config) -> redis.Redis:  # type: ignore
    """ Создание асинхронного класса Redis и удаление всех имеющихся в редис записей """
    db: redis.Redis = redis.Redis(host=pmr_redis_config.host, port=pmr_redis_config.port, db=0)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db.flushdb())
    return db


@pytest.fixture
def test_frame(test_redis) -> AIORedisFrame:
    return AIORedisFrame(client=test_redis)
