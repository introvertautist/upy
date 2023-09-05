"""Table model"""
from upy.core.table_model import BaseTableModel
from upy.table.table_meta import TableMetaclass


class TableModel(BaseTableModel, metaclass=TableMetaclass):
    """
    Base class for all tables
    """
