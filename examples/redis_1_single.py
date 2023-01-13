from typing import Union
import asyncio

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


async def main():
    # Во время первого подключения устанавливается глобальное подключение к Redis
    AIORedisORM(host="localhost", port=6379)

    # Создание единичной записи
    example_item: ExampleItem = ExampleItem(subsystem_id=3, tag_id=15, date_time=100, any_value=17.)
    result_of_operation: OperationResult = await example_item.save()
    print(result_of_operation)

    # Получение одной записи
    getted_item: Union[ExampleItem, None] = await ExampleItem.get(subsystem_id=3, tag_id=15)
    print(f"{getted_item=}")

    # Получение всех записей по фильтру
    getted_items: list[ExampleItem] = await ExampleItem.filter(subsystem_id=3)
    print(f"{getted_items=}")


asyncio.run(main())
