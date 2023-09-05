"""Table metaclass"""
from typing import Any, Type

# noinspection PyProtectedMember
from pydantic._internal._model_construction import ModelMetaclass

from upy.core.abstract_builder import AbstractQueryBuilder
from upy.core.table_model import BaseTableModel
from upy.exceptions import TableConfigRequired
from upy.fields.field import TableField


class TableMetaclass(ModelMetaclass):
    """
    Base table metaclass
    Used for generating new table classes
    Update attributes and cast it to TableField for query building
    """

    def __new__(  # type: ignore[misc] # pylint: disable=arguments-differ
        mcs: Type[BaseTableModel], name: str, bases: Any, attrs: dict
    ) -> BaseTableModel:
        """
        Create new instance of TableModel
        :param name: Instance name
        :param bases: Instance parent classes
        :param attrs:Instance attributes
        :return: New instance of TableModel
        """
        new_model: BaseTableModel = super().__new__(mcs, name, bases, attrs)  # type: ignore[misc]

        if bases[0] != BaseTableModel:
            if not hasattr(new_model, "config"):
                raise TableConfigRequired()

            for field_name, _ in new_model.model_fields.items():
                setattr(
                    new_model,
                    field_name,
                    TableField(name=field_name, prefix=new_model.config.tablename),
                )

        return new_model

    def __getattr__(cls, item: str) -> Any:
        """
        Get overridden attribute
        :param item: Attribute name
        :return: TableField or defined attributes in TableModel
        """
        return object.__getattribute__(cls, item)

    @property
    def objects(cls) -> AbstractQueryBuilder:
        """
        Access to query builder
        :return: New instance of QueryBuilder
        """
        return cls.config.query_builder(table=cls)

    @property
    def sql(cls) -> str:
        """
        Table SQL representation
        :return: SQL-string
        """
        return cls.config.tablename

    @property
    def params(cls) -> list[Any]:
        """
        Execution parameters, related to the table SQL
        :return: List of parameters
        """
        return []
