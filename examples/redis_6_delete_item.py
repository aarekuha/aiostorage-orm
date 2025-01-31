import random
import asyncio

from aiostorage_orm import AIOStorageORM
from aiostorage_orm import AIORedisORM
from aiostorage_orm import AIORedisItem


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
    orm: AIOStorageORM = AIORedisORM(host="localhost", port=6379)
    await orm.init()

    # Создание единичной записи
    example_item: ExampleItem = ExampleItem(subsystem_id=3, tag_id=15, date_time=100, any_value=17.)
    await example_item.save()
    print(f"After save: {await ExampleItem.get(subsystem_id=3, tag_id=15)=}")

    # Удаление единичной записи
    await example_item.delete()
    print(f"After delete: {await ExampleItem.get(subsystem_id=3, tag_id=15)=}")

    # Создание нескольких записей
    # Подготовка данных
    example_items: list[ExampleItem] = []
    for i in range(10):
        subsystem_id: int = i % 10
        example_item = ExampleItem(
            subsystem_id=subsystem_id,
            another_key_value=i,
            tag_id=10 + (15 * random.randint(0, 1)),
            date_time=i*100,
            any_value=random.random() * 10,
        )
        example_items.append(example_item)
    await orm.bulk_create(items=example_items)
    print("After save:")
    for item in await ExampleItem.filter(_items=example_items):
        print(f"{item=}")
    # Удаление нескольких записей
    await orm.bulk_delete(items=example_items)
    print(f"After delete: {await ExampleItem.filter(_items=example_items)=}")


asyncio.run(main())
