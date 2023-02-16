import asyncio
from enum import IntEnum
from typing import Union

from aiostorage_orm import AIORedisORM
from aiostorage_orm import AIORedisItem
from aiostorage_orm import OperationResult


class ExampleItem(AIORedisItem):
    class CustomStatus(IntEnum):
        disabled = 0
        enabled = 1

    # Атрибуты объекта с указанием типа данных (в процессе сбора данных из БД приводится тип)
    date_time: int
    any_value: str
    status: CustomStatus

    class Meta:
        # Системный префикс записи в Redis
        # Ключи указанные в префиксе обязательны для передачи в момент создания экземпляра
        table = "subsystem.{subsystem_id}.tag.{tag_id}"


async def main():
    # Во время первого подключения устанавливается глобальное подключение к Redis
    orm: AIORedisORM = AIORedisORM(host="localhost", port=6379)
    await orm.init()

    print("Создание единичной записи с использованием сложных типов данных (IntEnum) у атрибутов")
    example_item: ExampleItem = ExampleItem(
        subsystem_id=3,
        tag_id=15,
        date_time=101,
        any_value=17.,
        status=ExampleItem.CustomStatus.enabled,
    )
    result_of_operation: OperationResult = await example_item.save()
    print(result_of_operation)

    getted_item: Union[ExampleItem, None] = await ExampleItem.get(subsystem_id=3, tag_id=15)
    print(f"{getted_item}")


asyncio.run(main())
