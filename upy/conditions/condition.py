"""Condition and ConditionGroup"""
import copy
from enum import Enum
from typing import Any, Union

from upy.conditions.utils import push_with_reverse
from upy.exceptions import InvalidConditionComparisonInstance, InvalidConditionGroupComparisonInstance
from upy.expressions import Expression


class ConditionGroupOperator(str, Enum):
    """
    Condition group logical operator
    """

    OR = "OR"
    AND = "AND"


class Condition:
    """
    Condition define the logical relationship of entities for AND-OR operators
    Entities can be either a simple SQL-query or another Condition or ConditionGroup (group of conditions)
    """

    def __init__(self, sql: str, params: list[Any] | None = None):
        """
        Initialize Condition object
        :param sql: SQL string condition object
        :param params: Optional parameters for Condition
        """
        self._sql: str = sql
        self._params: list[Any] = params or []

    def __and__(self, other: Union[str, "Condition", "ConditionGroup"]) -> "ConditionGroup":
        """
        Resolve AND logical operator relationship and return ConditionSet object
        An instance for comparison can be:
            str - SQL-string object.
                Example: "table.field = $1"
            Condition - Already defined condition object.
                Example: Condition("table.field = $1", 7)
            ConditionGroup - Already defined group of conditions or condition logical relationship
                Example: Condition("table.field = $1", 7) & Condition("table.other_field = $1", 9)
        :param other: Instance for comparison
        :return: ConditionGroup object
        """
        if isinstance(other, str):
            return self & Condition(other)

        if isinstance(other, Condition):
            # TODO: Maybe just self?
            return ConditionGroup(self) & other

        if isinstance(other, ConditionGroup):
            return other.__rand__(self)

        raise InvalidConditionComparisonInstance(f"Condition operator AND can't be resolved with type {type(other)}")

    def __or__(self, other: Union[str, "Condition", "ConditionGroup"]) -> "ConditionGroup":
        """
        Resolve OR logical operator relationship and return ConditionSet object
        An instance for comparison can be:
            str - SQL-string object.
                Example: "table.field = $1"
            Condition - Already defined condition object.
                Example: Condition("table.field = $1", 7)
            ConditionGroup - Already defined group of conditions or condition logical relationship
                Example: Condition("table.field = $1", 7) & Condition("table.other_field = $1", 9)
        :param other: Instance for comparison
        :return: ConditionGroup object
        """
        if isinstance(other, str):
            return self | Condition(other)

        if isinstance(other, Condition):
            # TODO: Maybe just self?
            return ConditionGroup(self) | other

        if isinstance(other, ConditionGroup):
            return other.__ror__(self)

        raise InvalidConditionComparisonInstance(f"Condition operator OR can't be resolved with type {type(other)}")

    @property
    def sql(self) -> str:
        """
        SQL-string query of condition
        :return: SQL-string object
        """
        return self._sql

    @property
    def params(self) -> list[Any]:
        """
        Execution parameters, related to the condition SQL query
        :return: List of parameters
        """
        return self._params


