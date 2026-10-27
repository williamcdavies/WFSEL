"""
wfsel.time.converters.

Written by William Chuter-Davies
"""


def to_index(
    julian: int,
) -> int:
    """
    Convert a julian to an index.

    Parameters
    ----------
    julian : int
        The julian

    Returns
    -------
    int
        An index
    """
    return julian - 1


def to_day(
    index: int,
) -> int:
    """
    Convert an index to a julian.

    Parameters
    ----------
    index : int
        The index

    Returns
    -------
    int
        A julian
    """
    return index + 1
