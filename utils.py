"""Helper functions for the app."""

from typing import List
from models import Tasks


def sum_points(tasks: List[Tasks]) -> int:
    """Sum all points for the given list of task instances from `Tasks`
    table.

    :param tasks: list of tasks from `Tasks` table
    :return: total number of points rounded
    """
    total = 0
    for row in tasks:
        total += row.point

    return round(total)


def filter_positive(tasks: List[Tasks]) -> list:
    """Filter tasks to return just positive ones.

    :param tasks: list of tasks from `Tasks` table
    :return: list of positive row values
    """

    return [t for t in tasks if t.pn]


def filter_negative(tasks: List[Tasks]) -> list:
    """Filter tasks to return just negative ones.

    :param tasks: list of tasks from `Tasks` table
    :return: list of negative row values
    """

    return [t for t in tasks if not t.pn]
