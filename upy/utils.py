"""Common utils"""
from typing import Any

from pydantic import BaseModel

from upy.conditions import Condition, ConditionGroup
from upy.exceptions import InvalidFilterArgument
from upy.expressions import Expression
from upy.fields import TableField

FilterType = list[Condition | ConditionGroup | Expression | str]


def quote(value: str) -> str:
    """
    Quote value
    :param value: String value
    :return: Str
    """
    return f"`{value.replace('`', '``')}`"


class Query(BaseModel):
    """
    Part of SQL code representation
    """

    sql: str
    params: list[Any]


def generate_condition_group_by_arguments(*args: FilterType, default: str | None = None) -> ConditionGroup:
    """
    Generate WHERE condition group by provided arguments
    :param args: Filter arguments
    :param default: Default value, returned if arguments is empty
    :return: ConditionGroup
    """
    condition: ConditionGroup = ConditionGroup()

    if not args and default:
        return condition & Condition(sql=default)

    for arg in args:
        if isinstance(arg, ConditionGroup | Condition | Expression):
            condition &= arg
            continue

        if isinstance(arg, TableField):
            condition &= Expression(arg.alias)
            continue

        raise InvalidFilterArgument(f"Object of type '{type(arg)}' can not be used in filtering")

    return condition
