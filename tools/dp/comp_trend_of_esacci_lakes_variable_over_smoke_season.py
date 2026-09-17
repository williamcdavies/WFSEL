r"""
comp_trend_of_esacci_lakes_variable_over_smoke_season.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from collections               import defaultdict
from pathlib                   import Path

# Related Third-party Imports
import numpy                   as np
import pandas                  as pd
import psycopg

from psycopg                   import sql
from tqdm                      import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.io import (
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
from lib.math.utils            import (
    filter_df_by_column_bounds,
    intersect_dfs_by_columns,
    intersect_dfs_by_cells,
    normalise_df,
    sort_df_columns_numerically
)
from lib.esacci_lakes.vars     import (
    COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND,
    COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND
)
from lib.esacci_lakes.queries  import COUNT_OF_DISTINCT_START_DAYS_QUERY
from lib.io.vars               import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)

PROG                       = "comp_trend_of_esacci_lakes_variable_over_smoke_season.py"
NUMBER_OF_LOOKBACK_WEEKS   = 3
NUMBER_OF_DAYS_IN_A_WEEK   = 7
NUMBER_OF_LOOKBACK_PERIODS = NUMBER_OF_LOOKBACK_WEEKS
NUMBER_OF_DAYS_IN_A_PERIOD = NUMBER_OF_DAYS_IN_A_WEEK
LOCAL_DATA_RUN_DATE        = "31-08-26"


# Argument functions
# ==================================================================================================
def build_parser(
    prog: str
) -> argparse.ArgumentParser:
    """
    Builds a :class:`ArgumentParser`.

    Parameters
    ----------
    prog : :class:`str`
        The program name

    Returns
    -------
    A :class:`ArgumentParser`.
    """
    parser = argparse.ArgumentParser(
        prog=prog,
        usage="%(prog)s [options]",
        description=""""""
    )

    # Positional arguments
    add_argument_esacci_lakes_variable(parser)
    add_argument_local_data_dir_path(parser)
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_counts_of_distinct_start_days_csv_path(parser)

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
        loud=True
    ):
        return False

    if not argument_local_data_dir_path_exists(
        args.local_data_dir_path,
        loud=True
    ):
        return False

    if not argument_esacci_lakes_metadata_csv_path_exists(
        args.esacci_lakes_metadata_csv_path,
        loud=True
    ):
        return False

    if not argument_esacci_lakes_counts_of_distinct_start_days_csv_path_exists(
        args.esacci_lakes_counts_of_distinct_start_days_csv_path,
        loud=True
    ):
        return False

    return True


# ==================================================================================================


# Smoke year functions
# ==================================================================================================
def get_esacci_lakes_most_recent_smoke_year(
    esacci_lakes_id:                               int,
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame,
    *,
    lower_bound: float | None = None,
    upper_bound: float | None = None
) -> str | None:
    """
    Returns `esacci_lakes_id`'s most recent year whose count of distinct
    start days is within [`lower_bound`, `upper_bound`].

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id

    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    lower_bound : float | None
        Inclusive lower bound. If `None`, no lower bound is applied.
        default=None

    upper_bound : float | None
        Inclusive upper bound. If `None`, no upper bound is applied.
        default=None

    Returns
    -------
    The most recent qualifying year, or `None` if no year qualifies.

    Raises
    ------
    TypeError
        If `esacci_lakes_counts_of_distinct_start_days_df.loc[esacci_lakes_id]`
        is not a :class:`pandas.Series`.

    Notes
    -----
    Internal `.loc` call assumes `esacci_lakes_id` is an existing index
    value in `esacci_lakes_counts_of_distinct_start_days_df`.
    """
    counts_of_distinct_start_days_ser = esacci_lakes_counts_of_distinct_start_days_df.loc[esacci_lakes_id]

    if not isinstance(counts_of_distinct_start_days_ser, pd.Series):
        raise TypeError("expected `esacci_lakes_counts_of_distinct_start_days_df.loc[esacci_lakes_id]` to return a `pandas.Series`")

    if lower_bound is not None:
        counts_of_distinct_start_days_ser = counts_of_distinct_start_days_ser[counts_of_distinct_start_days_ser >= lower_bound]

    if upper_bound is not None:
        counts_of_distinct_start_days_ser = counts_of_distinct_start_days_ser[counts_of_distinct_start_days_ser <= upper_bound]

    if counts_of_distinct_start_days_ser.empty:
        return None

    return counts_of_distinct_start_days_ser.index[-1]


def get_esacci_lakes_most_recent_smoke_years_ser(
    esacci_lakes_metadata_df:                      pd.DataFrame,
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame,
    *,
    lower_bound: float | None = None,
    upper_bound: float | None = None
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of each lake's most recent year
    whose count of distinct start days is within [`lower_bound`,
    `upper_bound`].

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    lower_bound : float | None
        Inclusive lower bound. If `None`, no lower bound is applied.
        default=None

    upper_bound : float | None
        Inclusive upper bound. If `None`, no upper bound is applied.
        default=None

    Returns
    -------
    A :class:`pandas.Series` indexed by "esacci_lakes_id"
    """
    return pd.Series(
        {
            id_: get_esacci_lakes_most_recent_smoke_year(
                id_,
                esacci_lakes_counts_of_distinct_start_days_df,
                lower_bound=lower_bound,
                upper_bound=upper_bound
            )
            for id_
            in esacci_lakes_metadata_df.index
        }
    )


