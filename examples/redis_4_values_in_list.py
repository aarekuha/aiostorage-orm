import asyncio

from aiostorage_orm import AIOStorageORM
from aiostorage_orm import AIORedisORM
from aiostorage_orm import AIORedisItem
from aiostorage_orm import OperationResult


class ExampleItem(AIORedisItem):
    # Атрибуты объекта с указанием типа данных (в процессе сбора данных из БД приводится тип)
    date_time: int
    any_value: float

    class Meta:
        # Системный префикс записи в Redis
        # Ключи указанные в префиксе обязательны для передачи в момент создания экземпляра
        table = "subsystem.{subsystem_id}.tag.{tag_id}"


async def main():
    # Во время первого подключения устанавливается глобальное подключение к Redis
    orm: AIORedisORM = AIORedisORM(host="localhost", port=6379)
    await orm.init()

    # Создание трёх записей с последовательным subsystem_id
    items: list[ExampleItem] = []
    for i in range(3):
        items.append(ExampleItem(subsystem_id=21+i, tag_id=15, date_time=100+i, any_value=17.+i))
    result_of_operation: OperationResult = await orm.bulk_create(items=items)
    print(result_of_operation)

    # Получение всех записей по фильтру
    getted_items: list[ExampleItem] = await ExampleItem.filter(subsystem_id__in=[21, 23], tag_id=15)
    for item in getted_items:
        print(f"{item=}")


asyncio.run(main())