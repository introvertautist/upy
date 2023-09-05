from typing import ClassVar

from upy.conditions.condition import Condition
from upy.config import TableConfig
from upy.expressions import Expression
from upy.fields.field import TableField
from upy.table import TableModel

field = TableField(name="column", prefix="table")


class Table(TableModel):
    config: ClassVar[TableConfig] = TableConfig(tablename="table")
    column: int


def test_field_not_equal_to_none_raw():
    condition: Condition = field != None
    assert condition.sql == "table.column IS NOT NULL"


def test_field_not_equal_to_none():
    condition: Condition = Table.column != None
    assert condition.sql == "table.column IS NOT NULL"


def test_field_not_equal_to_other_field_raw():
    condition: Condition = field != TableField(name="other_column", prefix="other_table")
    assert condition.sql == "table.column <> other_table.other_column"


def test_field_not_equal_to_other_field():
    condition: Condition = Table.column != TableField(name="other_column", prefix="other_table")
    assert condition.sql == "table.column <> other_table.other_column"


def test_field_not_equal_to_expression_raw():
    condition: Condition = field != Expression("sum(other_column)")
    assert condition.sql == "table.column <> sum(other_column)"


def test_field_not_equal_to_expression_field():
    condition: Condition = (Table.column != Expression("sum(other_column)"))
    assert condition.sql == "table.column <> sum(other_column)"


def test_field_not_equal_to_list_raw():
    condition: Condition = field != [1, 2]
    assert condition.sql == "table.column NOT IN (%s, %s)"


def test_field_not_equal_to_list():
    condition: Condition = Table.column != [1, 2]
    assert condition.sql == "table.column NOT IN (%s, %s)"


def test_field_not_equal_to_set_raw():
    condition: Condition = field != {"one", "two"}
    assert condition.sql == "table.column NOT IN (%s, %s)"


def test_field_not_equal_to_set():
    condition: Condition = Table.column != {"one", "two"}
    assert condition.sql == "table.column NOT IN (%s, %s)"


def test_field_not_equal_to_tuple_raw():
    condition: Condition = field != ("one", "two")
    assert condition.sql == "table.column NOT IN (%s, %s)"


def test_field_not_equal_to_tuple():
    condition: Condition = Table.column != ("one", "two")
    assert condition.sql == "table.column NOT IN (%s, %s)"


def test_field_not_equal_to_primitive_raw():
    condition: Condition = field != 1
    assert condition.sql == "table.column <> %s"


def test_field_not_equal_to_primitive():
    condition: Condition = Table.column != 1
    assert condition.sql == "table.column <> %s"
