r"""
_shared.py

Shared functions under tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season.

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse

from collections import defaultdict
from pathlib     import Path

# Related Third-party Imports
import numpy  as np
import pandas as pd
import psycopg

from psycopg import sql

# Local Application/Library Specific Imports
from lib.structures.utils         import filter_df_by_column_bounds
from lib.esacci_lakes.queries    import DISTINCT_START_DAYS_QUERY
from lib.esacci_lakes.utils.proc import (
    add_argument_esacci_lakes_counts_of_distinct_start_days_csv_path,
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_variable,
    add_argument_local_data_dir_path,
    argument_esacci_lakes_counts_of_distinct_start_days_csv_path_exists,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_variable_is_in_esacci_lakes_variables,
    argument_local_data_dir_path_is_dir,
    read_local_data_csv
)
from lib.esacci_lakes.vars       import (
    ESACCI_LAKES_COVERAGE_LOWER_BOUND,
    LOCAL_DATA_RUN_DATE
)
from lib.proc.utils              import (
    arguments_are_valid as _arguments_are_valid,
    build_parser        as _build_parser,

    add_argument_output,
    argument_output_is_dir_or_missing,
    get_file_paths_from_dir_path_by_extension
)
from wfsel.time.constants               import (
    NUMBER_OF_DAYS_IN_YEAR_LEAP,
    NUMBER_OF_DAYS_IN_WEEK
)

PROG                      = "comp_trend_of_esacci_lakes_variable_over_smoke_season.py"
NUMBER_OF_LOOKAHEAD_WEEKS = 20
NUMBER_OF_LOOKBACK_WEEKS  = 3
WINDOW_SIZE               = 4


# Parser functions
# ==================================================================================================
def build_parser(
) -> argparse.ArgumentParser:
    """
    Builds a :class:`argparse.ArgumentParser`.

    Returns
    -------
    A :class:`argparse.ArgumentParser`.
    """
    return _build_parser(
        PROG,
        "",
        positional_args = [
            add_argument_esacci_lakes_variable,
            add_argument_local_data_dir_path,
            add_argument_esacci_lakes_metadata_csv_path,
            add_argument_esacci_lakes_counts_of_distinct_start_days_csv_path
        ],
        optional_args   = [
            add_argument_output
        ]
    )


# ==================================================================================================


# Validator functions
# ==================================================================================================
def arguments_are_valid(
    args: argparse.Namespace
) -> bool:
    """
    Validates `args`.

    Parameters
    ----------
    args : :class:`argparse.Namespace`
        The arguments

    Returns
    -------
    `True` if all arguments are successfully validated. `False`
    otherwise.
    """
    return _arguments_are_valid(
        args,
        [
            (
                argument_esacci_lakes_variable_is_in_esacci_lakes_variables,
                "esacci_lakes_variable"
            ),
            (
                argument_local_data_dir_path_is_dir,
                "local_data_dir_path"
            ),
            (
                argument_esacci_lakes_metadata_csv_path_exists,
                "esacci_lakes_metadata_csv_path"
            ),
            (
                argument_esacci_lakes_counts_of_distinct_start_days_csv_path_exists,
                "esacci_lakes_counts_of_distinct_start_days_csv_path"
            ),
            (
                argument_output_is_dir_or_missing,
                "output"
            )
        ]
    )


# ==================================================================================================


# System functions
# ==================================================================================================
def get_local_data_csv_paths_by_year(
    local_data_dir_path: Path,
    year:                int
) -> list[Path]:
    """
    Returns the paths of all csv files in `local_data_dir_path /
    "main.py" / LOCAL_DATA_RUN_DATE / str(year)` and its
    subdirectories.

    Parameters
    ----------
    local_data_dir_path : :class:`pathlib.Path`
        The local data directory

    year : :class:`int`
        The year

    Returns
    -------
    A sorted list of :class:`pathlib.Path`.

    Raises
    ------
    NotADirectoryError
        If `local_data_dir_path / "main.py" / LOCAL_DATA_RUN_DATE /
        str(year)` does not exist.
    """
    dir_path = local_data_dir_path / "main.py" / LOCAL_DATA_RUN_DATE / str(year)

    if not dir_path.is_dir():
        raise NotADirectoryError(f"expected `{dir_path}` to be an existing directory")

    return get_file_paths_from_dir_path_by_extension(
        dir_path,
        "csv"
    )


# ==================================================================================================


# Years functions
# ==================================================================================================
def get_esacci_lakes_years_df(
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame,
    *,
    lower_bound: float | None = None,
    upper_bound: float | None = None
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of each lake's years whose
    count of distinct start days is in [`lower_bound`,
    `upper_bound`].

    Parameters
    ----------
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
    A :class:`pandas.DataFrame` with columns "esacci_lakes_id" and
    "year", and one row per qualifying (lake, year) pair.
    """
    counts_of_distinct_start_days_long_df = (
        esacci_lakes_counts_of_distinct_start_days_df
        .rename(columns = int)
        .melt(
            ignore_index = False,
            var_name     = "year",
            value_name   = "count_of_distinct_start_days"
        )
        .reset_index()
    )

    counts_of_distinct_start_days_long_df = filter_df_by_column_bounds(
        counts_of_distinct_start_days_long_df,
        "count_of_distinct_start_days",
        lower = lower_bound,
        upper = upper_bound
    )

    return (
        counts_of_distinct_start_days_long_df
        .drop(columns = "count_of_distinct_start_days")
        .reset_index(drop = True)
    )


