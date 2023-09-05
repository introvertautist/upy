from typing import ClassVar

from upy import TableModel, TableConfig


class CustomTable(TableModel):
    config: ClassVar[TableConfig] = TableConfig(
        tablename="table"
    )

    id: int
    name: str


# print(CustomTable.objects.build_delete(strict=False))
# print(CustomTable.objects.build_delete(CustomTable.id == 5))
# print(CustomTable.objects.build_delete(table__id=5))


print(CustomTable.objects.filter(CustomTable.id >= 1).build_update(table__id=0))
