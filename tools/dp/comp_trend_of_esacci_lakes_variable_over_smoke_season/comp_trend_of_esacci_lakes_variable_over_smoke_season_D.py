r"""
comp_trend_of_esacci_lakes_variable_over_smoke_season.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from collections import defaultdict
from pathlib     import Path

# Related Third-party Imports
import numpy  as np
import pandas as pd
import psycopg

from psycopg import sql
from tqdm    import tqdm

# Local Application/Library Specific Imports
from lib.dataframe.utils         import (
    subtract_columns_from_df,
    filter_df_by_column_bounds,
    intersect_dfs_by_columns,
    intersect_dfs_by_cells,
    sort_df_columns_numerically
)
from lib.esacci_lakes.utils.proc import (
    add_argument_esacci_lakes_variable,
    add_argument_local_data_dir_path,
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_counts_of_distinct_start_days_csv_path,
    argument_esacci_lakes_variable_is_in_esacci_lakes_variables,
    argument_local_data_dir_path_exists,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_counts_of_distinct_start_days_csv_path_exists,
    read_local_data_csv,
    read_esacci_lakes_metadata_csv,
    read_esacci_lakes_counts_of_distinct_start_days_csv
)
from lib.esacci_lakes.vars       import (
    COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND,
    COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND
)
from lib.esacci_lakes.queries    import COUNT_OF_DISTINCT_START_DAYS_QUERY
from lib.proc.utils              import (
    add_argument_output,
    argument_output_is_a_directory
)
from lib.proc.vars               import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)

PROG                     = "comp_trend_of_esacci_lakes_variable_over_smoke_season.py"
LOCAL_DATA_RUN_DATE      = "22-09-26"
NUMBER_OF_LOOKBACK_WEEKS = 3
NUMBER_OF_DAYS_IN_A_WEEK = 7


# Argument functions
# ==================================================================================================
def build_parser(
    prog: str
) -> argparse.ArgumentParser:
    """
    Builds a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    prog : :class:`str`
        The program name

    Returns
    -------
    A :class:`argparse.ArgumentParser`.
    """
    parser = argparse.ArgumentParser(
        prog        = prog,
        usage       = "%(prog)s [options]",
        description = """Produces a comparison of each lake's mean value for an ESA CCI Lakes variable over its high-smoke and low-smoke seasons, using the average of every qualifying high-smoke year and the average of every qualifying low-smoke year."""
    )

    # Positional arguments
    add_argument_esacci_lakes_variable(parser)
    add_argument_local_data_dir_path(parser)
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_counts_of_distinct_start_days_csv_path(parser)

    # Optional arguments
    add_argument_output(parser)

    return parser


def arguments_are_valid(
    args: argparse.Namespace
) -> bool:
    """
    Validates `args`.

    Returns
    -------
    `True` if all arguments are successfully validated. `False`
    otherwise.
    """
    if not argument_esacci_lakes_variable_is_in_esacci_lakes_variables(
        args.esacci_lakes_variable,
        loud = True
    ):
        return False

    if not argument_local_data_dir_path_exists(
        args.local_data_dir_path,
        loud = True
    ):
        return False

    if not argument_esacci_lakes_metadata_csv_path_exists(
        args.esacci_lakes_metadata_csv_path,
        loud = True
    ):
        return False

    if not argument_esacci_lakes_counts_of_distinct_start_days_csv_path_exists(
        args.esacci_lakes_counts_of_distinct_start_days_csv_path,
        loud = True
    ):
        return False

    if not argument_output_is_a_directory(
        args.output,
        loud = True
    ):
        return False

    return True


# ==================================================================================================


# Smoke year functions
# ==================================================================================================
def get_esacci_lakes_smoke_years(
    esacci_lakes_id:                               int,
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame,
    *,
    lower_bound: float | None = None,
    upper_bound: float | None = None
) -> list[tuple[str, int]]:
    """
    Returns `esacci_lakes_id`'s years whose count of distinct start
    days is within [`lower_bound`, `upper_bound`].

    Parameters
    ----------
    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes counts of distinct start days

    lower_bound : :class:`float` | `None`
        Inclusive lower bound. If `None`, no lower bound is applied.
        default=None

    upper_bound : :class:`float` | `None`
        Inclusive upper bound. If `None`, no upper bound is applied.
        default=None

    Returns
    -------
    A list of (year, count of distinct start days) pairs, in the
    dataframe's column order, empty if no year qualifies.
    """
    counts_of_distinct_start_days_ser = esacci_lakes_counts_of_distinct_start_days_df.loc[esacci_lakes_id]

    if lower_bound is not None:
        counts_of_distinct_start_days_ser = counts_of_distinct_start_days_ser[counts_of_distinct_start_days_ser >= lower_bound]

    if upper_bound is not None:
        counts_of_distinct_start_days_ser = counts_of_distinct_start_days_ser[counts_of_distinct_start_days_ser <= upper_bound]

    return [
        (
            str(year),
            int(count_of_distinct_start_days)
        )
        for (
            year,
            count_of_distinct_start_days
        )
        in counts_of_distinct_start_days_ser.items()
    ]


