from typing import ClassVar

from upy import TableModel, TableConfig


class Table(TableModel):
    config: ClassVar[TableConfig] = TableConfig(tablename="table")
    id: int
    name: str


def test_delete_all_strict():
    query = Table.objects.build_delete()
    assert query.sql == "DELETE FROM table"
    assert len(query.params) == 0


def test_delete_all():
    query = Table.objects.build_delete(strict=False)
    assert query.sql == "DELETE FROM table WHERE true"
    assert len(query.params) == 0


def test_delete_with_args_filter():
    query = Table.objects.build_delete(Table.id == 1)
    assert query.sql == "DELETE FROM table WHERE table.id = %s"
    assert query.params == [1]


def test_delete_with_args_filter_common():
    query = Table.objects.build_delete((Table.id == 1) | (Table.id == 2))
    assert query.sql == "DELETE FROM table WHERE table.id = %s OR table.id = %s"
    assert query.params == [1, 2]


def test_delete_with_where():
    query = Table.objects.filter(Table.id == 1).build_delete()
    assert query.sql == "DELETE FROM table WHERE table.id = %s"
    assert query.params == [1]


def test_delete_with_multiple_where():
    query = Table.objects.\
        filter(Table.id == 1).\
        filter(Table.name == "test").\
        build_delete()
    assert query.sql == "DELETE FROM table WHERE table.id = %s AND table.name = %s"
    assert query.params == [1, "test"]


def test_delete_with_common_where_and_direct_filter():
    query = Table.objects.filter(Table.id == 1).build_delete(Table.name == "test")
    assert query.sql == "DELETE FROM table WHERE table.id = %s AND table.name = %s"
    assert query.params == [1, "test"]
