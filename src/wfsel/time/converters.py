"""
Filename:   wfsel.time.converters.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""


def to_index(
    day: int,
) -> int:
    """
    Convert a day to an index.

    Parameters
    ----------
    day : int
        The day

    Returns
    -------
    int
        An index
    """
    index = day - 1

    return index


def to_day(
    index: int,
) -> int:
    """
    Convert an index to a day.

    Parameters
    ----------
    index : int
        The index

    Returns
    -------
    int
        A day
    """
    day = index + 1

    return day