def get_esacci_lakes_most_recent_high_smoke_years_ser(
    esacci_lakes_metadata_df:                      pd.DataFrame,
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of each lake's most recent
    high-smoke year.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    Returns
    -------
    A :class:`pandas.Series` indexed by "esacci_lakes_id", named
    "most_recent_smoke_year".
    """
    return get_esacci_lakes_most_recent_smoke_years_ser(
        esacci_lakes_metadata_df,
        esacci_lakes_counts_of_distinct_start_days_df,
        lower_bound=COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND
    )


def get_esacci_lakes_most_recent_low_smoke_years_ser(
    esacci_lakes_metadata_df:                      pd.DataFrame,
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of each lake's most recent
    low-smoke year.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    Returns
    -------
    A :class:`pandas.Series` indexed by "esacci_lakes_id", named
    "most_recent_smoke_year".
    """
    return get_esacci_lakes_most_recent_smoke_years_ser(
        esacci_lakes_metadata_df,
        esacci_lakes_counts_of_distinct_start_days_df,
        upper_bound=COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND
    )


# ==================================================================================================


# Smoke season functions
# ==================================================================================================
def get_esacci_lakes_distinct_start_days_ser(
    cur:             psycopg.Cursor,
    esacci_lakes_id: int,
    year:            str
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of `esacci_lakes_id`'s distinct
    smoke event start days for `year`.

    Parameters
    ----------
    cur : :class:`psycopg.Cursor`
        The cursor

    esacci_lakes_id : int
        The ESA CCI Lakes id

    year : :class:`str`
        The year to query

    Returns
    -------
    A :class:`pandas.Series`.

    Notes
    -----
    Internal `COUNT_OF_DISTINCT_START_DAYS_QUERY` execution assumes a
    table named "hms_smokes{year}" exists.
    """
    query = COUNT_OF_DISTINCT_START_DAYS_QUERY.format(table=sql.Identifier(f"hms_smokes{year}"))

    cur.execute(
        query,
        params={
            "id": esacci_lakes_id
        }
    )

    return pd.Series(
        [
            record[0]
            for record
            in cur.fetchall()
        ]
    )


def get_period_idx(
    day:                        int,
    day_0:                      int,
    number_of_days_in_a_period: int
) -> int:
    """
    Returns the index of the period containing `day`, relative to
    `day_0`.

    Parameters
    ----------
    day : int
        The day to find the period index for

    day_0 : int
        The anchor day

    number_of_days_in_a_period : int
        The number of days in a period

    Returns
    -------
    The period index.
    """
    return (day - day_0) // number_of_days_in_a_period


def get_first_day_of_smoke_season(
    distinct_start_days_ser: pd.Series
) -> int:
    """
    Returns the first day in `distinct_start_days_ser` whose preceding 3
    entries all fall within a 7-day rolling window.

    Parameters
    ----------
    distinct_start_days_ser : :class:`pandas.Series`
        A sorted :class:`pandas.Series` of smoke event start days

    Returns
    -------
    The first qualifying day, or `-1` if none is found.

    Notes
    -----
    A day at index `i` qualifies if `distinct_start_days_ser[i] -
    distinct_start_days_ser[i - 3] < 7`, i.e. it and the 3 preceding
    entries span less than 7 days.
    """
    for i in range(3, len(distinct_start_days_ser)):
        if distinct_start_days_ser[i] - distinct_start_days_ser[i - 3] < 7:
            return distinct_start_days_ser[i]

    return -1


def get_last_day_of_smoke_season(
    distinct_start_days_ser: pd.Series
) -> int:
    """
    Returns the last day in `distinct_start_days_ser` whose preceding 3
    entries all fall within a 7-day rolling window.

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
    reverse.
    """
    for i in reversed(range(3, len(distinct_start_days_ser))):
        if distinct_start_days_ser[i] - distinct_start_days_ser[i - 3] < 7:
            return distinct_start_days_ser[i]

    return -1


def get_first_day_of_interest(
    day_of_smoke_season_0:      int,
    number_of_lookback_periods: int,
    number_of_days_in_a_period: int
) -> int:
    """
    Returns the first day of interest.

    Parameters
    ----------
    day_of_smoke_season_0 : int
        The first day of the smoke season

    number_of_lookback_periods : int
        The number of periods to look back

    number_of_days_in_a_period : int
        The number of days in a period

    Returns
    -------
    The first day of interest.
    """
    number_of_lookback_days = number_of_lookback_periods * number_of_days_in_a_period

    return day_of_smoke_season_0 - number_of_lookback_days


def get_last_day_of_interest(
    day_of_smoke_season_0:      int,
    day_of_smoke_season_n:      int,
    number_of_days_in_a_period: int
) -> int:
    """
    Returns the last day of interest.

    Parameters
    ----------
    day_of_smoke_season_0 : int
        The first day of the smoke season

    day_of_smoke_season_n : int
        The last day of the smoke season

    number_of_days_in_a_period : int
        The number of days in a period

    Returns
    -------
    The last day of interest.
    """
    period_idx = get_period_idx(
        day_of_smoke_season_n,
        day_of_smoke_season_0,
        number_of_days_in_a_period
    )

    number_of_lookahead_days = (period_idx + 1) * number_of_days_in_a_period - 1

    return day_of_smoke_season_0 + number_of_lookahead_days


def get_esacci_lakes_smoke_season_ranges_df(
    conn:                         psycopg.Connection,
    esacci_lakes_metadata_df:     pd.DataFrame,
    esacci_lakes_smoke_years_ser: pd.Series
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of each lake's smoke season day
    range, computed from `esacci_lakes_smoke_years_ser`.

    Parameters
    ----------
    conn : :class:`psycopg.Connection`
        The connection

    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_smoke_years_ser : :class:`pandas.Series`
        A :class:`pandas.Series` of each lake's smoke year, as
        returned by `get_esacci_lakes_most_recent_high_smoke_years_ser`
        or `get_esacci_lakes_most_recent_low_smoke_years_ser`

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id", with
    columns "day_of_smoke_season_0" and "day_of_smoke_season_n".

    Notes
    -----
    If a lake has no smoke year in `esacci_lakes_smoke_years_ser`, or
    no qualifying smoke season window is found, both
    "day_of_smoke_season_0" and "day_of_smoke_season_n" are set to
    `-1`.
    """
    records = []

    for id_ in esacci_lakes_metadata_df.index:
        smoke_year = esacci_lakes_smoke_years_ser.loc[id_]

        if pd.isna(smoke_year):
            day_of_smoke_season_0 = -1
            day_of_smoke_season_n = -1
        else:
            with conn.cursor() as cur:
                distinct_start_days_ser = get_esacci_lakes_distinct_start_days_ser(
                    cur,
                    id_,
                    smoke_year
                )

            day_of_smoke_season_0 = get_first_day_of_smoke_season(distinct_start_days_ser)
            day_of_smoke_season_n = get_last_day_of_smoke_season(distinct_start_days_ser)

        record                          = {"esacci_lakes_id": id_}
        record["day_of_smoke_season_0"] = day_of_smoke_season_0
        record["day_of_smoke_season_n"] = day_of_smoke_season_n

        records.append(record)

    return pd.DataFrame(records).set_index("esacci_lakes_id")


def get_esacci_lakes_interest_ranges_df(
    esacci_lakes_metadata_df:            pd.DataFrame,
    esacci_lakes_smoke_season_ranges_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of each lake's day-of-interest
    range, computed from `esacci_lakes_smoke_season_ranges_df`.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_smoke_season_ranges_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`, as returned by
        `get_esacci_lakes_smoke_season_ranges_df`

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id", with
    columns "day_of_interest_0" and "day_of_interest_n".

    Notes
    -----
    A lake whose "day_of_smoke_season_0" or "day_of_smoke_season_n" is
    `-1` in `esacci_lakes_smoke_season_ranges_df` has both
    "day_of_interest_0" and "day_of_interest_n" set to `-1`.
    """
    records = []

    for id_ in esacci_lakes_metadata_df.index:
        day_of_smoke_season_0 = esacci_lakes_smoke_season_ranges_df.loc[id_]["day_of_smoke_season_0"]
        day_of_smoke_season_n = esacci_lakes_smoke_season_ranges_df.loc[id_]["day_of_smoke_season_n"]

        if (
            day_of_smoke_season_0 == -1
            or day_of_smoke_season_n == -1
        ):
            day_of_interest_0 = -1
            day_of_interest_n = -1
        else:
            day_of_interest_0 = get_first_day_of_interest(
                day_of_smoke_season_0,
                NUMBER_OF_LOOKBACK_PERIODS,
                NUMBER_OF_DAYS_IN_A_PERIOD
            )
            day_of_interest_n = get_last_day_of_interest(
                day_of_smoke_season_0,
                day_of_smoke_season_n,
                NUMBER_OF_DAYS_IN_A_PERIOD
            )

        record                       = {"esacci_lakes_id": id_}
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

    Notes
    -----
    Internal path construction assumes `local_data_dir_path / "main.py"
    / LOCAL_DATA_RUN_DATE / year` is an existing directory containing
    csv files.
    """
    year_dir_path = local_data_dir_path / "main.py" / LOCAL_DATA_RUN_DATE / year

    if not year_dir_path.is_dir():
        raise NotADirectoryError(f"expected \"{year_dir_path}\" to be an existing directory")

    return sorted(year_dir_path.glob("**/*.csv"))


def get_esacci_lakes_variable_values_by_period_idx(
    esacci_lakes_id:            int,
    esacci_lakes_variable:      str,
    local_data_csv_paths:       list[Path],
    day_of_interest_0:          int,
    day_of_interest_n:          int,
    number_of_days_in_a_period: int
) -> dict[int, list[float]]:
    """
    Returns `esacci_lakes_id`'s `esacci_lakes_variable` values,
    bucketed by period index, for days `day_of_interest_0` through
    `day_of_interest_n`.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    local_data_csv_paths : list[:class:`pathlib.Path`]
        Paths to a year's daily local data csv files, one file per
        day, ordered by day of year

    day_of_interest_0 : int
        The first day to sample

    day_of_interest_n : int
        The last day to sample

    number_of_days_in_a_period : int
        The number of days in a period

    Returns
    -------
    A dict mapping period index to a list of daily values.

    Raises
    ------
    ValueError
        If `day_of_interest_0` is less than 1, or if `day_of_interest_n`
        is greater than `len(local_data_csv_paths)`.

    Notes
    -----
    Only days where `esacci_lakes_id` is present with `coverage >= 50`
    are included. Assumes `local_data_csv_paths[day - 1]` is `day`'s
    file, and that each file has an "esacci_lakes_id" index, a
    "coverage" column, and a "{esacci_lakes_variable}_mean" column.
    """
    if day_of_interest_0 < 1:
        raise ValueError("expected `day_of_interest_0` to be >= 1")

    if day_of_interest_n > len(local_data_csv_paths):
        raise ValueError("expected `day_of_interest_n` to be <= `len(local_data_csv_paths)`")

    variable_values_by_period_idx = defaultdict(list)

    for day in range(day_of_interest_0, day_of_interest_n + 1):
        period_idx = get_period_idx(
            day,
            day_of_interest_0,
            number_of_days_in_a_period
        )

        local_data_df = read_local_data_csv(local_data_csv_paths[day - 1])
        local_data_df = filter_df_by_column_bounds(
            local_data_df,
            "coverage",
            lower=50
        )

        if esacci_lakes_id in local_data_df.index:
            column = f"""{esacci_lakes_variable}_mean"""
            value  = local_data_df[column].loc[esacci_lakes_id].item()

            variable_values_by_period_idx[period_idx].append(value)

    return variable_values_by_period_idx


def get_esacci_lakes_variable_mean_by_period_idx(
    esacci_lakes_variable_values_by_period_idx: dict[int, list[float]]
) -> dict[int, float]:
    """
    Returns the mean of each period's values in
    `esacci_lakes_variable_values_by_period_idx`.

    Parameters
    ----------
    esacci_lakes_variable_values_by_period_idx : dict[int, list[float]]
        A dict mapping period index to a list of values

    Returns
    -------
    A dict mapping period index to the mean of that period's values.
    A period with no values maps to `numpy.nan`.
    """
    return {
        period_idx: (np.nanmean(values) if values else np.nan)
        for period_idx, values
        in esacci_lakes_variable_values_by_period_idx.items()
    }


def get_esacci_lakes_variable_means_ser(
    esacci_lakes_id:        int,
    esacci_lakes_variable:  str,
    most_recent_smoke_year: str,
    day_of_interest_0:      int,
    day_of_interest_n:      int,
    local_data_dir_path:    Path
) -> pd.Series:
    """
    Returns a :class:`pandas.Series` of `esacci_lakes_id`'s
    `esacci_lakes_variable` period means, indexed by "w_{n}", for days
    `day_of_interest_0` through `day_of_interest_n` of
    `most_recent_smoke_year`.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    most_recent_smoke_year : :class:`str`
        The year to source local data csv files from

    day_of_interest_0 : int
        The first day to sample

    day_of_interest_n : int
        The last day to sample

    local_data_dir_path : :class:`pathlib.Path`
        The local data directory

    Returns
    -------
    A :class:`pandas.Series` indexed by "w_{n}".
    """
    local_data_csv_paths = get_local_data_csv_paths_by_year(
        most_recent_smoke_year,
        local_data_dir_path
    )

    variable_values_by_period_idx = get_esacci_lakes_variable_values_by_period_idx(
        esacci_lakes_id,
        esacci_lakes_variable,
        local_data_csv_paths,
        day_of_interest_0,
        day_of_interest_n,
        NUMBER_OF_DAYS_IN_A_PERIOD
    )
    variable_mean_by_period_idx = get_esacci_lakes_variable_mean_by_period_idx(variable_values_by_period_idx)

    return pd.Series(
        {
            f"w_{period_idx - NUMBER_OF_LOOKBACK_PERIODS}": mean
            for period_idx, mean
            in variable_mean_by_period_idx.items()
        }
    )


def get_esacci_lakes_variable_over_smoke_season_df(
    esacci_lakes_metadata_df:                 pd.DataFrame,
    esacci_lakes_variable:                    str,
    esacci_lakes_most_recent_smoke_years_ser: pd.Series,
    esacci_lakes_interest_ranges_df:          pd.DataFrame,
    local_data_dir_path:                      Path
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of `esacci_lakes_variable`'s
    weekly values over each lake's smoke season.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
            The :class:`pandas.DataFrame`

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    esacci_lakes_most_recent_smoke_years_ser : :class:`pandas.Series`
        The :class:`pandas.Series`, as returned by
        `get_esacci_lakes_most_recent_high_smoke_years_ser` or
        `get_esacci_lakes_most_recent_low_smoke_years_ser`

    esacci_lakes_interest_ranges_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`, as returned by
        `get_esacci_lakes_interest_ranges_df`

    local_data_dir_path : :class:`pathlib.Path`
        The local data directory

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id", with one
    column per period, named "w_{n}".

    Notes
    -----
    A lake with no most recent smoke year, or no qualifying smoke
    season window, contributes a row with no period columns. Rows are
    not aligned across a corresponding call for the other smoke level.
    """
    records = []

    for id_ in tqdm(esacci_lakes_metadata_df.index):
        most_recent_smoke_year = esacci_lakes_most_recent_smoke_years_ser.loc[id_]
        day_of_interest_0      = esacci_lakes_interest_ranges_df.loc[id_]["day_of_interest_0"]
        day_of_interest_n      = esacci_lakes_interest_ranges_df.loc[id_]["day_of_interest_n"]

        if (
            not pd.isna(most_recent_smoke_year)
            and day_of_interest_0 != -1
            and day_of_interest_n != -1
        ):
            variable_means_ser = get_esacci_lakes_variable_means_ser(
                id_,
                esacci_lakes_variable,
                most_recent_smoke_year,
                day_of_interest_0,
                day_of_interest_n,
                local_data_dir_path
            )
        else:
            variable_means_ser = pd.Series(dtype=float)

        record = {"esacci_lakes_id": id_, **variable_means_ser.to_dict()}

        records.append(record)

    return pd.DataFrame(records).set_index("esacci_lakes_id")


def get_esacci_lakes_variable_over_high_smoke_season_df(
    esacci_lakes_metadata_df:                      pd.DataFrame,
    esacci_lakes_variable:                         str,
    esacci_lakes_most_recent_high_smoke_years_ser: pd.Series,
    esacci_lakes_interest_ranges_df:               pd.DataFrame,
    local_data_dir_path:                           Path
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of `esacci_lakes_variable`'s
    weekly values over each lake's high-smoke season.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    esacci_lakes_most_recent_high_smoke_years_ser : :class:`pandas.Series`
        The :class:`pandas.Series`, as returned by
        `get_esacci_lakes_most_recent_high_smoke_years_ser`

    esacci_lakes_interest_ranges_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`, as returned by
        `get_esacci_lakes_interest_ranges_df`

    local_data_dir_path : :class:`pathlib.Path`
        The local data directory

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id", with one
    column per period, named "w_{n}".
    """
    return get_esacci_lakes_variable_over_smoke_season_df(
        esacci_lakes_metadata_df,
        esacci_lakes_variable,
        esacci_lakes_most_recent_high_smoke_years_ser,
        esacci_lakes_interest_ranges_df,
        local_data_dir_path
    )


def get_esacci_lakes_variable_over_low_smoke_season_df(
    esacci_lakes_metadata_df:                     pd.DataFrame,
    esacci_lakes_variable:                        str,
    esacci_lakes_most_recent_low_smoke_years_ser: pd.Series,
    esacci_lakes_interest_ranges_df:              pd.DataFrame,
    local_data_dir_path:                          Path
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of `esacci_lakes_variable`'s
    weekly values over each lake's low-smoke season.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    esacci_lakes_most_recent_low_smoke_years_ser : :class:`pandas.Series`
        The :class:`pandas.Series`, as returned by
        `get_esacci_lakes_most_recent_low_smoke_years_ser`

    esacci_lakes_interest_ranges_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`, as returned by
        `get_esacci_lakes_interest_ranges_df`

    local_data_dir_path : :class:`pathlib.Path`
        The local data directory

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id", with one
    column per period, named "w_{n}".
    """
    return get_esacci_lakes_variable_over_smoke_season_df(
        esacci_lakes_metadata_df,
        esacci_lakes_variable,
        esacci_lakes_most_recent_low_smoke_years_ser,
        esacci_lakes_interest_ranges_df,
        local_data_dir_path
    )


# ==================================================================================================


# Write functions
# ==================================================================================================
def write_esacci_lakes_variable_over_smoke_season_df_to_csv(
    esacci_lakes_variable_over_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable:                      str,
    class_:                                     str
) -> None:
    """
    Writes `esacci_lakes_variable_over_smoke_season_df` to a csv file
    named "{class_}_smoke_season_{esacci_lakes_variable}.csv".

    Parameters
    ----------
    esacci_lakes_variable_over_smoke_season_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    class_ : :class:`str`
        One of "high" or "low"

    Returns
    -------
    None
    """
    esacci_lakes_variable_over_smoke_season_df.to_csv(f"""data/dp/{class_}_smoke_season_{esacci_lakes_variable}.csv""")


def write_esacci_lakes_variable_over_high_smoke_season_df_to_csv(
    esacci_lakes_variable_over_high_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable:                           str
) -> None:
    """
    Writes `esacci_lakes_variable_over_high_smoke_season_df` to a csv
    file.

    Parameters
    ----------
    esacci_lakes_variable_over_high_smoke_season_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    Returns
    -------
    None
    """
    write_esacci_lakes_variable_over_smoke_season_df_to_csv(
        esacci_lakes_variable_over_high_smoke_season_df,
        esacci_lakes_variable,
        "high"
    )


def write_esacci_lakes_variable_over_low_smoke_season_df_to_csv(
    esacci_lakes_variable_over_low_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable:                          str
) -> None:
    """
    Writes `esacci_lakes_variable_over_low_smoke_season_df` to a csv
    file.

    Parameters
    ----------
    esacci_lakes_variable_over_low_smoke_season_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    Returns
    -------
    None
    """
    write_esacci_lakes_variable_over_smoke_season_df_to_csv(
        esacci_lakes_variable_over_low_smoke_season_df,
        esacci_lakes_variable,
        "low"
    )


def write_esacci_lakes_variable_anomaly_over_smoke_season_df_to_csv(
    esacci_lakes_variable_anomaly_over_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable:                              str,
    class_:                                             str
) -> None:
    """
    Writes `esacci_lakes_variable_anomaly_over_smoke_season_df` to a
    csv file named
    "{class_}_smoke_season_{esacci_lakes_variable}_anomaly.csv".

    Parameters
    ----------
    esacci_lakes_variable_anomaly_over_smoke_season_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    class_ : :class:`str`
        One of "high" or "low"

    Returns
    -------
    None
    """
    esacci_lakes_variable_anomaly_over_smoke_season_df.to_csv(f"""data/dp/{class_}_smoke_season_{esacci_lakes_variable}_anomaly.csv""")


def write_esacci_lakes_variable_anomaly_over_high_smoke_season_df_to_csv(
    esacci_lakes_variable_anomaly_over_high_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable:                                   str
) -> None:
    """
    Writes `esacci_lakes_variable_anomaly_over_high_smoke_season_df`
    to a csv file.

    Parameters
    ----------
    esacci_lakes_variable_anomaly_over_high_smoke_season_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    Returns
    -------
    None
    """
    write_esacci_lakes_variable_anomaly_over_smoke_season_df_to_csv(
        esacci_lakes_variable_anomaly_over_high_smoke_season_df,
        esacci_lakes_variable,
        "high"
    )


def write_esacci_lakes_variable_anomaly_over_low_smoke_season_df_to_csv(
    esacci_lakes_variable_anomaly_over_low_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable:                                  str
) -> None:
    """
    Writes `esacci_lakes_variable_anomaly_over_low_smoke_season_df` to
    a csv file.

    Parameters
    ----------
    esacci_lakes_variable_anomaly_over_low_smoke_season_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    Returns
    -------
    None
    """
    write_esacci_lakes_variable_anomaly_over_smoke_season_df_to_csv(
        esacci_lakes_variable_anomaly_over_low_smoke_season_df,
        esacci_lakes_variable,
        "low"
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

    most_recent_high_smoke_years_ser = get_esacci_lakes_most_recent_high_smoke_years_ser(
        metadata_df,
        counts_of_distinct_start_days_df
    )
    most_recent_low_smoke_years_ser  = get_esacci_lakes_most_recent_low_smoke_years_ser(
        metadata_df,
        counts_of_distinct_start_days_df
    )

    with psycopg.connect("dbname=spatial") as conn:
        smoke_season_ranges_df = get_esacci_lakes_smoke_season_ranges_df(
            conn,
            metadata_df,
            most_recent_high_smoke_years_ser
        )

    interest_ranges_df = get_esacci_lakes_interest_ranges_df(
        metadata_df,
        smoke_season_ranges_df
    )

    variable_over_high_smoke_season_df = get_esacci_lakes_variable_over_high_smoke_season_df(
        metadata_df,
        args.esacci_lakes_variable,
        most_recent_high_smoke_years_ser,
        interest_ranges_df,
        args.local_data_dir_path
    )
    variable_over_low_smoke_season_df  = get_esacci_lakes_variable_over_low_smoke_season_df(
        metadata_df,
        args.esacci_lakes_variable,
        most_recent_low_smoke_years_ser,
        interest_ranges_df,
        args.local_data_dir_path
    )

    variable_over_high_smoke_season_df = sort_df_columns_numerically(variable_over_high_smoke_season_df)
    variable_over_low_smoke_season_df  = sort_df_columns_numerically(variable_over_low_smoke_season_df)

    (
        variable_over_high_smoke_season_df,
        variable_over_low_smoke_season_df
    ) = intersect_dfs_by_columns(
        variable_over_high_smoke_season_df,
        variable_over_low_smoke_season_df
    )

    (
        variable_over_high_smoke_season_df,
        variable_over_low_smoke_season_df
    ) = intersect_dfs_by_cells(
        variable_over_high_smoke_season_df,
        variable_over_low_smoke_season_df
    )

    variable_anomaly_over_high_smoke_season_df = normalise_df(
        variable_over_high_smoke_season_df,
        "w_-1"
    )
    variable_anomaly_over_low_smoke_season_df  = normalise_df(
        variable_over_low_smoke_season_df,
        "w_-1"
    )

    write_esacci_lakes_variable_over_high_smoke_season_df_to_csv(
        variable_over_high_smoke_season_df,
        args.esacci_lakes_variable
    )
    write_esacci_lakes_variable_over_low_smoke_season_df_to_csv(
        variable_over_low_smoke_season_df,
        args.esacci_lakes_variable
    )
    write_esacci_lakes_variable_anomaly_over_high_smoke_season_df_to_csv(
        variable_anomaly_over_high_smoke_season_df,
        args.esacci_lakes_variable
    )
    write_esacci_lakes_variable_anomaly_over_low_smoke_season_df_to_csv(
        variable_anomaly_over_low_smoke_season_df,
        args.esacci_lakes_variable
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
