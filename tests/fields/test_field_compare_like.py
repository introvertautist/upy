from typing import ClassVar

from upy.conditions.condition import Condition
from upy.config import TableConfig
from upy.exceptions import InvalidOperatorComparison
from upy.expressions import Expression
from upy.fields.field import TableField
from upy.table import TableModel

field = TableField(name="column", prefix="table")


class Table(TableModel):
    config: ClassVar[TableConfig] = TableConfig(tablename="table")
    column: int


def test_field_like_to_none():
    try:
        Table.column % None
    except Exception as exc:
        assert isinstance(exc, InvalidOperatorComparison)
    else:
        assert False

    try:
        Table.column % None
    except Exception as exc:
        assert isinstance(exc, InvalidOperatorComparison)
    else:
        assert False


def test_field_like_to_other_field_raw():
    condition: Condition = field % TableField(name="other_column", prefix="other_table")
    assert condition.sql == "table.column LIKE other_table.other_column"

    condition: Condition = field % TableField(name="other_column", prefix="other_table")
    assert condition.sql == "table.column LIKE other_table.other_column"


def test_field_like_to_other_field():
    condition: Condition = Table.column % TableField(name="other_column", prefix="other_table")
    assert condition.sql == "table.column LIKE other_table.other_column"

    condition: Condition = Table.column % TableField(name="other_column", prefix="other_table")
    assert condition.sql == "table.column LIKE other_table.other_column"


def test_field_like_to_expression_raw():
    condition: Condition = field % Expression("sum(other_column)")
    assert condition.sql == "table.column LIKE sum(other_column)"

    condition: Condition = field % Expression("sum(other_column)")
    assert condition.sql == "table.column LIKE sum(other_column)"


def test_field_like_to_expression_field():
    condition: Condition = (Table.column % Expression("sum(other_column)"))
    assert condition.sql == "table.column LIKE sum(other_column)"

    condition: Condition = (Table.column % Expression("sum(other_column)"))
    assert condition.sql == "table.column LIKE sum(other_column)"


def test_field_like_to_list():
    try:
        Table.column % [1, 2]
    except Exception as exc:
        assert isinstance(exc, InvalidOperatorComparison)
    else:
        assert False

    try:
        Table.column % [1, 2]
    except Exception as exc:
        assert isinstance(exc, InvalidOperatorComparison)
    else:
        assert False


def test_field_like_to_set():
    try:
        Table.column % {1, 2}
    except Exception as exc:
        assert isinstance(exc, InvalidOperatorComparison)
    else:
        assert False

    try:
        Table.column % {1, 2}
    except Exception as exc:
        assert isinstance(exc, InvalidOperatorComparison)
    else:
        assert False


def test_field_like_to_tuple():
    try:
        Table.column % (1, 2)
    except Exception as exc:
        assert isinstance(exc, InvalidOperatorComparison)
    else:
        assert False

    try:
        Table.column % (1, 2)
    except Exception as exc:
        assert isinstance(exc, InvalidOperatorComparison)
    else:
        assert False


def test_field_like_to_primitive_raw():
    condition: Condition = field % "test"
    assert condition.sql == "table.column LIKE %s"

    condition: Condition = field % "test"
    assert condition.sql == "table.column LIKE %s"


def test_field_like_to_primitive():
    condition: Condition = Table.column % "test"
    assert condition.sql == "table.column LIKE %s"

    condition: Condition = Table.column % "test"
    assert condition.sql == "table.column LIKE %s"
