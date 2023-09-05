"""Condition utils"""


def push_with_reverse(first: list, second: list) -> None:  # TODO: Crutch
    """
    Modify initial list and insert items from second
    :param first: List to be modified
    :param second: List of values for insert
    :return: None
    """
    for item in second:
        first.insert(0, item)
