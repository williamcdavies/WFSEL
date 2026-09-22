r"""
utils.py

Description:
    Provides definitions for time-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
from datetime import datetime


def get_now_as_date_string(
) -> str:
    """
    Returns the current time as a date string.

    Returns
    -------
    A :class:`str`.
    """
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def get_year_from_datetime(
    time: datetime
) -> str:
    """
    Returns `time`'s year, as a zero-padded four-digit string.

    Parameters
    ----------
    time : :class:`datetime.datetime`
        The datetime

    Returns
    -------
    A :class:`str`.
    """
    return time.strftime("%Y")


def get_month_from_datetime(
    time: datetime
) -> str:
    """
    Returns `time`'s month, as a zero-padded two-digit string.

    Parameters
    ----------
    time : :class:`datetime.datetime`
        The datetime

    Returns
    -------
    A :class:`str`.
    """
    return time.strftime("%m")