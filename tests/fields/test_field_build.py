from upy.fields.field import TableField


def test_field_alias():
    field = TableField(name="column", prefix="table")
    assert field.alias == "table.column"

