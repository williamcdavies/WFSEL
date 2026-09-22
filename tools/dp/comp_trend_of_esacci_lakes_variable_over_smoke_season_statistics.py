r"""
comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from pathlib import Path

# Related Third-party Imports
import numpy  as np
import pandas as pd

from scipy.stats import ttest_rel

# Local Application/Library Specific Imports
from lib.dataframe.utils import get_ser_from_df
from lib.proc.utils      import (
    add_argument_output,
    argument_output_is_a_directory
)
from lib.proc.vars       import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)

PROG                                            = "comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py"
ALPHA                                           = 0.05
MINIMUM_SAMPLE_SIZE_FOR_ONE_TAILED_PAIRED_TTEST = 5


# Argument functions
# ==================================================================================================
def add_argument_high_lakes_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `high_lakes_csv_path` argument to a
    :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `high_lakes_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "high_lakes_csv_path",
        type = Path,
        help = """path to some high-smoke-season lakes csv file as produced by view_trend_of_esacci_lakes_variable_over_smoke_season.py"""
    )


def add_argument_low_lakes_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `low_lakes_csv_path` argument to a
    :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `low_lakes_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "low_lakes_csv_path",
        type = Path,
        help = """path to some low-smoke-season lakes csv file as produced by view_trend_of_esacci_lakes_variable_over_smoke_season.py"""
    )


def argument_high_lakes_csv_path_exists(
    high_lakes_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `high_lakes_csv_path`.

    Parameters
    ----------
    high_lakes_csv_path : :class:`pathlib.Path`
        The argument `high_lakes_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `high_lakes_csv_path` exists. `False` otherwise.
    """
    if high_lakes_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument high_lakes_csv_path: no such file or directory: {high_lakes_csv_path}""")

    return False


def argument_low_lakes_csv_path_exists(
    low_lakes_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `low_lakes_csv_path`.

    Parameters
    ----------
    low_lakes_csv_path : :class:`pathlib.Path`
        The argument `low_lakes_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `low_lakes_csv_path` exists. `False` otherwise.
    """
    if low_lakes_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument low_lakes_csv_path: no such file or directory: {low_lakes_csv_path}""")

    return False


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
        description = """Computes the longest consecutive cluster of weeks whose paired t-test of a high-smoke-season lakes file against a low-smoke-season lakes file is significant."""
    )

    # Positional arguments
    add_argument_high_lakes_csv_path(parser)
    add_argument_low_lakes_csv_path(parser)

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
    if not argument_high_lakes_csv_path_exists(
        args.high_lakes_csv_path,
        loud = True
    ):
        return False

    if not argument_low_lakes_csv_path_exists(
        args.low_lakes_csv_path,
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


# Read functions
# ==================================================================================================
def read_lakes_csv(
    lakes_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `lakes_csv_path` into a :class:`pandas.DataFrame`.

    Parameters
    ----------
    lakes_csv_path : :class:`pathlib.Path`
        The path to some lakes csv file as produced by
        view_trend_of_esacci_lakes_variable_over_smoke_season.py

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        lakes_csv_path,
        index_col = "esacci_lakes_id"
    )


# ==================================================================================================


# Data functions
# ==================================================================================================
def get_week_numbers(
    high_lakes_df: pd.DataFrame,
    low_lakes_df: pd.DataFrame
) -> set[int]:
    """
    Returns the week numbers common to `high_lakes_df`'s and
    `low_lakes_df`'s "w_{n}" columns.

    Parameters
    ----------
    high_lakes_df : :class:`pandas.DataFrame`
        The dataframe

    low_lakes_df : :class:`pandas.DataFrame`
        The dataframe

    Returns
    -------
    A :class:`set` of :class:`int`.
    """
    prefix  = "w_"

    high_week_numbers = {
        int(c[len(prefix):])
        for c
        in high_lakes_df.columns
        if c.startswith(prefix)
    }
    low_week_numbers  = {
        int(c[len(prefix):])
        for c
        in low_lakes_df.columns
        if c.startswith(prefix)
    }

    return high_week_numbers & low_week_numbers


def get_ttest_result(
    a:           pd.Series,
    b:           pd.Series,
    alternative: str
):
    """
    Returns the paired t-test result of `a` against `b`.

    Parameters
    ----------
    a : :class:`pandas.Series`
        The series

    b : :class:`pandas.Series`
        The series

    alternative : :class:`str`
        The alternative hypothesis

    Returns
    -------
    A :class:`scipy.stats.TtestResult`.

    Raises
    ------
    ValueError
        If `a` and `b` are not of equal length, or not of equal index.
    """
    if len(a) != len(b):
        raise ValueError("expected `a` and `b` to be of equal length")

    if not a.index.equals(b.index):
        raise ValueError("expected `a` and `b` to be of equal index")

    return ttest_rel(
        a,
        b,
        alternative = alternative
    )


def get_ttest_results_ser(
    high_lakes_df: pd.DataFrame,
    low_lakes_df:  pd.DataFrame
) -> pd.Series:
    """
    Returns each common week's paired t-test result of `high_lakes_df`
    against `low_lakes_df`.

    Parameters
    ----------
    high_lakes_df : :class:`pandas.DataFrame`
        The dataframe

    low_lakes_df : :class:`pandas.DataFrame`
        The dataframe

    Returns
    -------
    A :class:`pandas.Series` of :class:`scipy.stats.TtestResult`,
    indexed by "w". A week whose sample size is below
    `MINIMUM_SAMPLE_SIZE_FOR_ONE_TAILED_PAIRED_TTEST` maps to `None`.

    Notes
    -----
    The paired t-test's alternative hypothesis is that `high_lakes_ser`'s
    mean is less than `low_lakes_ser`'s mean.
    """
    results = {}

    week_numbers = get_week_numbers(
        high_lakes_df,
        low_lakes_df
    )

    for week_number in week_numbers:
        high_lakes_ser = get_ser_from_df(
            high_lakes_df,
            f"w_{week_number}"
        ).dropna()
        low_lakes_ser  = get_ser_from_df(
            low_lakes_df,
            f"w_{week_number}"
        ).dropna()

        if (
            len(high_lakes_ser) >= MINIMUM_SAMPLE_SIZE_FOR_ONE_TAILED_PAIRED_TTEST
            and len(low_lakes_ser) >= MINIMUM_SAMPLE_SIZE_FOR_ONE_TAILED_PAIRED_TTEST
        ):
            results[week_number] = get_ttest_result(
                high_lakes_ser,
                low_lakes_ser,
                alternative = "less"
            )
        else:
            results[week_number] = None

    return pd.Series(results)


def get_w_ser(
    high_lakes_df: pd.DataFrame,
    low_lakes_df:  pd.DataFrame
) -> pd.Series:
    """
    Returns the week numbers common to `high_lakes_df`'s and
    `low_lakes_df`'s "w_{n}" columns.

    Parameters
    ----------
    high_lakes_df : :class:`pandas.DataFrame`
        The dataframe

    low_lakes_df : :class:`pandas.DataFrame`
        The dataframe

    Returns
    -------
    A :class:`pandas.Series` of :class:`int`, indexed by "w".
    """
    week_numbers = sorted(
        get_week_numbers(
            high_lakes_df,
            low_lakes_df
        )
    )

    return pd.Series(
        week_numbers,
        index = pd.Index(week_numbers, name = "w")
    )


def get_t_ser(
    ttest_results_ser: pd.Series
) -> pd.Series:
    """
    Returns each week's t-statistic in `ttest_results_ser`.

    Parameters
    ----------
    ttest_results_ser : :class:`pandas.Series`
        The series, as returned by `get_ttest_results_ser`

    Returns
    -------
    A :class:`pandas.Series` indexed by "w". A week whose result is
    `None` maps to `numpy.nan`.
    """
    return ttest_results_ser.apply(lambda result: result.statistic if result is not None else np.nan)


def get_p_ser(
    ttest_results_ser: pd.Series
) -> pd.Series:
    """
    Returns each week's p-value in `ttest_results_ser`.

    Parameters
    ----------
    ttest_results_ser : :class:`pandas.Series`
        The series, as returned by `get_ttest_results_ser`

    Returns
    -------
    A :class:`pandas.Series` indexed by "w". A week whose result is
    `None` maps to `numpy.nan`.
    """
    return ttest_results_ser.apply(lambda result: result.pvalue if result is not None else np.nan)


def get_dof_ser(
    ttest_results_ser: pd.Series
) -> pd.Series:
    """
    Returns each week's degrees of freedom in `ttest_results_ser`.

    Parameters
    ----------
    ttest_results_ser : :class:`pandas.Series`
        The series, as returned by `get_ttest_results_ser`

    Returns
    -------
    A :class:`pandas.Series` indexed by "w". A week whose result is
    `None` maps to `numpy.nan`.
    """
    return ttest_results_ser.apply(lambda result: result.df if result is not None else np.nan)


def get_mean_ser(
    lakes_df: pd.DataFrame
) -> pd.Series:
    """
    Returns `lakes_df`'s week columns' means, indexed by week number.

    Parameters
    ----------
    lakes_df : :class:`pandas.DataFrame`
        The dataframe

    Returns
    -------
    A :class:`pandas.Series` indexed by "w".
    """
    prefix = "w_"

    means = {
        int(column[len(prefix):]): lakes_df[column].mean()
        for column
        in lakes_df.columns
        if column.startswith(prefix)
    }

    return pd.Series(means).rename_axis("w")


def get_mean_delta_ser(
    mean_high_ser: pd.Series,
    mean_low_ser:  pd.Series
) -> pd.Series:
    """
    Returns `mean_high_ser` minus `mean_low_ser`.

    Parameters
    ----------
    mean_high_ser : :class:`pandas.Series`
        The series, as returned by `get_mean_ser`

    mean_low_ser : :class:`pandas.Series`
        The series, as returned by `get_mean_ser`

    Returns
    -------
    A :class:`pandas.Series` indexed by "w".
    """
    return (mean_high_ser - mean_low_ser).rename_axis("w")


def get_longest_significant_cluster(
    w_ser: pd.Series,
    p_ser: pd.Series
) -> list[int]:
    """
    Returns the weeks in `w_ser`'s longest cluster of consecutive weeks
    whose `p_ser` value is less than `ALPHA`.

    Parameters
    ----------
    w_ser : :class:`pandas.Series`
        The series, as returned by `get_w_ser`

    p_ser : :class:`pandas.Series`
        The series, as returned by `get_p_ser`

    Returns
    -------
    A sorted list of :class:`int`.
    """
    significant_weeks = sorted(w_ser[p_ser < ALPHA])

    if not significant_weeks:
        return []

    longest_significant_cluster = [significant_weeks[0]]
    current_significant_cluster = [significant_weeks[0]]

    for week in significant_weeks[1:]:
        if week == current_significant_cluster[-1] + 1:
            current_significant_cluster.append(week)
        else:
            current_significant_cluster = [week]

        if len(current_significant_cluster) > len(longest_significant_cluster):
            longest_significant_cluster = current_significant_cluster

    return longest_significant_cluster


def get_significant_mean_delta_min(
    mean_delta_ser:              pd.Series,
    longest_significant_cluster: list[int]
) -> float:
    """
    Returns `mean_delta_ser`'s minimum value over
    `longest_significant_cluster`.

    Parameters
    ----------
    mean_delta_ser : :class:`pandas.Series`
        The series, as returned by `get_mean_delta_ser`

    longest_significant_cluster : list[:class:`int`]
        The weeks, as returned by `get_longest_significant_cluster`

    Returns
    -------
    A :class:`float`. `numpy.nan` if `longest_significant_cluster` is
    empty.
    """
    if not longest_significant_cluster:
        return np.nan

    return mean_delta_ser.loc[longest_significant_cluster].min()


def get_significant_mean_delta_max(
    mean_delta_ser:              pd.Series,
    longest_significant_cluster: list[int]
) -> float:
    """
    Returns `mean_delta_ser`'s maximum value over
    `longest_significant_cluster`.

    Parameters
    ----------
    mean_delta_ser : :class:`pandas.Series`
        The series, as returned by `get_mean_delta_ser`

    longest_significant_cluster : list[:class:`int`]
        The weeks, as returned by `get_longest_significant_cluster`

    Returns
    -------
    A :class:`float`. `numpy.nan` if `longest_significant_cluster` is
    empty.
    """
    if not longest_significant_cluster:
        return np.nan

    return mean_delta_ser.loc[longest_significant_cluster].max()


def get_results_df(
    w_ser:          pd.Series,
    t_ser:          pd.Series,
    p_ser:          pd.Series,
    dof_ser:        pd.Series,
    mean_high_ser:  pd.Series,
    mean_low_ser:   pd.Series,
    mean_delta_ser: pd.Series
) -> pd.DataFrame:
    """
    Returns `w_ser`, `t_ser`, `p_ser`, `dof_ser`, `mean_high_ser`,
    `mean_low_ser`, and `mean_delta_ser` combined into one dataframe.

    Parameters
    ----------
    w_ser : :class:`pandas.Series`
        The series, as returned by `get_w_ser`

    t_ser : :class:`pandas.Series`
        The series, as returned by `get_t_ser`

    p_ser : :class:`pandas.Series`
        The series, as returned by `get_p_ser`

    dof_ser : :class:`pandas.Series`
        The series, as returned by `get_dof_ser`

    mean_high_ser : :class:`pandas.Series`
        The series, as returned by `get_mean_ser`

    mean_low_ser : :class:`pandas.Series`
        The series, as returned by `get_mean_ser`

    mean_delta_ser : :class:`pandas.Series`
        The series, as returned by `get_mean_delta_ser`

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "w", with columns "t", "p",
    "dof", "mean_high", "mean_low", and "mean_delta".
    """
    return pd.DataFrame(
        {
            "t":          t_ser,
            "p":          p_ser,
            "dof":        dof_ser,
            "mean_high":  mean_high_ser,
            "mean_low":   mean_low_ser,
            "mean_delta": mean_delta_ser
        },
        index = w_ser.index
    )


def get_summary_df(
    longest_significant_cluster: list[int],
    significant_mean_delta_min:  float,
    significant_mean_delta_max:  float
) -> pd.DataFrame:
    """
    Returns a single-row summary of `longest_significant_cluster` and
    its mean delta bounds.

    Parameters
    ----------
    longest_significant_cluster : list[:class:`int`]
        The weeks, as returned by `get_longest_significant_cluster`

    significant_mean_delta_min : :class:`float`
        The minimum, as returned by `get_significant_mean_delta_min`

    significant_mean_delta_max : :class:`float`
        The maximum, as returned by `get_significant_mean_delta_max`

    Returns
    -------
    A single-row :class:`pandas.DataFrame` with columns
    "longest_cluster_weeks", "longest_cluster_min_delta", and
    "longest_cluster_max_delta".
    """
    return pd.DataFrame(
        [
            {
                "longest_cluster_weeks":     longest_significant_cluster,
                "longest_cluster_min_delta": significant_mean_delta_min,
                "longest_cluster_max_delta": significant_mean_delta_max
            }
        ]
    )


# ==================================================================================================


# Write functions
# ==================================================================================================
def write_results_df_to_csv(
    results_df: pd.DataFrame,
    output:     Path
) -> None:
    """
    Writes `results_df` to `output`.

    Parameters
    ----------
    results_df : :class:`pandas.DataFrame`
        The dataframe

    output : :class:`pathlib.Path`
        The output directory path

    Returns
    -------
    None
    """
    output.mkdir(
        parents  = True,
        exist_ok = True
    )

    results_df.to_csv(output / "results.csv")


def write_summary_df_to_csv(
    summary_df: pd.DataFrame,
    output:     Path
) -> None:
    """
    Writes `summary_df` to `output`.

    Parameters
    ----------
    summary_df : :class:`pandas.DataFrame`
        The dataframe

    output : :class:`pathlib.Path`
        The output directory path

    Returns
    -------
    None
    """
    output.mkdir(
        parents  = True,
        exist_ok = True
    )

    summary_df.to_csv(output / "summary.csv")


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    high_lakes_df = read_lakes_csv(args.high_lakes_csv_path)
    low_lakes_df  = read_lakes_csv(args.low_lakes_csv_path)

    ttest_results_ser = get_ttest_results_ser(
        high_lakes_df,
        low_lakes_df
    )

    w_ser          = get_w_ser(
        high_lakes_df,
        low_lakes_df
    )
    t_ser          = get_t_ser(ttest_results_ser)
    p_ser          = get_p_ser(ttest_results_ser)
    dof_ser        = get_dof_ser(ttest_results_ser)
    mean_high_ser  = get_mean_ser(high_lakes_df)
    mean_low_ser   = get_mean_ser(low_lakes_df)
    mean_delta_ser = get_mean_delta_ser(
        mean_high_ser,
        mean_low_ser
    )

    longest_significant_cluster = get_longest_significant_cluster(
        w_ser,
        p_ser
    )
    significant_mean_delta_min  = get_significant_mean_delta_min(
        mean_delta_ser,
        longest_significant_cluster
    )
    significant_mean_delta_max  = get_significant_mean_delta_max(
        mean_delta_ser,
        longest_significant_cluster
    )

    results_df = get_results_df(
        w_ser,
        t_ser,
        p_ser,
        dof_ser,
        mean_high_ser,
        mean_low_ser,
        mean_delta_ser
    )
    summary_df = get_summary_df(
        longest_significant_cluster,
        significant_mean_delta_min,
        significant_mean_delta_max
    )

    write_results_df_to_csv(
        results_df,
        args.output
    )

    write_summary_df_to_csv(
        summary_df,
        args.output
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
