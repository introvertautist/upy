from typing import ClassVar

from upy import TableModel, TableConfig
from upy.exceptions import TableConfigRequired


def test_table_build_without_config():
    try:
        class Table(TableModel):
            column: int
    except Exception as exc:
        assert isinstance(exc, TableConfigRequired)
    else:
        assert False


def test_table_build():
    class Table(TableModel):
        config: ClassVar[TableConfig] = TableConfig(tablename="table")
        column: int

    assert Table.sql == "table"
