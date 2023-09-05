from typing import ClassVar

from upy import ConditionGroup
from upy.config import TableConfig
from upy.table import TableModel


class Table(TableModel):
    config: ClassVar[TableConfig] = TableConfig(tablename="table")
    first: int
    second: int


def test_conditions_compare_or():
    condition: ConditionGroup = (Table.first == 1) | (Table.second == 2)
    assert condition.sql == "table.first = %s OR table.second = %s"


def test_conditions_compare_and():
    condition: ConditionGroup = (Table.first == 1) & (Table.second == 2)
    assert condition.sql == "table.first = %s AND table.second = %s"


def test_conditions_compare_common():
    condition: ConditionGroup = ((Table.first == 1) | (Table.first == 2)) & ((Table.second == 3) | (Table.second == 4))
    assert condition.sql == "(table.first = %s OR table.first = %s) AND (table.second = %s OR table.second = %s)"
