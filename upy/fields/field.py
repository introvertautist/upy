"""Table field"""
from typing import Any

from upy.conditions.condition import Condition
from upy.exceptions import InvalidOperatorComparison
from upy.expressions import Expression


class TableField:
    """
    Base class for table field
    Used only for query building and does not affect to validation and result model building
    """

    def __init__(self, name: str, prefix: str):
        """
        Initialize table field
        :param name: String field name
        :param prefix: String field prefix. Used to restrict access to fields when querying with multiple tables
        """
        self.name: str = name
        self.prefix: str = prefix
        self.alias: str = f"{prefix}.{name}"

    @classmethod
    def from_alias(cls, field: str) -> "TableField":
        """
        Build TableField from field name
        Parse alias of initial field, if it's presented as alias (via '__' or '.')
        :param field: Field name
        :return: TableField object
        """
        if "__" in field:
            _field = field.split("__")
            return cls(name=_field[1], prefix=_field[0])

        if "." in field:
            _field = field.split(".")
            return cls(name=_field[1], prefix=_field[0])

        raise RuntimeError("Invalid alias")

    def __eq__(self, other: Any) -> Condition:  # type: ignore[override]
        """
        Resolve EQUAL (==) operator for fields comparison
        :param other: Instance for comparison
        :return: Condition
        """
        if other is None:
            return Condition(f"{self.alias} IS NULL")

        if isinstance(other, TableField):
            return Condition(f"{self.alias} = {other.alias}")

        if isinstance(other, Expression):
            return Condition(f"{self.alias} = {other.sql}", other.params)

        if isinstance(other, list | tuple | set):
            if len(other) == 0:  # TODO: Maybe not needed?
                return Condition("FALSE")

            sql = ", ".join(["%s" for _ in range(len(other))])
            return Condition(f"{self.alias} IN ({sql})", list(other))

        return Condition(f"{self.alias} = %s", [other])

    def __ne__(self, other: Any) -> Condition:  # type: ignore[override]
        """
        Resolve NOT_EQUAL (!=) operator for fields comparison
        :param other: Instance for comparison
        :return: Condition
        """
        if other is None:
            return Condition(f"{self.alias} IS NOT NULL")

        if isinstance(other, TableField):
            return Condition(f"{self.alias} <> {other.alias}")

        if isinstance(other, Expression):
            return Condition(f"{self.alias} <> {other.sql}", other.params)

        if isinstance(other, list | tuple | set):
            if len(other) < 1:  # TODO: Maybe not needed?
                return Condition("TRUE")

            sql = ", ".join(["%s" for _ in range(len(other))])
            return Condition(f"{self.alias} NOT IN ({sql})", list(other))

        return Condition(f"{self.alias} <> %s", [other])

    def __gt__(self, other: Any) -> Condition:
        """
        Resolve GT (>) operator for fields comparison
        :param other: Instance for comparison
        :return: Condition
        """
        if other is None:
            raise InvalidOperatorComparison("Can not use '>' operator with None")

        if isinstance(other, list | tuple | set):
            raise InvalidOperatorComparison("Can not use '>' operator with list, tuple or set object")

        # TODO: String objects validation
        if isinstance(other, TableField):
            return Condition(f"{self.alias} > {other.alias}")

        if isinstance(other, Expression):
            return Condition(f"{self.alias} > {other.sql}", other.params)

        return Condition(f"{self.alias} > %s", [other])

    def __lt__(self, other: Any) -> Condition:
        """
        Resolve LT (<) operator for fields comparison
        :param other: Instance for comparison
        :return: Condition
        """
        if other is None:
            raise InvalidOperatorComparison("Can not use '<' operator with None")

        if isinstance(other, list | tuple | set):
            raise InvalidOperatorComparison("Can not use '<' operator with list, tuple or set object")

        # TODO: String objects validation
        if isinstance(other, TableField):
            return Condition(f"{self.alias} < {other.alias}")

        if isinstance(other, Expression):
            return Condition(f"{self.alias} < {other.sql}", other.params)

        return Condition(f"{self.alias} < %s", [other])

    def __ge__(self, other: Any) -> Condition:
        """
        Resolve GE (>=) operator for fields comparison
        :param other: Instance for comparison
        :return: Condition
        """
        if other is None:
            raise InvalidOperatorComparison("Can not use '>=' operator with None")

        if isinstance(other, list | tuple | set):
            raise InvalidOperatorComparison("Can not use '>=' operator with list, tuple or set object")

        # TODO: String objects validation
        if isinstance(other, TableField):
            return Condition(f"{self.alias} >= {other.alias}")

        if isinstance(other, Expression):
            return Condition(f"{self.alias} >= {other.sql}", other.params)

        return Condition(f"{self.alias} >= %s", [other])

    def __le__(self, other: Any) -> Condition:
        """
        Resolve LE (<=) operator for fields comparison
        :param other: Instance for comparison
        :return: Condition
        """
        if other is None:
            raise InvalidOperatorComparison("Can not use '<=' operator with None")

        if isinstance(other, list | tuple | set):
            raise InvalidOperatorComparison("Can not use '<=' operator with list, tuple or set object")

        # TODO: String objects validation
        if isinstance(other, TableField):
            return Condition(f"{self.alias} <= {other.alias}")

        if isinstance(other, Expression):
            return Condition(f"{self.alias} <= {other.sql}", other.params)

        return Condition(f"{self.alias} <= %s", [other])

    def __mod__(self, other: Any) -> Condition:
        """
        Resolve MOD (%) operator for fields comparison
        Override initial logic to SQL-LIKE operator
        :param other: Instance for comparison
        :return: Condition
        """
        if other is None:
            raise InvalidOperatorComparison("Can not use '%' (LIKE) operator with None")

        if isinstance(other, list | tuple | set):
            raise InvalidOperatorComparison("Can not use '%' (LIKE) operator with list, tuple or set object")

        if isinstance(other, TableField):
            return Condition(f"{self.alias} LIKE {other.alias}")

        if isinstance(other, Expression):
            return Condition(f"{self.alias} LIKE {other.sql}", other.params)

        return Condition(f"{self.alias} LIKE %s", [other])
