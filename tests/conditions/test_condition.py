from typing import ClassVar

from upy import Condition
from upy.config import TableConfig
from upy.table import TableModel


class Table(TableModel):
    config: ClassVar[TableConfig] = TableConfig(tablename="table")
    first: int
    second: int


def test_condition_build():
    condition = Condition("table.first = $1", [7])
    assert condition.sql == "table.first = $1"
    assert condition.params == [7]