def get_esacci_lakes_smoke_years_ser(
    *,
    esacci_lakes_metadata_df:                      pd.DataFrame,
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame,
    lower_bound: float | None = None,
    upper_bound: float | None = None
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of each lake's years whose count
    of distinct start days is within [`lower_bound`, `upper_bound`].

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes counts of distinct start days

    lower_bound : :class:`float` | `None`
        Inclusive lower bound. If `None`, no lower bound is applied.
        default=None

    upper_bound : :class:`float` | `None`
        Inclusive upper bound. If `None`, no upper bound is applied.
        default=None

    Returns
    -------
    A :class:`pandas.Series` of list[(:class:`str`, :class:`int`)]
    indexed by "esacci_lakes_id".
    """
    return pd.Series(
        {
            id_: get_esacci_lakes_smoke_years(
                id_,
                esacci_lakes_counts_of_distinct_start_days_df,
                lower_bound = lower_bound,
                upper_bound = upper_bound
            )
            for id_
            in esacci_lakes_metadata_df.index
        },
        dtype = object
    )


def get_esacci_lakes_high_smoke_years_ser(
    *,
    esacci_lakes_metadata_df:                      pd.DataFrame,
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of each lake's high-smoke years.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes counts of distinct start days

    Returns
    -------
    A :class:`pandas.Series` of list[(:class:`str`, :class:`int`)]
    indexed by "esacci_lakes_id".
    """
    return get_esacci_lakes_smoke_years_ser(
        esacci_lakes_metadata_df                      = esacci_lakes_metadata_df,
        esacci_lakes_counts_of_distinct_start_days_df = esacci_lakes_counts_of_distinct_start_days_df,
        lower_bound                                   = COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND
    )


def get_esacci_lakes_low_smoke_years_ser(
    *,
    esacci_lakes_metadata_df:                      pd.DataFrame,
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of each lake's low-smoke years.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes counts of distinct start days

    Returns
    -------
    A :class:`pandas.Series` of list[(:class:`str`, :class:`int`)]
    indexed by "esacci_lakes_id".
    """
    return get_esacci_lakes_smoke_years_ser(
        esacci_lakes_metadata_df                      = esacci_lakes_metadata_df,
        esacci_lakes_counts_of_distinct_start_days_df = esacci_lakes_counts_of_distinct_start_days_df,
        upper_bound                                   = COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND
    )


def get_esacci_lakes_smoke_year(
    esacci_lakes_id:                               int,
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame,
    *,
    lower_bound: float | None = None,
    upper_bound: float | None = None
) -> list[tuple[str, int]]:
    """
    Returns `esacci_lakes_id`'s most recent year, among years whose count of
    distinct start days is within [`lower_bound`, `upper_bound`].

    Parameters
    ----------
    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes counts of distinct start days

    lower_bound : :class:`float` | `None`
        Inclusive lower bound. If `None`, no lower bound is applied.
        default=None

    upper_bound : :class:`float` | `None`
        Inclusive upper bound. If `None`, no upper bound is applied.
        default=None

    Returns
    -------
    A list containing `esacci_lakes_id`'s most recent (year, count of distinct
    start days) pair, empty if no year qualifies.
    """
    counts_of_distinct_start_days_ser = esacci_lakes_counts_of_distinct_start_days_df.loc[esacci_lakes_id]

    if lower_bound is not None:
        counts_of_distinct_start_days_ser = counts_of_distinct_start_days_ser[counts_of_distinct_start_days_ser >= lower_bound]

    if upper_bound is not None:
        counts_of_distinct_start_days_ser = counts_of_distinct_start_days_ser[counts_of_distinct_start_days_ser <= upper_bound]

    if counts_of_distinct_start_days_ser.empty:
        return []

    year                         = max(counts_of_distinct_start_days_ser.index, key = int)
    count_of_distinct_start_days = counts_of_distinct_start_days_ser.loc[year]

    return [
        (
            str(year),
            int(count_of_distinct_start_days)
        )
    ]


def get_esacci_lakes_smoke_year_ser(
    *,
    esacci_lakes_metadata_df:                      pd.DataFrame,
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame,
    lower_bound: float | None = None,
    upper_bound: float | None = None
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of each lake's most recent year, among
    years whose count of distinct start days is within [`lower_bound`,
    `upper_bound`].

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes counts of distinct start days

    lower_bound : :class:`float` | `None`
        Inclusive lower bound. If `None`, no lower bound is applied.
        default=None

    upper_bound : :class:`float` | `None`
        Inclusive upper bound. If `None`, no upper bound is applied.
        default=None

    Returns
    -------
    A :class:`pandas.Series` of list[(:class:`str`, :class:`int`)]
    indexed by "esacci_lakes_id". Each list has at most one element.
    """
    return pd.Series(
        {
            id_: get_esacci_lakes_smoke_year(
                id_,
                esacci_lakes_counts_of_distinct_start_days_df,
                lower_bound = lower_bound,
                upper_bound = upper_bound
            )
            for id_
            in esacci_lakes_metadata_df.index
        },
        dtype = object
    )


def get_esacci_lakes_high_smoke_year_ser(
    *,
    esacci_lakes_metadata_df:                      pd.DataFrame,
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of each lake's high-smoke year.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes counts of distinct start days

    Returns
    -------
    A :class:`pandas.Series` of list[(:class:`str`, :class:`int`)]
    indexed by "esacci_lakes_id". Each list has at most one element.
    """
    return get_esacci_lakes_smoke_year_ser(
        esacci_lakes_metadata_df                      = esacci_lakes_metadata_df,
        esacci_lakes_counts_of_distinct_start_days_df = esacci_lakes_counts_of_distinct_start_days_df,
        lower_bound                                   = COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND
    )


def get_esacci_lakes_low_smoke_year_ser(
    *,
    esacci_lakes_metadata_df:                      pd.DataFrame,
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of each lake's low-smoke year.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes counts of distinct start days

    Returns
    -------
    A :class:`pandas.Series` of list[(:class:`str`, :class:`int`)]
    indexed by "esacci_lakes_id". Each list has at most one element.
    """
    return get_esacci_lakes_smoke_year_ser(
        esacci_lakes_metadata_df                      = esacci_lakes_metadata_df,
        esacci_lakes_counts_of_distinct_start_days_df = esacci_lakes_counts_of_distinct_start_days_df,
        upper_bound                                   = COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND
    )


# ==================================================================================================


# Smoke season functions
# ==================================================================================================
def get_esacci_lakes_distinct_start_days_ser(
    cursor: psycopg.Cursor,
    *,
    esacci_lakes_id: int,
    year:            str
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of `esacci_lakes_id`'s distinct
    start days within `year`.

    Parameters
    ----------
    cursor : :class:`psycopg.Cursor`
        The cursor

    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    year : :class:`str`
        The year to query

    Returns
    -------
    A :class:`pandas.Series`.
    """
    query = COUNT_OF_DISTINCT_START_DAYS_QUERY.format(table = sql.Identifier(f"hms_smokes{year}"))

    cursor.execute(
        query,
        params = {
            "id": esacci_lakes_id
        }
    )

    return pd.Series(
        [
            record[0]
            for record
            in cursor.fetchall()
        ]
    )


def get_week_idx(
    day_i:                    int,
    day_0:                    int,
    number_of_days_in_a_week: int
) -> int:
    """
    Returns the index of the week containing `day_i`, relative to
    `day_0`.

    Parameters
    ----------
    day_i : :class:`int`
        The day to find the week index for

    day_0 : :class:`int`
        The anchor day

    number_of_days_in_a_week : :class:`int`
        The number of days in a week

    Returns
    -------
    The week index.
    """
    return (day_i - day_0) // number_of_days_in_a_week


def get_first_day_of_smoke_season(
    distinct_start_days_ser: pd.Series
) -> int:
    """
    Returns the earliest day of the first 4-day window in
    `distinct_start_days_ser` that spans less than 7 days.

    Parameters
    ----------
    distinct_start_days_ser : :class:`pandas.Series`
        A sorted :class:`pandas.Series` of smoke event start days

    Returns
    -------
    `distinct_start_days_ser[i - 3]` for the smallest `i` satisfying the
    condition in `Notes`, or `-1` if no such `i` exists.

    Notes
    -----
    A day at index `i` qualifies if `distinct_start_days_ser[i] -
    distinct_start_days_ser[i - 3] < 7`, i.e. it and the 3 preceding
    entries span less than 7 days. Searches `distinct_start_days_ser`
    forward, so the earliest qualifying window is found, and returns
    that window's earliest day.
    """
    for i in range(3, len(distinct_start_days_ser)):
        if distinct_start_days_ser[i] - distinct_start_days_ser[i - 3] < 7:
            return distinct_start_days_ser[i - 3]

    return -1


def get_last_day_of_smoke_season(
    distinct_start_days_ser: pd.Series
) -> int:
    """
    Returns the latest day of the last 4-day window in
    `distinct_start_days_ser` that spans less than 7 days.

    Parameters
    ----------
    distinct_start_days_ser : :class:`pandas.Series`
        A sorted :class:`pandas.Series` of smoke event start days

    Returns
    -------
    The last qualifying day, or `-1` if none is found.

    Notes
    -----
    A day at index `i` qualifies if `distinct_start_days_ser[i] -
    distinct_start_days_ser[i - 3] < 7`, i.e. it and the 3 preceding
    entries span less than 7 days. Searches `distinct_start_days_ser` in
    reverse, so the latest qualifying window is found, and returns that
    window's latest day.
    """
    for i in reversed(range(3, len(distinct_start_days_ser))):
        if distinct_start_days_ser[i] - distinct_start_days_ser[i - 3] < 7:
            return distinct_start_days_ser[i]

    return -1


def get_first_day_of_interest(
    day_of_smoke_season_0:    int,
    number_of_lookback_weeks: int,
    number_of_days_in_a_week: int
) -> int:
    """
    Returns the first day of interest.

    Parameters
    ----------
    day_of_smoke_season_0 : :class:`int`
        The first day of the smoke season

    number_of_lookback_weeks : :class:`int`
        The number of weeks to look back

    number_of_days_in_a_week : :class:`int`
        The number of days in a week

    Returns
    -------
    The first day of interest.
    """
    number_of_lookback_days = number_of_lookback_weeks * number_of_days_in_a_week

    return day_of_smoke_season_0 - number_of_lookback_days


def get_last_day_of_interest(
    day_of_smoke_season_0:    int,
    day_of_smoke_season_n:    int,
    number_of_days_in_a_week: int
) -> int:
    """
    Returns the last day of interest.

    Parameters
    ----------
    day_of_smoke_season_0 : :class:`int`
        The first day of the smoke season

    day_of_smoke_season_n : :class:`int`
        The last day of the smoke season

    number_of_days_in_a_week : :class:`int`
        The number of days in a week

    Returns
    -------
    The last day of interest.
    """
    week_idx = get_week_idx(
        day_of_smoke_season_n,
        day_of_smoke_season_0,
        number_of_days_in_a_week
    )

    number_of_lookahead_days = (week_idx + 1) * number_of_days_in_a_week - 1

    return day_of_smoke_season_0 + number_of_lookahead_days


def get_esacci_lakes_smoke_season_ranges_df(
    connection: psycopg.Connection,
    *,
    esacci_lakes_metadata_df:     pd.DataFrame,
    esacci_lakes_smoke_years_ser: pd.Series
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of each lake's smoke season range.

    Parameters
    ----------
    connection : :class:`psycopg.Connection`
        The connection

    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_smoke_years_ser : :class:`pandas.Series`
        The series, as returned by `get_esacci_lakes_high_smoke_years_ser`

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id", with columns
    "day_of_smoke_season_0" and "day_of_smoke_season_n".
    """
    records = []

    for id_ in esacci_lakes_metadata_df.index:
        tuples = esacci_lakes_smoke_years_ser.loc[id_]

        days_of_smoke_season_0 = []
        days_of_smoke_season_n = []

        for smoke_year, _ in tuples:
            with connection.cursor() as cur:
                distinct_start_days_ser = get_esacci_lakes_distinct_start_days_ser(
                    cur,
                    esacci_lakes_id = id_,
                    year            = smoke_year
                )

            day_0 = get_first_day_of_smoke_season(distinct_start_days_ser)
            day_n = get_last_day_of_smoke_season(distinct_start_days_ser)

            if (
                day_0 != -1
                and day_n != -1
            ):
                days_of_smoke_season_0.append(day_0)
                days_of_smoke_season_n.append(day_n)

        if days_of_smoke_season_0:
            day_of_smoke_season_0 = int(np.floor(np.median(days_of_smoke_season_0)))
            day_of_smoke_season_n = int(np.floor(np.median(days_of_smoke_season_n)))
        else:
            day_of_smoke_season_0 = -1
            day_of_smoke_season_n = -1

        record                          = {"esacci_lakes_id": id_}
        record["day_of_smoke_season_0"] = day_of_smoke_season_0
        record["day_of_smoke_season_n"] = day_of_smoke_season_n

        records.append(record)

    return pd.DataFrame(records).set_index("esacci_lakes_id")


def get_esacci_lakes_interest_ranges_df(
    *,
    esacci_lakes_metadata_df:            pd.DataFrame,
    esacci_lakes_smoke_season_ranges_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of each lake's interest
    ranges.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_smoke_season_ranges_df : :class:`pandas.DataFrame`
        The dataframe, as returned by
        `get_esacci_lakes_smoke_season_ranges_df`

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id", with columns
    "day_of_interest_0" and "day_of_interest_n".
    """
    records = []

    for id_ in esacci_lakes_metadata_df.index:
        day_of_smoke_season_0  = esacci_lakes_smoke_season_ranges_df.loc[id_]["day_of_smoke_season_0"]
        day_of_smoke_season_n  = esacci_lakes_smoke_season_ranges_df.loc[id_]["day_of_smoke_season_n"]

        if (
            day_of_smoke_season_0 != -1
            and day_of_smoke_season_n != -1
        ):
            day_of_interest_0 = get_first_day_of_interest(
                day_of_smoke_season_0,
                NUMBER_OF_LOOKBACK_WEEKS,
                NUMBER_OF_DAYS_IN_A_WEEK
            )
            day_of_interest_n = get_last_day_of_interest(
                day_of_smoke_season_0,
                day_of_smoke_season_n,
                NUMBER_OF_DAYS_IN_A_WEEK
            )

            if (
                day_of_interest_0 < 1
                or day_of_interest_n > 366
            ):
                day_of_interest_0 = -1
                day_of_interest_n = -1
        else:
            day_of_interest_0 = -1
            day_of_interest_n = -1

        record                      = {"esacci_lakes_id": id_}
        record["day_of_interest_0"] = day_of_interest_0
        record["day_of_interest_n"] = day_of_interest_n

        records.append(record)

    return pd.DataFrame(records).set_index("esacci_lakes_id")


# ==================================================================================================


# Local data functions
# ==================================================================================================
def get_local_data_csv_paths_by_year(
    year:                str,
    local_data_dir_path: Path
) -> list[Path]:
    """
    Returns a sorted list of paths to `year`'s local data csv files.

    Parameters
    ----------
    year : :class:`str`
        The year

    local_data_dir_path : :class:`pathlib.Path`
        The local data directory

    Returns
    -------
    A sorted list of :class:`pathlib.Path`.

    Raises
    ------
    NotADirectoryError
        If `local_data_dir_path / "main.py" / LOCAL_DATA_RUN_DATE /
        year` does not exist.
    """
    year_dir_path = local_data_dir_path / "main.py" / LOCAL_DATA_RUN_DATE / year

    if not year_dir_path.is_dir():
        raise NotADirectoryError(f"expected `{year_dir_path}` to be an existing directory")

    return sorted(year_dir_path.glob("**/*.csv"))


def get_esacci_lakes_variable_values_by_week_idx(
    esacci_lakes_id:       int,
    esacci_lakes_variable: str,
    *,
    local_data_csv_paths:     list[Path],
    day_of_interest_0:        int,
    day_of_interest_n:        int,
    number_of_days_in_a_week: int
) -> dict[int, list[float]]:
    """
    Returns `esacci_lakes_id`'s `esacci_lakes_variable` values, bucketed
    by week index, for days `day_of_interest_0` through
    `day_of_interest_n`.

    Parameters
    ----------
    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    local_data_csv_paths : list[:class:`pathlib.Path`]
        Paths to a year's daily local data csv files, one file per day,
        ordered by day of year

    day_of_interest_0 : :class:`int`
        The first day to sample

    day_of_interest_n : :class:`int`
        The last day to sample

    number_of_days_in_a_week : :class:`int`
        The number of days in a week

    Returns
    -------
    A dict mapping week index to a list of daily values.

    Raises
    ------
    ValueError
        If `day_of_interest_0` is less than 1, or if `day_of_interest_n`
        is greater than `len(local_data_csv_paths)`.
    """
    if day_of_interest_0 < 1:
        raise ValueError("expected `day_of_interest_0` to be >= 1")

    if day_of_interest_n > len(local_data_csv_paths):
        raise ValueError("expected `day_of_interest_n` to be <= `len(local_data_csv_paths)`")

    variable_values_by_week_idx = defaultdict(list)

    for day in range(day_of_interest_0, day_of_interest_n + 1):
        week_idx = get_week_idx(
            day,
            day_of_interest_0,
            number_of_days_in_a_week
        )

        local_data_df = read_local_data_csv(local_data_csv_paths[day - 1])
        local_data_df = filter_df_by_column_bounds(
            local_data_df,
            f"""{esacci_lakes_variable}_coverage""",
            lower = 0.5
        )

        if esacci_lakes_id in local_data_df.index:
            column = f"""{esacci_lakes_variable}_mean"""
            value  = local_data_df[column].loc[esacci_lakes_id].item()

            variable_values_by_week_idx[week_idx].append(value)

    return variable_values_by_week_idx


def get_esacci_lakes_variable_mean_by_week_idx(
    esacci_lakes_variable_values_by_week_idx: dict[int, list[float]]
) -> dict[int, float]:
    """
    Returns the mean of each week's values in
    `esacci_lakes_variable_values_by_week_idx`.

    Parameters
    ----------
    esacci_lakes_variable_values_by_week_idx : dict[:class:`int`, list[:class:`float`]]
        A dict mapping week index to a list of values

    Returns
    -------
    A dict mapping week index to the mean of that week's values. A
    week with no values maps to `numpy.nan`.
    """
    return {
        week_idx: (np.nanmean(values) if values else np.nan)
        for week_idx, values
        in esacci_lakes_variable_values_by_week_idx.items()
    }


def get_esacci_lakes_variable_means_ser(
    esacci_lakes_id:       int,
    esacci_lakes_variable: str,
    *,
    smoke_year:          str,
    day_of_interest_0:   int,
    day_of_interest_n:   int,
    local_data_dir_path: Path
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of `esacci_lakes_id`'s
    `esacci_lakes_variable` week means, indexed by "w_{n}", for days
    `day_of_interest_0` through `day_of_interest_n` of `smoke_year`.

    Parameters
    ----------
    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    smoke_year : :class:`str`
        The year to source local data csv files from

    day_of_interest_0 : :class:`int`
        The first day to sample

    day_of_interest_n : :class:`int`
        The last day to sample

    local_data_dir_path : :class:`pathlib.Path`
        The local data directory

    Returns
    -------
    A :class:`pandas.Series` indexed by "w_{n}", restricted to `n <= 20`.
    """
    local_data_csv_paths = get_local_data_csv_paths_by_year(
        smoke_year,
        local_data_dir_path
    )

    variable_values_by_week_idx = get_esacci_lakes_variable_values_by_week_idx(
        esacci_lakes_id,
        esacci_lakes_variable,
        local_data_csv_paths     = local_data_csv_paths,
        day_of_interest_0        = day_of_interest_0,
        day_of_interest_n        = day_of_interest_n,
        number_of_days_in_a_week = NUMBER_OF_DAYS_IN_A_WEEK
    )
    variable_mean_by_week_idx = get_esacci_lakes_variable_mean_by_week_idx(variable_values_by_week_idx)

    return pd.Series(
        {
            f"w_{week_idx - NUMBER_OF_LOOKBACK_WEEKS}": mean
            for week_idx, mean
            in variable_mean_by_week_idx.items()
            if week_idx - NUMBER_OF_LOOKBACK_WEEKS <= 20
        }
    )


def get_esacci_lakes_variable_over_smoke_seasons_df(
    esacci_lakes_metadata_df: pd.DataFrame,
    esacci_lakes_variable:    str,
    *,
    esacci_lakes_smoke_years_ser:    pd.Series,
    esacci_lakes_interest_ranges_df: pd.DataFrame,
    local_data_dir_path:             Path
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of `esacci_lakes_variable`'s
    weekly values over each lake's smoke seasons, averaged across
    every year in `esacci_lakes_smoke_years_ser`.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    esacci_lakes_smoke_years_ser : :class:`pandas.Series`
        The series, as returned by `get_esacci_lakes_high_smoke_years_ser` or
        `get_esacci_lakes_low_smoke_years_ser`

    esacci_lakes_interest_ranges_df : :class:`pandas.DataFrame`
        The dataframe, as returned by
        `get_esacci_lakes_interest_ranges_df`

    local_data_dir_path : :class:`pathlib.Path`
        The local data directory

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id", with one
    column per week, named "w_{n}".
    """
    records = []

    for id_ in tqdm(esacci_lakes_metadata_df.index):
        tuples             = esacci_lakes_smoke_years_ser.loc[id_]
        day_of_interest_0  = esacci_lakes_interest_ranges_df.loc[id_]["day_of_interest_0"]
        day_of_interest_n  = esacci_lakes_interest_ranges_df.loc[id_]["day_of_interest_n"]

        variable_means_sers = []

        if (
            day_of_interest_0 != -1
            and day_of_interest_n != -1
        ):
            for year, _ in tuples:
                variable_means_sers.append(
                    get_esacci_lakes_variable_means_ser(
                        id_,
                        esacci_lakes_variable,
                        smoke_year          = year,
                        day_of_interest_0   = day_of_interest_0,
                        day_of_interest_n   = day_of_interest_n,
                        local_data_dir_path = local_data_dir_path
                    )
                )

        if variable_means_sers:
            variable_mean_ser = pd.concat(
                variable_means_sers,
                axis = 1
            ).mean(
                axis   = 1,
                skipna = True
            )
        else:
            variable_mean_ser = pd.Series(dtype = float)

        record = {"esacci_lakes_id": id_, **variable_mean_ser.to_dict()}

        records.append(record)

    return pd.DataFrame(records).set_index("esacci_lakes_id")


# ==================================================================================================


# Write functions
# ==================================================================================================
def write_esacci_lakes_variable_over_smoke_season_df_to_csv(
    esacci_lakes_variable_over_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable:                      str,
    output:                                     Path,
    *,
    class_: str
) -> None:
    """
    Writes `esacci_lakes_variable_over_smoke_season_df` to a csv file
    in `output`, named "{class_}_smoke_season_{esacci_lakes_variable}.csv".

    Parameters
    ----------
    esacci_lakes_variable_over_smoke_season_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes variable data

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    output : :class:`pathlib.Path`
        The output directory path

    class_ : :class:`str`
        One of "high" or "low"

    Returns
    -------
    None
    """
    output.mkdir(
        parents  = True,
        exist_ok = True
    )

    esacci_lakes_variable_over_smoke_season_df.to_csv(output / f"""{class_}_smoke_season_{esacci_lakes_variable}.csv""")


def write_esacci_lakes_variable_over_high_smoke_season_df_to_csv(
    esacci_lakes_variable_over_high_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable:                           str,
    output:                                          Path
) -> None:
    """
    Writes `esacci_lakes_variable_over_high_smoke_season_df` to a csv
    file in `output`.

    Parameters
    ----------
    esacci_lakes_variable_over_high_smoke_season_df : :class:`pandas.DataFrame`
        The high ESA CCI Lakes variable data

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    output : :class:`pathlib.Path`
        The output directory path

    Returns
    -------
    None
    """
    write_esacci_lakes_variable_over_smoke_season_df_to_csv(
        esacci_lakes_variable_over_high_smoke_season_df,
        esacci_lakes_variable,
        output,
        class_ = "high"
    )


def write_esacci_lakes_variable_over_low_smoke_season_df_to_csv(
    esacci_lakes_variable_over_low_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable:                          str,
    output:                                         Path
) -> None:
    """
    Writes `esacci_lakes_variable_over_low_smoke_season_df` to a csv
    file in `output`.

    Parameters
    ----------
    esacci_lakes_variable_over_low_smoke_season_df : :class:`pandas.DataFrame`
        The low ESA CCI Lakes variable data

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    output : :class:`pathlib.Path`
        The output directory path

    Returns
    -------
    None
    """
    write_esacci_lakes_variable_over_smoke_season_df_to_csv(
        esacci_lakes_variable_over_low_smoke_season_df,
        esacci_lakes_variable,
        output,
        class_ = "low"
    )


def write_esacci_lakes_variable_anomaly_over_smoke_season_df_to_csv(
    esacci_lakes_variable_anomaly_over_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable:                              str,
    output:                                             Path,
    *,
    class_: str
) -> None:
    """
    Writes `esacci_lakes_variable_anomaly_over_smoke_season_df` to a
    csv file in `output`, named
    "{class_}_smoke_season_{esacci_lakes_variable}_anomaly.csv".

    Parameters
    ----------
    esacci_lakes_variable_anomaly_over_smoke_season_df : :class:`pandas.DataFrame`
        The anomalous ESA CCI Lakes variable data

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    output : :class:`pathlib.Path`
        The output directory path

    class_ : :class:`str`
        One of "high" or "low"

    Returns
    -------
    None
    """
    output.mkdir(
        parents  = True,
        exist_ok = True
    )

    esacci_lakes_variable_anomaly_over_smoke_season_df.to_csv(output / f"""{class_}_smoke_season_{esacci_lakes_variable}_anomaly.csv""")


def write_esacci_lakes_variable_anomaly_over_high_smoke_season_df_to_csv(
    esacci_lakes_variable_anomaly_over_high_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable:                                   str,
    output:                                                  Path
) -> None:
    """
    Writes `esacci_lakes_variable_anomaly_over_high_smoke_season_df` to
    a csv file in `output`.

    Parameters
    ----------
    esacci_lakes_variable_anomaly_over_high_smoke_season_df : :class:`pandas.DataFrame`
        The anomalous high ESA CCI Lakes variable data

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    output : :class:`pathlib.Path`
        The output directory path

    Returns
    -------
    None
    """
    write_esacci_lakes_variable_anomaly_over_smoke_season_df_to_csv(
        esacci_lakes_variable_anomaly_over_high_smoke_season_df,
        esacci_lakes_variable,
        output,
        class_ = "high"
    )


def write_esacci_lakes_variable_anomaly_over_low_smoke_season_df_to_csv(
    esacci_lakes_variable_anomaly_over_low_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable:                                  str,
    output:                                                 Path
) -> None:
    """
    Writes `esacci_lakes_variable_anomaly_over_low_smoke_season_df` to
    a csv file in `output`.

    Parameters
    ----------
    esacci_lakes_variable_anomaly_over_low_smoke_season_df : :class:`pandas.DataFrame`
        The anomalous low ESA CCI Lakes variable data

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    output : :class:`pathlib.Path`
        The output directory path

    Returns
    -------
    None
    """
    write_esacci_lakes_variable_anomaly_over_smoke_season_df_to_csv(
        esacci_lakes_variable_anomaly_over_low_smoke_season_df,
        esacci_lakes_variable,
        output,
        class_ = "low"
    )


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    metadata_df                      = read_esacci_lakes_metadata_csv(args.esacci_lakes_metadata_csv_path)
    counts_of_distinct_start_days_df = read_esacci_lakes_counts_of_distinct_start_days_csv(args.esacci_lakes_counts_of_distinct_start_days_csv_path)

    high_smoke_years_ser = get_esacci_lakes_high_smoke_years_ser(
        esacci_lakes_metadata_df                      = metadata_df,
        esacci_lakes_counts_of_distinct_start_days_df = counts_of_distinct_start_days_df
    )
    low_smoke_years_ser  = get_esacci_lakes_low_smoke_years_ser(
        esacci_lakes_metadata_df                      = metadata_df,
        esacci_lakes_counts_of_distinct_start_days_df = counts_of_distinct_start_days_df
    )

    with psycopg.connect("dbname=spatial") as conn:
        smoke_season_ranges_df = get_esacci_lakes_smoke_season_ranges_df(
            conn,
            esacci_lakes_metadata_df     = metadata_df,
            esacci_lakes_smoke_years_ser = high_smoke_years_ser
        )

    interest_ranges_df = get_esacci_lakes_interest_ranges_df(
        esacci_lakes_metadata_df            = metadata_df,
        esacci_lakes_smoke_season_ranges_df = smoke_season_ranges_df
    )

    variable_over_high_smoke_season_df = get_esacci_lakes_variable_over_smoke_seasons_df(
        metadata_df,
        args.esacci_lakes_variable,
        esacci_lakes_smoke_years_ser    = high_smoke_years_ser,
        esacci_lakes_interest_ranges_df = interest_ranges_df,
        local_data_dir_path             = args.local_data_dir_path
    )
    variable_over_low_smoke_season_df  = get_esacci_lakes_variable_over_smoke_seasons_df(
        metadata_df,
        args.esacci_lakes_variable,
        esacci_lakes_smoke_years_ser    = low_smoke_years_ser,
        esacci_lakes_interest_ranges_df = interest_ranges_df,
        local_data_dir_path             = args.local_data_dir_path
    )

    pre_intersect_high_all_nan = variable_over_high_smoke_season_df.isna().all(axis = 1)
    pre_intersect_low_all_nan  = variable_over_low_smoke_season_df.isna().all(axis = 1)

    variable_over_high_smoke_season_df = sort_df_columns_numerically(variable_over_high_smoke_season_df)
    variable_over_low_smoke_season_df  = sort_df_columns_numerically(variable_over_low_smoke_season_df)

    (
        variable_over_high_smoke_season_df,
        variable_over_low_smoke_season_df
    ) = intersect_dfs_by_columns(
        variable_over_high_smoke_season_df,
        variable_over_low_smoke_season_df
    )

    post_column_intersect_high_all_nan = variable_over_high_smoke_season_df.isna().all(axis = 1)
    post_column_intersect_low_all_nan  = variable_over_low_smoke_season_df.isna().all(axis = 1)

    (
        variable_over_high_smoke_season_df,
        variable_over_low_smoke_season_df
    ) = intersect_dfs_by_cells(
        variable_over_high_smoke_season_df,
        variable_over_low_smoke_season_df
    )

    post_cell_intersect_high_all_nan = variable_over_high_smoke_season_df.isna().all(axis = 1)
    # post_cell_intersect_low_all_nan  = variable_over_low_smoke_season_df.isna().all(axis = 1)

    variable_anomaly_over_high_smoke_season_df = subtract_columns_from_df(
        variable_over_high_smoke_season_df,
        [
            "w_-1"
        ]
    )
    variable_anomaly_over_low_smoke_season_df  = subtract_columns_from_df(
        variable_over_low_smoke_season_df,
        [
            "w_-1"
        ]
    )

    post_normalisation_high_all_nan = variable_anomaly_over_high_smoke_season_df.isna().all(axis = 1)
    # post_normalisation_low_all_nan  = variable_anomaly_over_low_smoke_season_df.isna().all(axis = 1)

    write_esacci_lakes_variable_over_high_smoke_season_df_to_csv(
        variable_over_high_smoke_season_df,
        args.esacci_lakes_variable,
        args.output
    )
    write_esacci_lakes_variable_over_low_smoke_season_df_to_csv(
        variable_over_low_smoke_season_df,
        args.esacci_lakes_variable,
        args.output
    )
    write_esacci_lakes_variable_anomaly_over_high_smoke_season_df_to_csv(
        variable_anomaly_over_high_smoke_season_df,
        args.esacci_lakes_variable,
        args.output
    )
    write_esacci_lakes_variable_anomaly_over_low_smoke_season_df_to_csv(
        variable_anomaly_over_low_smoke_season_df,
        args.esacci_lakes_variable,
        args.output
    )

    # Diagnostic bucket counts
    # ==============================================================================================
    total = len(metadata_df)

    no_high_season         = high_smoke_years_ser.apply(len) == 0
    no_low_season          = low_smoke_years_ser.apply(len) == 0
    invalid_season_range   = smoke_season_ranges_df["day_of_smoke_season_0"] == -1
    invalid_interest_range = interest_ranges_df["day_of_interest_0"] == -1

    count_of_lakes_with_no_high_smoke_season         = no_high_season.sum()
    count_of_lakes_with_no_low_smoke_seasons         = (no_low_season & ~no_high_season).sum()
    count_of_lakes_with_no_valid_smoke_season_range  = (invalid_season_range & ~no_high_season & ~no_low_season).sum()
    count_of_lakes_with_no_valid_interest_range      = (invalid_interest_range & ~invalid_season_range & ~no_high_season & ~no_low_season).sum()

    excluded_so_far = (
        no_high_season
        | (no_low_season & ~no_high_season)
        | (invalid_season_range & ~no_high_season & ~no_low_season)
        | (invalid_interest_range & ~invalid_season_range & ~no_high_season & ~no_low_season)
    )

    count_of_lakes_with_no_high_smoke_season_coverage = (pre_intersect_high_all_nan & ~excluded_so_far).sum()

    excluded_so_far = excluded_so_far | (pre_intersect_high_all_nan & ~excluded_so_far)

    count_of_lakes_with_no_low_smoke_season_coverage = (pre_intersect_low_all_nan & ~excluded_so_far).sum()

    excluded_so_far = excluded_so_far | (pre_intersect_low_all_nan & ~excluded_so_far)

    newly_dropped_at_column_intersection = (post_column_intersect_high_all_nan | post_column_intersect_low_all_nan) & ~excluded_so_far

    count_of_lakes_dropped_due_to_column_intersection = newly_dropped_at_column_intersection.sum()

    excluded_so_far = excluded_so_far | newly_dropped_at_column_intersection

    count_of_lakes_dropped_due_to_cell_intersection = (post_cell_intersect_high_all_nan & ~excluded_so_far).sum()

    excluded_so_far = excluded_so_far | (post_cell_intersect_high_all_nan & ~excluded_so_far)

    count_of_lakes_dropped_due_to_normalisation = (post_normalisation_high_all_nan & ~excluded_so_far).sum()

    excluded_so_far = excluded_so_far | (post_normalisation_high_all_nan & ~excluded_so_far)

    count_of_lakes_surviving = total - excluded_so_far.sum()

    print(f"Total lakes: {total}")
    print(f"count_of_lakes_with_no_high_smoke_season: {count_of_lakes_with_no_high_smoke_season}")
    print(f"count_of_lakes_with_no_low_smoke_seasons: {count_of_lakes_with_no_low_smoke_seasons}")
    print(f"count_of_lakes_with_no_valid_smoke_season_range: {count_of_lakes_with_no_valid_smoke_season_range}")
    print(f"count_of_lakes_with_no_valid_interest_range: {count_of_lakes_with_no_valid_interest_range}")
    print(f"count_of_lakes_with_no_high_smoke_season_coverage: {count_of_lakes_with_no_high_smoke_season_coverage}")
    print(f"count_of_lakes_with_no_low_smoke_season_coverage: {count_of_lakes_with_no_low_smoke_season_coverage}")
    print(f"count_of_lakes_dropped_due_to_column_intersection: {count_of_lakes_dropped_due_to_column_intersection}")
    print(f"count_of_lakes_dropped_due_to_cell_intersection: {count_of_lakes_dropped_due_to_cell_intersection}")
    print(f"count_of_lakes_dropped_due_to_normalisation: {count_of_lakes_dropped_due_to_normalisation}")
    print(f"count_of_lakes_surviving: {count_of_lakes_surviving}")

    checksum = (
        count_of_lakes_with_no_high_smoke_season
        + count_of_lakes_with_no_low_smoke_seasons
        + count_of_lakes_with_no_valid_smoke_season_range
        + count_of_lakes_with_no_valid_interest_range
        + count_of_lakes_with_no_high_smoke_season_coverage
        + count_of_lakes_with_no_low_smoke_season_coverage
        + count_of_lakes_dropped_due_to_column_intersection
        + count_of_lakes_dropped_due_to_cell_intersection
        + count_of_lakes_dropped_due_to_normalisation
        + count_of_lakes_surviving
    )

    print(f"Checksum: {checksum} (should equal {total})")
    # ==============================================================================================

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())