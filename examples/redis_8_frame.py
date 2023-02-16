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
        ttl = 100  # Время жизни объекта в базе данных
        frame_size = 4  # Размер frame'а


async def main() -> None:
    # Во время первого подключения устанавливается глобальное подключение к Redis
    orm: AIOStorageORM = AIORedisORM(host="localhost", port=6379)
    await orm.init()

    print("Создание единичной записи и добавление во frame")
    example_item: ExampleItem = ExampleItem(subsystem_id=3, tag_id=15, date_time=101, any_value=17.)
    result_of_operation: OperationResult = await orm.frame.add(item_or_items=example_item)
    print(result_of_operation)

    # Получение сохраненных во frame'е данных
    new_item: ExampleItem = ExampleItem(subsystem_id=3, tag_id=15)
    getted_items: list[ExampleItem] = await orm.frame.get(new_item, 0, 0)
    for item in getted_items:
        print(f"{item=}")

    print("Групповая вставка данных во frame")
    example_items: list[ExampleItem] = []
    for i in range(0, 10):
        example_item = ExampleItem(
            subsystem_id=1,
            tag_id=1,
            date_time=i * 10,
            any_value=random.random() * 10,
        )
        example_items.append(example_item)
    await example_items[0].init_frame()
    result_of_operation = await orm.frame.add(item_or_items=example_items)
    print(result_of_operation)
    # Получение сохраненных во frame'е данных
    new_item = ExampleItem(subsystem_id=1, tag_id=1)
    print("Все элементы:")
    getted_items = await orm.frame.get(item=new_item)
    for idx, item in enumerate(getted_items):
        print(f"{idx}: {item=}")
    print("Самый старый объект:")
    getted_items = await orm.frame.get(item=new_item, start_index=0, end_index=0)
    for idx, item in enumerate(getted_items):
        print(f"{idx}: {item=}")
    print("Самый свежий объект:")
    getted_items = await orm.frame.get(item=new_item, start_index=-1, end_index=-1)
    for idx, item in enumerate(getted_items):
        print(f"{idx}: {item=}")


asyncio.run(main())
