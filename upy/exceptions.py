"""Upy exceptions"""


class UpyException(Exception):
    """
    Base upy exception
    """


class InvalidConditionComparisonInstance(UpyException):
    """
    Raised for errors related to the condition comparison
    When provided instance for comparison has undefined type
    """


class InvalidConditionGroupComparisonInstance(UpyException):
    """
    Raised for errors related to the condition group comparison
    When provided instance for comparison has undefined type
    """


class InvalidOperatorComparison(UpyException):
    """
    Raised for errors related to the fields comparison
    When provided instance for comparison has broken type
    """


class UndefinedTable(UpyException):
    """
    Raised for errors related to the query building
    When table instance was not provided to query builder
    """


class TableConfigRequired(UpyException):
    """
    Raised for errors related to the table building
    When table instance has no config attribute
    """


class InvalidFilterArgument(UpyException):
    """
    Raised for errors related to the query building
    When query builder can not process provided argument type
    """
