from typing import ClassVar

from upy.conditions import Condition
from upy.config import TableConfig
from upy.table import TableModel


class Table(TableModel):
    config: ClassVar[TableConfig] = TableConfig(tablename="table")
    first: int
    second: int
    third: bool


def test_condition_and_to_str():
    condition = Condition("table.first = 1")
    comparison = condition & "table.third"
    assert comparison.sql == "table.first = 1 AND table.third"


def test_condition_and_to_other_condition():
    condition = Condition("table.first = 1")
    comparison = condition & Condition("table.third")
    assert comparison.sql == "table.first = 1 AND table.third"


def test_condition_or_to_str():
    condition = Condition("table.first = 1")
    comparison = condition | "table.third"
    assert comparison.sql == "table.first = 1 OR table.third"


def test_condition_or_to_other_condition():
    condition = Condition("table.first = 1")
    comparison = condition | Condition("table.third")
    assert comparison.sql == "table.first = 1 OR table.third"
