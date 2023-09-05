"""Table config"""
from typing import Type

from pydantic import BaseModel

from upy.builder import QueryBuilder


class TableConfig(BaseModel):
    """
    Table configuration class
    Used as helper for query builder
        tablename - Name of the table
        query_builder - Class for generating SQL queries. This property is open, because you can create you own
            QueryBuilder by inheritance from the initial class.
        pk - String name of the field, that is primary key. Used to select or delete elements from table
            with direct access to primary key (Table.objects.delete(1)),
            without keyword arguments (Table.objects.delete(id=1))
            or direct table field access (Table.objects.delete(Table.id == 1)).
    """

    tablename: str
    query_builder: Type[QueryBuilder] = QueryBuilder
    pk: str | None = None