# ==================================================================================================


# Smoke season functions
# ==================================================================================================
def get_esacci_lakes_distinct_start_days_ser(
    esacci_lakes_id: int,
    year:            int,
    cursor:          psycopg.Cursor
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of `esacci_lakes_id`'s distinct
    start days in `year`.

    Parameters
    ----------
    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    year : :class:`int`
        The year

    cursor : :class:`psycopg.Cursor`
        The cursor

    Returns
    -------
    A :class:`pandas.Series`.
    """
    query = DISTINCT_START_DAYS_QUERY.format(table = sql.Identifier(f"hms_smokes{year}"))

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


# ==================================================================================================


# Smoke season range functions
# ==================================================================================================
def get_esacci_lakes_smoke_season_range(
    esacci_lakes_id: int,
    year:            int,
    connection:      psycopg.Connection
) -> tuple[int, int, int]:
    """
    Returns `year` and the first and last days of `esacci_lakes_id`'s
    smoke season in `year`.

    Parameters
    ----------
    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    year : :class:`int`
        The year

    connection : :class:`psycopg.Connection`
        The connection

    Returns
    -------
    A tuple of `year`, the first day of the smoke season, and the last
    day of the smoke season. Both the first day of the smoke season and
    the last day of the smoke season are `-1` if either is invalid.
    """
    with connection.cursor() as cursor:
        distinct_start_days_ser = get_esacci_lakes_distinct_start_days_ser(
            esacci_lakes_id,
            year,
            cursor
        )

    first_day_of_smoke_season = get_first_day_of_smoke_season(distinct_start_days_ser)
    last_day_of_smoke_season  = get_last_day_of_smoke_season(distinct_start_days_ser)

    if (
        first_day_of_smoke_season == -1 or
        last_day_of_smoke_season == -1
    ):
        first_day_of_smoke_season = -1
        last_day_of_smoke_season  = -1

    return (
        year,
        first_day_of_smoke_season,
        last_day_of_smoke_season
    )


def get_esacci_lakes_smoke_season_ranges_df(
    esacci_lakes_years_df: pd.DataFrame,
    connection:            psycopg.Connection
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of the smoke season ranges of
    `esacci_lakes_years_df`.

    Parameters
    ----------
    esacci_lakes_years_df : :class:`pandas.DataFrame`
        The dataframe

    connection : :class:`psycopg.Connection`
        The connection

    Returns
    -------
    A :class:`pandas.DataFrame` with columns "esacci_lakes_id", "year",
    "first_day_of_smoke_season", and "last_day_of_smoke_season".
    """
    return pd.DataFrame(
        [
            (
                esacci_lakes_id,
                *get_esacci_lakes_smoke_season_range(
                    esacci_lakes_id,
                    year,
                    connection
                )
            )
            for (
                esacci_lakes_id,
                year
            )
            in zip(
                esacci_lakes_years_df["esacci_lakes_id"],
                esacci_lakes_years_df["year"]
            )
        ],
        columns = [
            "esacci_lakes_id",
            "year",
            "first_day_of_smoke_season",
            "last_day_of_smoke_season"
        ]
    )


def get_first_day_of_smoke_season(
    distinct_start_days_ser: pd.Series
) -> int:
    """
    Returns the earliest day of the first window that spans fewer than
    `NUMBER_OF_DAYS_IN_A_WEEK` days.

    Parameters
    ----------
    distinct_start_days_ser : :class:`pandas.Series`
        A sorted :class:`pandas.Series` of distinct start days

    Returns
    -------
    `distinct_start_days_ser[i - (WINDOW_SIZE - 1)]` for the smallest
    `i` satisfying the condition in `Notes`, or `-1` if no such `i`
    exists.

    Notes
    -----
    A day at index `i` qualifies if `distinct_start_days_ser[i] -
    distinct_start_days_ser[i - (WINDOW_SIZE - 1)] <
    NUMBER_OF_DAYS_IN_A_WEEK`. `distinct_start_days_ser` is searched in
    ascending order.
    """
    for i in range(
        WINDOW_SIZE - 1,
        len(distinct_start_days_ser)
    ):
        if distinct_start_days_ser[i] - distinct_start_days_ser[i - (WINDOW_SIZE - 1)] < NUMBER_OF_DAYS_IN_WEEK:
            return distinct_start_days_ser[i - (WINDOW_SIZE - 1)]

    return -1


def get_last_day_of_smoke_season(
    distinct_start_days_ser: pd.Series
) -> int:
    """
    Returns the latest day of the last window that spans fewer than
    `NUMBER_OF_DAYS_IN_A_WEEK` days.

    Parameters
    ----------
    distinct_start_days_ser : :class:`pandas.Series`
        A sorted :class:`pandas.Series` of distinct start days

    Returns
    -------
    `distinct_start_days_ser[i]` for the largest `i` satisfying the
    condition in `Notes`, or `-1` if no such `i` exists.

    Notes
    -----
    A day at index `i` qualifies if `distinct_start_days_ser[i] -
    distinct_start_days_ser[i - (WINDOW_SIZE - 1)] <
    NUMBER_OF_DAYS_IN_A_WEEK`. `distinct_start_days_ser` is searched in
    descending order.
    """
    for i in reversed(
        range(
            WINDOW_SIZE - 1,
            len(distinct_start_days_ser)
        )
    ):
        if distinct_start_days_ser[i] - distinct_start_days_ser[i - (WINDOW_SIZE - 1)] < NUMBER_OF_DAYS_IN_WEEK:
            return distinct_start_days_ser[i]

    return -1


def get_week_index(
    first_day: int,
    day:       int
) -> int:
    """
    Returns the index of the week containing `day`, relative to
    `first_day`.

    Parameters
    ----------
    first_day : :class:`int`
        The first day

    day : :class:`int`
        The day to find the week index for

    Returns
    -------
    The week index, such that 0 is the week index containing
    `first_day`.
    """
    return (day - first_day) // NUMBER_OF_DAYS_IN_WEEK


# ==================================================================================================


# Interest range functions
# ==================================================================================================
def get_esacci_lakes_interest_range(
    esacci_lakes_smoke_season_range: tuple[int, int, int]
) -> tuple[int, int, int]:
    """
    Returns `esacci_lakes_smoke_season_range`'s year and the first and
    last days of interest.

    Parameters
    ----------
    esacci_lakes_smoke_season_range : tuple[:class:`int`, :class:`int`, :class:`int`]
        The year and the first and last days of the smoke season

    Returns
    -------
    A tuple of the year, the first day of interest, and the last day of
    interest. Both the first day of interest and last day of interest
    are `-1` if either is invalid.
    """
    (
        year,
        first_day_of_smoke_season,
        last_day_of_smoke_season
    ) = esacci_lakes_smoke_season_range

    first_day_of_interest = get_first_day_of_interest(first_day_of_smoke_season)
    last_day_of_interest  = get_last_day_of_interest(
        first_day_of_smoke_season,
        last_day_of_smoke_season
    )

    if (
        first_day_of_interest == -1 or
        last_day_of_interest == -1
    ):
        first_day_of_interest = -1
        last_day_of_interest  = -1

    return (
        year,
        first_day_of_interest,
        last_day_of_interest
    )


def get_esacci_lakes_interest_ranges_df(
    esacci_lakes_smoke_season_ranges_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of the interest ranges of
    `esacci_lakes_smoke_season_ranges_df`.

    Parameters
    ----------
    esacci_lakes_smoke_season_ranges_df : :class:`pandas.DataFrame`
        The smoke season ranges, with columns "esacci_lakes_id", "year",
        "first_day_of_smoke_season", and "last_day_of_smoke_season"

    Returns
    -------
    A :class:`pandas.DataFrame` with columns "esacci_lakes_id", "year",
    "first_day_of_interest", and "last_day_of_interest".
    """
    return pd.DataFrame(
        [
            (
                esacci_lakes_id,
                *get_esacci_lakes_interest_range(esacci_lakes_smoke_season_range)
            )
            for (
                esacci_lakes_id,
                esacci_lakes_smoke_season_range
            )
            in zip(
                esacci_lakes_smoke_season_ranges_df["esacci_lakes_id"],
                esacci_lakes_smoke_season_ranges_df[
                    [
                        "year",
                        "first_day_of_smoke_season",
                        "last_day_of_smoke_season"
                    ]
                ].itertuples(index = False)
            )
        ],
        columns = [
            "esacci_lakes_id",
            "year",
            "first_day_of_interest",
            "last_day_of_interest"
        ]
    )


def get_first_day_of_interest(
    first_day_of_smoke_season: int
) -> int:
    """
    Returns the first day of interest.

    Parameters
    ----------
    first_day_of_smoke_season : :class:`int`
        The first day of the smoke season

    Returns
    -------
    The day `NUMBER_OF_LOOKBACK_WEEKS` weeks before
    `first_day_of_smoke_season`, or `-1` if `first_day_of_smoke_season`
    is not a day of the year or that day is less than 1.
    """
    if (
        first_day_of_smoke_season < 1 or
        first_day_of_smoke_season > NUMBER_OF_DAYS_IN_YEAR_LEAP
    ):
        return -1

    number_of_lookback_days = NUMBER_OF_LOOKBACK_WEEKS * NUMBER_OF_DAYS_IN_WEEK
    first_day_of_interest   = first_day_of_smoke_season - number_of_lookback_days

    if first_day_of_interest < 1:
        return -1

    return first_day_of_interest


def get_last_day_of_interest(
    first_day_of_smoke_season: int,
    last_day_of_smoke_season:  int
) -> int:
    """
    Returns the last day of interest.

    Parameters
    ----------
    first_day_of_smoke_season : :class:`int`
        The first day of the smoke season

    last_day_of_smoke_season : :class:`int`
        The last day of the smoke season

    Returns
    -------
    The last day of the week containing `last_day_of_smoke_season`, with
    weeks counted from `first_day_of_smoke_season`, or `-1` if either
    input is not a day of the year or that day is greater than
    `NUMBER_OF_DAYS_IN_A_LEAP_YEAR`.
    """
    if (
        first_day_of_smoke_season < 1 or
        first_day_of_smoke_season > NUMBER_OF_DAYS_IN_YEAR_LEAP or
        last_day_of_smoke_season < 1 or
        last_day_of_smoke_season > NUMBER_OF_DAYS_IN_YEAR_LEAP
    ):
        return -1

    week_index = get_week_index(
        first_day_of_smoke_season,
        last_day_of_smoke_season
    )
    week_number = week_index + 1

    number_of_lookahead_days = week_number * NUMBER_OF_DAYS_IN_WEEK - 1
    last_day_of_interest     = first_day_of_smoke_season + number_of_lookahead_days

    if last_day_of_interest > NUMBER_OF_DAYS_IN_YEAR_LEAP:
        return -1

    return last_day_of_interest


# ==================================================================================================


# Local data functions
# ==================================================================================================
def get_esacci_lakes_local_data_means_by_week_index(
    esacci_lakes_variable: str,
    local_data_dir_path:   Path,
    *,
    esacci_lakes_id:       int,
    year:                  int,
    first_day_of_interest: int,
    last_day_of_interest:  int
) -> dict[str, float]:
    """
    Returns a dict of the weekly means of `esacci_lakes_variable` for
    `esacci_lakes_id` over days `first_day_of_interest` through
    `last_day_of_interest` in `year`.

    Parameters
    ----------
    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    local_data_dir_path : :class:`pathlib.Path`
        The local data directory

    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    year : :class:`int`
        The year

    first_day_of_interest : :class:`int`
        The first day of interest

    last_day_of_interest : :class:`int`
        The last day of interest

    Returns
    -------
    A dict mapping "w_{n}" to the mean of that week's daily values,
    where "w_0" is the week beginning `NUMBER_OF_LOOKBACK_WEEKS` weeks
    after `first_day_of_interest`. Weeks beyond
    `NUMBER_OF_LOOKAHEAD_WEEKS` are omitted. A day on which
    `esacci_lakes_id` is absent, or has coverage below
    `ESACCI_LAKES_COVERAGE_LOWER_BOUND`, adds no value. Empty if either
    day of interest is `-1`.
    """
    if (
        first_day_of_interest == -1 or
        last_day_of_interest == -1
    ):
        return {}

    local_data_values_by_week_index = get_esacci_lakes_local_data_values_by_week_index(
        esacci_lakes_variable,
        local_data_dir_path,
        esacci_lakes_id       = esacci_lakes_id,
        year                  = year,
        first_day_of_interest = first_day_of_interest,
        last_day_of_interest  = last_day_of_interest
    )

    return {
        f"w_{week_index - NUMBER_OF_LOOKBACK_WEEKS}": np.nanmean(values)
        for (
            week_index,
            values
        )
        in local_data_values_by_week_index.items()
        if week_index - NUMBER_OF_LOOKBACK_WEEKS <= NUMBER_OF_LOOKAHEAD_WEEKS
    }


def get_esacci_lakes_local_data_means_by_week_index_df(
    esacci_lakes_interest_ranges_df: pd.DataFrame,
    esacci_lakes_variable:           str,
    local_data_dir_path:             Path
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of the weekly means of
    `esacci_lakes_variable` over each interest range in
    `esacci_lakes_interest_ranges_df`.

    Parameters
    ----------
    esacci_lakes_interest_ranges_df : :class:`pandas.DataFrame`
        The interest ranges, with columns "esacci_lakes_id", "year",
        "first_day_of_interest", and "last_day_of_interest"

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    local_data_dir_path : :class:`pathlib.Path`
        The local data directory

    Returns
    -------
    A :class:`pandas.DataFrame` with one row per row of
    `esacci_lakes_interest_ranges_df` and columns "esacci_lakes_id",
    "year", and one column per week, named "w_{n}".
    """
    return pd.DataFrame(
        [
            {
                "esacci_lakes_id": esacci_lakes_id,
                "year":            year,
                **get_esacci_lakes_local_data_means_by_week_index(
                    esacci_lakes_variable,
                    local_data_dir_path,
                    esacci_lakes_id       = esacci_lakes_id,
                    year                  = year,
                    first_day_of_interest = first_day_of_interest,
                    last_day_of_interest  = last_day_of_interest
                )
            }
            for (
                esacci_lakes_id,
                year,
                first_day_of_interest,
                last_day_of_interest
            )
            in zip(
                esacci_lakes_interest_ranges_df["esacci_lakes_id"],
                esacci_lakes_interest_ranges_df["year"],
                esacci_lakes_interest_ranges_df["first_day_of_interest"],
                esacci_lakes_interest_ranges_df["last_day_of_interest"]
            )
        ]
    )


def get_esacci_lakes_local_data_values_by_week_index(
    esacci_lakes_variable: str,
    local_data_dir_path:   Path,
    *,
    esacci_lakes_id:       int,
    year:                  int,
    first_day_of_interest: int,
    last_day_of_interest:  int
) -> dict[int, list[float]]:
    """
    Returns a dict of the weekly values of `esacci_lakes_variable` for
    `esacci_lakes_id` over days `first_day_of_interest` through
    `last_day_of_interest` in `year`.

    Parameters
    ----------
    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    local_data_dir_path : :class:`pathlib.Path`
        The local data directory

    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    year : :class:`int`
        The year

    first_day_of_interest : :class:`int`
        The first day of interest

    last_day_of_interest : :class:`int`
        The last day of interest

    Returns
    -------
    A dict mapping week index to a list of that week's daily values,
    where week index 0 is the week beginning on `first_day_of_interest`.
    A day on which `esacci_lakes_id` is absent, or has coverage below
    `ESACCI_LAKES_COVERAGE_LOWER_BOUND`, adds no value.

    Raises
    ------
    ValueError
        If `first_day_of_interest` is less than 1, or if
        `last_day_of_interest` is greater than the number of local data
        csv files in `year`.
    """
    local_data_csv_paths = get_local_data_csv_paths_by_year(
        local_data_dir_path,
        year
    )

    if first_day_of_interest < 1:
        raise ValueError("expected `first_day_of_interest` to be >= 1")

    if last_day_of_interest > len(local_data_csv_paths):
        raise ValueError("expected `last_day_of_interest` to be <= `len(local_data_csv_paths)`")

    local_data_values_by_week_index = defaultdict(list)

    for day in range(
        first_day_of_interest,
        last_day_of_interest + 1
    ):
        week_index = get_week_index(
            first_day_of_interest,
            day
        )

        local_data_df = read_local_data_csv(local_data_csv_paths[day - 1])
        local_data_df = filter_df_by_column_bounds(
            local_data_df,
            f"{esacci_lakes_variable}_coverage",
            lower = ESACCI_LAKES_COVERAGE_LOWER_BOUND
        )

        if esacci_lakes_id in local_data_df.index:
            local_data_values_by_week_index[week_index].append(local_data_df[f"{esacci_lakes_variable}_mean"].loc[esacci_lakes_id].item())

    return local_data_values_by_week_index


# ==================================================================================================



