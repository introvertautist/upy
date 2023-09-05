"""Query builder"""
from enum import Enum
from typing import Any

from upy.conditions.condition import Condition, ConditionGroup
from upy.core.abstract_builder import TM, AbstractQueryBuilder
from upy.exceptions import UndefinedTable
from upy.expressions.expression import Expression
from upy.fields.field import TableField
from upy.utils import FilterType, Query, generate_condition_group_by_arguments


class SqlConstruction(str, Enum):
    """Enum with base SQL constructions"""

    FROM = "FROM"
    TABLE = "TABLE"
    WHERE = "WHERE"
    DELETE = "DELETE"
    UPDATE = "UPDATE"


class QueryBuilder(AbstractQueryBuilder[TM]):
    """
    Query builder
    """

    def __init__(self, table: TM) -> None:
        """
        Initialize QueryBuilder
        :param table: Parent table
        """
        self.table: TM = table
        self.__where: ConditionGroup | None = None

    def filter(self, *args: FilterType) -> "QueryBuilder":
        """
        Update where condition
        :param args: Filter arguments
        :return: QueryBuilder
        """
        self.__update_where_by_arguments(*args)
        return self

    def build_update(self, *args: Condition | Expression, **kwargs: Any) -> Query:
        """
        Build SQL UPDATE query
        Modify provided arguments and cast it to ConditionGroup object
        :param args: Filter arguments
        :param kwargs: Updated fields with values
        :return: Query object
        """
        query: list[str] = [SqlConstruction.UPDATE.value]
        params: list[Condition | ConditionGroup | Expression] = []

        self.__query_building_pipeline(query, params, [SqlConstruction.TABLE])
        query.append("SET")
        query.append(self.__patch_params_for_update(params, *args, **kwargs))

        self.__query_building_pipeline(query, params, [SqlConstruction.WHERE])
        result_query = " ".join(query)

        return Query(sql=result_query, params=params)

    def build_delete(self, *args: FilterType, strict: bool = True) -> Query:
        """
        Build SQL DELETE query
        Modify provided arguments and cast it to ConditionGroup object
        :param args: Filter arguments
        :param strict: Strict False used to set 'WHERE = true' to prevent PostgreSQL warning on deleting all data
        :return: Query object
        """
        query: list[str] = [SqlConstruction.DELETE.value]
        params: list[Condition | ConditionGroup | Expression] = []

        self.__update_where_by_arguments(*args)

        if not strict and self.__where is None:
            self.__where = ConditionGroup(Condition("true"))

        self.__query_building_pipeline(query, params, [SqlConstruction.FROM, SqlConstruction.WHERE])
        result_query = " ".join(query)

        return Query(sql=result_query, params=params)

    def __update_where_by_arguments(self, *args: FilterType) -> None:
        """
        Update where clause with provided condition arguments
        :param args: Any condition expression
        :return: None
        """
        if not args:
            return

        condition = generate_condition_group_by_arguments(*args)
        if not self.__where:
            self.__where = condition
        else:
            self.__where &= condition

    def __patch_params_for_update(self, params: list[Any], *args: Condition | Expression, **kwargs: Any) -> str:
        """
        Patch SQL query and params with provided args and kwargs
        Also make field aliasing like <table_name>.<field> if one of field in initial query already aliased
        :param params: Initial query parameters
        :param args: Updated fields as Condition or Expression
        :param kwargs: Updated fields as keyword arguments
        :return: Update SQL clause
        """
        sql: list[str] = []
        alias_prefix = ""

        if args or self.__where:
            alias_prefix = f"{self.table.sql}."

        for arg in args:
            sql.append(arg.sql)
            params.extend(arg.params)

        for field, value in kwargs.items():
            if "." in field or "__" in field:
                _field = TableField.from_alias(field)
                sql.append(f"{_field.alias} = %s")
                params.append(value)
            else:
                sql.append(f"{alias_prefix}{field} = %s")
                params.append(value)

        return ", ".join(sql)

    def __query_building_pipeline(
        self, sql: list[str], params: list[Any], constructions: list[SqlConstruction]
    ) -> None:
        """
        Building SQL query pipeline
        Construct query by reserved constructions
        :param sql: List of pre-defined SQL constructions
        :param params: Execution parameters
        :param constructions: SQL constructions for building
        :return: None
        """
        if SqlConstruction.TABLE in constructions:
            if not self.table:
                raise UndefinedTable()

            sql.append(self.table.sql)
            params.extend(self.table.params)

        if SqlConstruction.FROM in constructions:
            if not self.table:
                raise UndefinedTable()

            sql.extend([SqlConstruction.FROM.value, self.table.sql])
            params.extend(self.table.params)

        if SqlConstruction.WHERE in constructions and self.__where:
            sql.extend([SqlConstruction.WHERE, self.__where.sql])
            params.extend(self.__where.params)