class ConditionGroup:
    """
    Resolve logical operators for group of conditions
    """

    def __init__(self, condition: Condition | None = None):
        """
        Initialize condition group
        :param condition: Condition object
        """
        self._sql: str | None = None
        self._params: list[Any] = []
        self.__last_operator: ConditionGroupOperator | None = None

        if condition:
            self.__post_init(condition)

    def __post_init(self, condition: Union[Condition, "ConditionGroup"]) -> "ConditionGroup":
        """
        Post initialize for condition group
        Used only when condition group provided:
        Remember SQL query, it's execution parameters and last logical operator
        :param condition: Condition object
        :return: ConditionGroup object
        """
        self._sql = condition.sql
        self._params = condition.params

        if isinstance(condition, ConditionGroup):
            self.__last_operator = condition.last_operator

        return self

    def __and__(self, condition: Union[str, Condition, "ConditionGroup", Expression]) -> "ConditionGroup":
        """
        Handle AND operator for conditions in group
        :param condition: SQL-string, Condition or ConditionGroup object
        :return: ConditionGroup
        """
        return copy.deepcopy(self)._and(condition)

    def __rand__(self, condition: Union[str, Condition, "ConditionGroup"]) -> "ConditionGroup":
        """
        Handle right AND operator for conditions in group
        :param condition: SQL-string, Condition or ConditionGroup object
        :return: ConditionGroup
        """
        return copy.deepcopy(self)._rand(condition)

    def __or__(self, condition: Union[str, Condition, "ConditionGroup"]) -> "ConditionGroup":
        """
        Handle OR operator for conditions in group
        :param condition: SQL-string, Condition or ConditionGroup object
        :return: ConditionGroup
        """
        return copy.deepcopy(self)._or(condition)

    def __ror__(self, condition: Union[str, Condition, "ConditionGroup"]) -> "ConditionGroup":
        """
        Handle right OR operator for conditions in group
        :param condition: SQL-string, Condition or ConditionGroup object
        :return: ConditionGroup
        """
        return copy.deepcopy(self)._ror(condition)

    def _and(self, condition: Union[str, Condition, "ConditionGroup", Expression]) -> "ConditionGroup":
        """
        Resolve AND operator for conditions in group
        :param condition: SQL-string, Condition or ConditionGroup object
        :return: ConditionGroup
        """
        if isinstance(condition, str):
            return self._and(Condition(condition))

        if not isinstance(condition, Condition) and not isinstance(condition, ConditionGroup):
            raise InvalidConditionGroupComparisonInstance(
                f"Condition group operator AND can't be resolved with type {type(condition)}"
            )

        if self._sql is None:
            return self.__post_init(condition)

        if self.__last_operator is not None and self.__last_operator == ConditionGroupOperator.OR:
            self._sql = f"({self._sql})"

        if isinstance(condition, ConditionGroup) and condition.last_operator == ConditionGroupOperator.OR:
            self._sql = f"{self._sql} AND ({condition.sql})"
        else:
            self._sql = f"{self._sql} AND {condition.sql}"

        self._params.extend(condition.params)
        self.__last_operator = ConditionGroupOperator.AND
        return self

    def _rand(self, condition: Union[str, Condition, "ConditionGroup"]) -> "ConditionGroup":
        """
        Resolve right AND operator for conditions in group
        :param condition: SQL-string, Condition or ConditionGroup object
        :return: ConditionGroup
        """
        if isinstance(condition, str):
            return self._rand(Condition(condition))

        if not isinstance(condition, Condition):
            raise InvalidConditionGroupComparisonInstance(
                f"Condition group operator right AND can't be resolved with type {type(condition)}"
            )

        if self._sql is None:
            return self.__post_init(condition)

        if self.__last_operator is not None and self.__last_operator == ConditionGroupOperator.OR:
            self._sql = f"({self._sql})"

        self._sql = f"{condition.sql} AND {self._sql}"
        push_with_reverse(self._params, condition.params)
        self.__last_operator = ConditionGroupOperator.AND
        return self

    def _or(self, condition: Union[str, Condition, "ConditionGroup"]) -> "ConditionGroup":
        """
        Resolve OR operator for conditions in group
        :param condition: SQL-string, Condition or ConditionGroup object
        :return: ConditionGroup
        """
        if isinstance(condition, str):
            return self._or(Condition(condition))

        if not isinstance(condition, Condition) and not isinstance(condition, ConditionGroup):
            raise InvalidConditionGroupComparisonInstance(
                f"Condition group operator OR can't be resolved with type {type(condition)}"
            )

        if self._sql is None:
            return self.__post_init(condition)

        self._sql = f"{self._sql} OR {condition.sql}"
        self._params.extend(condition.params)
        self.__last_operator = ConditionGroupOperator.OR
        return self

    def _ror(self, condition: Union[str, Condition, "ConditionGroup"]) -> "ConditionGroup":
        """
        Resolve right OR operator for conditions in group
        :param condition: SQL-string, Condition or ConditionGroup object
        :return: ConditionGroup
        """
        if isinstance(condition, str):
            return self._ror(Condition(condition))

        if not isinstance(condition, Condition):
            raise InvalidConditionGroupComparisonInstance(
                f"Condition group operator right OR can't be resolved with type {type(condition)}"
            )

        if self._sql is None:
            return self.__post_init(condition)

        self._sql = f"{condition.sql} OR {self._sql}"
        push_with_reverse(self._params, condition.params)
        self.__last_operator = ConditionGroupOperator.OR
        return self

    @property
    def sql(self) -> str:
        """
        SQL-string query of condition group
        :return: SQL-string object
        """
        return "" if self._sql is None else self._sql

    @property
    def params(self) -> list[Any]:
        """
        Execution parameters, related to the condition group SQL query
        :return: List of parameters
        """
        return self._params

    @property
    def last_operator(self) -> ConditionGroupOperator | None:
        """
        Return last condition group operator
        :return: List of parameters
        """
        return self.__last_operator
