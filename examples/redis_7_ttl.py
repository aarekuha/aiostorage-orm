from typing import Union
import random
import asyncio

from aiostorage_orm import AIOStorageORM
from aiostorage_orm import AIORedisORM
from aiostorage_orm import AIORedisItem
from aiostorage_orm import OperationResult


class ExampleItem(AIORedisItem):
    # Атрибуты объекта с указанием типа данных (в процессе сбора данных из БД приводится тип)
    date_time: int
    any_value: str

    class Meta:
        # Системный префикс записи в Redis
        # Ключи указанные в префиксе обязательны для передачи в момент создания экземпляра
        table = "subsystem.{subsystem_id}.tag.{tag_id}"
        # Время жизни объекта в базе данных
        ttl = 10


async def main():
    # Во время первого подключения устанавливается глобальное подключение к Redis
    orm: AIOStorageORM = AIORedisORM(host="localhost", port=6379)
    await orm.init()

    # Создание единичной записи с ограниченным временем жизни
    example_item: ExampleItem = ExampleItem(subsystem_id=3, tag_id=15, date_time=100, any_value=17.)
    result_of_operation: OperationResult = await example_item.save()
    print(result_of_operation)

    # Получение одной записи
    getted_item: Union[ExampleItem, None] = await ExampleItem.get(subsystem_id=3, tag_id=15)
    print(f"{getted_item=}")

    # Групповая вставка объектов с ограниченным временем жизни
    # Подготовка данных
    example_items: list[ExampleItem] = []
    for i in range(100):
        subsystem_id: int = i % 10
        example_item = ExampleItem(
            subsystem_id=subsystem_id,
            another_key_value=i,
            tag_id=10 + (15 * random.randint(0, 1)),
            date_time=i*100,
            any_value=random.random() * 10,
        )
        example_items.append(example_item)
    result_of_operation = await orm.bulk_create(items=example_items)
    print(result_of_operation)


asyncio.run(main())
