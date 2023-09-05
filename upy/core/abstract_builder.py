"""Query builder interface"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from upy.utils import FilterType, Query

TM = TypeVar("TM", bound="TableModel")  # type: ignore[name-defined] # noqa: F821 # pylint: disable=invalid-name


class AbstractQueryBuilder(Generic[TM], ABC):
    """
    Interface for query builder
    """

    @abstractmethod
    def filter(self, *args: FilterType) -> "AbstractQueryBuilder":
        """
        Update where condition
        :param args: Filter arguments
        :return: QueryBuilder
        """

    @abstractmethod
    def build_delete(self, *args: FilterType, strict: bool = True) -> Query:
        """
        Build SQL DELETE query
        Modify provided arguments and cast it to ConditionGroup object
        :param args: Filter arguments
        :param strict: Strict False used to set 'WHERE = true' to prevent PostgreSQL warning on deleting all data
        :return: Query object
        """
