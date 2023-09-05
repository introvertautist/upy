"""Expression"""
from typing import Any


class Expression:
    """
    Base SQL expression, containing SQL query part. Example:
        Expression("count(table.field) as alias")
        Expression("field = $1", 7)
    """

    def __init__(self, sql: str, *params: tuple[Any, ...]):
        """
        Initialize expression object
        :param sql: SQL string query part
        :param params: Execution parameters
        """
        self._sql: str = sql
        self._params: list[Any] = list(params)  # TODO: Ha-ha-ha...

    @property
    def sql(self) -> str:
        """
        SQL-string query of expression
        :return: SQL-string object
        """
        return self._sql

    @property
    def params(self) -> list[Any]:
        """
        Execution parameters, related to the expression SQL query
        :return: List of parameters
        """
        return self._params
