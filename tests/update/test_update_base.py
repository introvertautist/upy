from typing import ClassVar

from upy import TableModel, TableConfig, Condition


class Table(TableModel):
    config: ClassVar[TableConfig] = TableConfig(tablename="table")
    id: int
    name: str


def test_update_one_arg():
    query = Table.objects.build_update(id=1)
    assert query.sql == "UPDATE table SET id = %s"


def test_update_one_aliased_arg():
    query = Table.objects.build_update(table__id=1)
    assert query.sql == "UPDATE table SET table.id = %s"


def test_update_by_filter_condition():
    query = Table.objects.filter(Table.id == 1).build_update(Table.id == 10)
    assert query.sql == "UPDATE table SET table.id = %s WHERE table.id = %s"


def test_update_by_filter_condition_with_arg():
    query = Table.objects.\
        filter(Table.id == 1).\
        filter(Table.name == "ping").\
        build_update(name="pong")
    assert query.sql == "UPDATE table SET table.name = %s WHERE table.id = %s AND table.name = %s"


def test_update_by_args_and_kwargs():
    query = Table.objects.build_update(Table.id == 10, name="test")
    assert query.sql == "UPDATE table SET table.id = %s, table.name = %s"
