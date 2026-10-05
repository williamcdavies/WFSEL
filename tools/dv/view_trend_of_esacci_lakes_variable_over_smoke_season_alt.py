r"""
view_trend_of_esacci_lakes_variable_over_smoke_season_alt.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import ast
import sys

from pathlib import Path

# Related Third-party Imports
import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.proc import (
    add_argument_esacci_lakes_variable,
    add_argument_hylak_field,
    argument_esacci_lakes_variable_is_in_esacci_lakes_variables,
    argument_hylak_field_is_in_hylak_fields
)
from lib.esacci_lakes.vars       import (
    ESACCI_LAKES_VARIABLES,
    HYLAK_FIELDS
)
from lib.plot.utils              import (
    force_ax_xtick_visibility,
    save_figure
)
from lib.proc.utils              import (
    add_argument_output,
    argument_output_is_a_file
)
from lib.proc.vars               import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)

PROG  = "view_trend_of_esacci_lakes_variable_over_smoke_season_alt.py"
FORMS = [
    "Absolute",
    "Anomaly"
]


# Argument functions
# ==================================================================================================
def add_argument_above_high_lakes_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `above_high_lakes_csv_path` argument to a
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
    Argument `above_high_lakes_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "above_high_lakes_csv_path",
        type = Path,
        help = """path to some above-threshold high-smoke-season lakes csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_alt.py"""
    )


def add_argument_above_low_lakes_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `above_low_lakes_csv_path` argument to a
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
    Argument `above_low_lakes_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "above_low_lakes_csv_path",
        type = Path,
        help = """path to some above-threshold low-smoke-season lakes csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_alt.py"""
    )


def add_argument_below_high_lakes_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `below_high_lakes_csv_path` argument to a
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
    Argument `below_high_lakes_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "below_high_lakes_csv_path",
        type = Path,
        help = """path to some below-threshold high-smoke-season lakes csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_alt.py"""
    )


def add_argument_below_low_lakes_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `below_low_lakes_csv_path` argument to a
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
    Argument `below_low_lakes_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "below_low_lakes_csv_path",
        type = Path,
        help = """path to some below-threshold low-smoke-season lakes csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_alt.py"""
    )


def add_argument_above_results_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `above_results_csv_path` argument to a
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
    Argument `above_results_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "above_results_csv_path",
        type = Path,
        help = """path to some above-threshold results csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py"""
    )


def add_argument_below_results_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `below_results_csv_path` argument to a
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
    Argument `below_results_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "below_results_csv_path",
        type = Path,
        help = """path to some below-threshold results csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py"""
    )


def add_argument_above_summary_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `above_summary_csv_path` argument to a
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
    Argument `above_summary_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "above_summary_csv_path",
        type = Path,
        help = """path to some above-threshold summary csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py"""
    )


def add_argument_below_summary_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `below_summary_csv_path` argument to a
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
    Argument `below_summary_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "below_summary_csv_path",
        type = Path,
        help = """path to some below-threshold summary csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py"""
    )


def add_argument_threshold(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `threshold` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `threshold` is of type :class:`float`.
    """
    parser.add_argument(
        "threshold",
        type = float,
        help = """the value `hylak_field` was split on"""
    )


def add_argument_form(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `form` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `form` is of type :class:`str`.
    """
    parser.add_argument(
        "-f", "--form",
        default = "Absolute",
        type    = str,
        choices = FORMS,
        help    = """the form of the input data. default=Absolute"""
    )


def argument_above_high_lakes_csv_path_exists(
    above_high_lakes_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `above_high_lakes_csv_path`.

    Parameters
    ----------
    above_high_lakes_csv_path : :class:`pathlib.Path`
        The argument `above_high_lakes_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `above_high_lakes_csv_path` exists. `False` otherwise.
    """
    if above_high_lakes_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument above_high_lakes_csv_path: no such file or directory: {above_high_lakes_csv_path}""")

    return False


def argument_above_low_lakes_csv_path_exists(
    above_low_lakes_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `above_low_lakes_csv_path`.

    Parameters
    ----------
    above_low_lakes_csv_path : :class:`pathlib.Path`
        The argument `above_low_lakes_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `above_low_lakes_csv_path` exists. `False` otherwise.
    """
    if above_low_lakes_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument above_low_lakes_csv_path: no such file or directory: {above_low_lakes_csv_path}""")

    return False


def argument_below_high_lakes_csv_path_exists(
    below_high_lakes_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `below_high_lakes_csv_path`.

    Parameters
    ----------
    below_high_lakes_csv_path : :class:`pathlib.Path`
        The argument `below_high_lakes_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `below_high_lakes_csv_path` exists. `False` otherwise.
    """
    if below_high_lakes_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument below_high_lakes_csv_path: no such file or directory: {below_high_lakes_csv_path}""")

    return False


def argument_below_low_lakes_csv_path_exists(
    below_low_lakes_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `below_low_lakes_csv_path`.

    Parameters
    ----------
    below_low_lakes_csv_path : :class:`pathlib.Path`
        The argument `below_low_lakes_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `below_low_lakes_csv_path` exists. `False` otherwise.
    """
    if below_low_lakes_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument below_low_lakes_csv_path: no such file or directory: {below_low_lakes_csv_path}""")

    return False


def argument_above_results_csv_path_exists(
    above_results_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `above_results_csv_path`.

    Parameters
    ----------
    above_results_csv_path : :class:`pathlib.Path`
        The argument `above_results_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `above_results_csv_path` exists. `False` otherwise.
    """
    if above_results_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument above_results_csv_path: no such file or directory: {above_results_csv_path}""")

    return False


def argument_below_results_csv_path_exists(
    below_results_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `below_results_csv_path`.

    Parameters
    ----------
    below_results_csv_path : :class:`pathlib.Path`
        The argument `below_results_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `below_results_csv_path` exists. `False` otherwise.
    """
    if below_results_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument below_results_csv_path: no such file or directory: {below_results_csv_path}""")

    return False


def argument_above_summary_csv_path_exists(
    above_summary_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `above_summary_csv_path`.

    Parameters
    ----------
    above_summary_csv_path : :class:`pathlib.Path`
        The argument `above_summary_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `above_summary_csv_path` exists. `False` otherwise.
    """
    if above_summary_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument above_summary_csv_path: no such file or directory: {above_summary_csv_path}""")

    return False


def argument_below_summary_csv_path_exists(
    below_summary_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `below_summary_csv_path`.

    Parameters
    ----------
    below_summary_csv_path : :class:`pathlib.Path`
        The argument `below_summary_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `below_summary_csv_path` exists. `False` otherwise.
    """
    if below_summary_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument below_summary_csv_path: no such file or directory: {below_summary_csv_path}""")

    return False


def argument_form_is_in_forms(
    form: str,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `form`.

    Parameters
    ----------
    form : :class:`str`
        The argument `form`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `form` is in `FORMS`. `False` otherwise.
    """
    if form in FORMS:
        return True

    if loud:
        print(f"""error: argument form: not in {FORMS}: {form}""")

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
        description = """Produces a trend visualisation of an ESA CCI Lakes variable over the smoke season, split by a HydroLAKES field's value against an explicit threshold, from precomputed lakes, results, and summary csv files."""
    )

    # Positional arguments
    add_argument_esacci_lakes_variable(parser)
    add_argument_hylak_field(parser)
    add_argument_above_high_lakes_csv_path(parser)
    add_argument_above_low_lakes_csv_path(parser)
    add_argument_below_high_lakes_csv_path(parser)
    add_argument_below_low_lakes_csv_path(parser)
    add_argument_above_results_csv_path(parser)
    add_argument_below_results_csv_path(parser)
    add_argument_above_summary_csv_path(parser)
    add_argument_below_summary_csv_path(parser)
    add_argument_threshold(parser)

    # Optional arguments
    add_argument_form(parser)
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

    if not argument_hylak_field_is_in_hylak_fields(
        args.hylak_field,
        loud = True
    ):
        return False

    if not argument_above_high_lakes_csv_path_exists(
        args.above_high_lakes_csv_path,
        loud = True
    ):
        return False

    if not argument_above_low_lakes_csv_path_exists(
        args.above_low_lakes_csv_path,
        loud = True
    ):
        return False

    if not argument_below_high_lakes_csv_path_exists(
        args.below_high_lakes_csv_path,
        loud = True
    ):
        return False

    if not argument_below_low_lakes_csv_path_exists(
        args.below_low_lakes_csv_path,
        loud = True
    ):
        return False

    if not argument_above_results_csv_path_exists(
        args.above_results_csv_path,
        loud = True
    ):
        return False

    if not argument_below_results_csv_path_exists(
        args.below_results_csv_path,
        loud = True
    ):
        return False

    if not argument_above_summary_csv_path_exists(
        args.above_summary_csv_path,
        loud = True
    ):
        return False

    if not argument_below_summary_csv_path_exists(
        args.below_summary_csv_path,
        loud = True
    ):
        return False

    if not argument_form_is_in_forms(
        args.form,
        loud = True
    ):
        return False

    if not argument_output_is_a_file(
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
    Reads `lakes_csv_path` into a dataframe.

    Parameters
    ----------
    lakes_csv_path : :class:`pathlib.Path`
        The path to some lakes csv file as produced by
        comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_alt.py

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        lakes_csv_path,
        index_col = "esacci_lakes_id"
    )


def read_results_csv(
    results_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `results_csv_path` into a dataframe.

    Parameters
    ----------
    results_csv_path : :class:`pathlib.Path`
        The path to some results csv file as produced by
        comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "w".
    """
    return pd.read_csv(
        results_csv_path,
        index_col = "w"
    )


def read_summary_csv(
    summary_csv_path: Path
) -> pd.Series:
    """
    Reads `summary_csv_path`'s single row into a series.

    Parameters
    ----------
    summary_csv_path : :class:`pathlib.Path`
        The path to some summary csv file as produced by
        comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py

    Returns
    -------
    A :class:`pandas.Series`.
    """
    return pd.read_csv(summary_csv_path).iloc[0]


# ==================================================================================================


# Data functions
# ==================================================================================================
def get_lakes_df_week_number_ser_pairs(
    lakes_df: pd.DataFrame
) -> list[tuple[int, pd.Series]]:
    """
    Returns `lakes_df`'s week columns as (week number, series) pairs.

    Parameters
    ----------
    lakes_df : :class:`pandas.DataFrame`
        The dataframe

    Returns
    -------
    A list of (week number, series) pairs.
    """
    prefix = "w_"
    pairs  = []

    for label_, ser in lakes_df.filter(like = prefix).items():
        n = int(label_.removeprefix(prefix))

        pairs.append((n, ser))

    return pairs


def get_mean_high_ser(
    results_df: pd.DataFrame
) -> pd.Series:
    """
    Returns `results_df`'s "mean_high" column.

    Parameters
    ----------
    results_df : :class:`pandas.DataFrame`
        The dataframe, as returned by `read_results_csv`

    Returns
    -------
    A :class:`pandas.Series` indexed by "w".
    """
    return results_df["mean_high"]


def get_mean_low_ser(
    results_df: pd.DataFrame
) -> pd.Series:
    """
    Returns `results_df`'s "mean_low" column.

    Parameters
    ----------
    results_df : :class:`pandas.DataFrame`
        The dataframe, as returned by `read_results_csv`

    Returns
    -------
    A :class:`pandas.Series` indexed by "w".
    """
    return results_df["mean_low"]


def get_longest_cluster_weeks(
    summary_ser: pd.Series
) -> list[int]:
    """
    Returns `summary_ser`'s "longest_cluster_weeks" field, parsed from
    its string representation.

    Parameters
    ----------
    summary_ser : :class:`pandas.Series`
        The series, as returned by `read_summary_csv`

    Returns
    -------
    A list of :class:`int`.
    """
    return ast.literal_eval(summary_ser["longest_cluster_weeks"])


# ==================================================================================================


# Plot functions
# ==================================================================================================
def plot_lakes_df_scatterplot(
    ax:       plt.Axes,
    lakes_df: pd.DataFrame,
    *,
    color: str,
    label: str | None = None
) -> None:
    """
    Plots a scatterplot of `lakes_df`'s week columns onto `ax`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    lakes_df : :class:`pandas.DataFrame`
        The dataframe

    color : :class:`str`
        The point color

    label : :class:`str` | `None`
        The legend label

    Returns
    -------
    None
    """
    for n, ser in get_lakes_df_week_number_ser_pairs(lakes_df):
        ax.scatter(
            x          = [n] * len(ser),
            y          = ser,
            label      = label,
            color      = color,
            edgecolors = "none",
            alpha      = 0.1
        )


def plot_lakes_df_lineplot(
    ax:       plt.Axes,
    mean_ser: pd.Series,
    *,
    color: str,
    label: str | None = None
) -> None:
    """
    Plots a line of `mean_ser`'s values onto `ax`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    mean_ser : :class:`pandas.Series`
        A series of means

    color : :class:`str`
        The line color

    label : :class:`str` | `None`
        The legend label

    Returns
    -------
    None
    """
    ax.plot(
        mean_ser.index,
        mean_ser,
        label  = label,
        color  = color,
        marker = "o"
    )


def plot_significant_cluster_span(
    ax: plt.Axes,
    *,
    longest_cluster_weeks: list[int]
) -> None:
    """
    Shades `ax`'s background over `longest_cluster_weeks`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    longest_cluster_weeks : list[:class:`int`]
        The weeks, as returned by `get_longest_cluster_weeks`

    Returns
    -------
    None
    """
    if not longest_cluster_weeks:
        return

    ax.axvspan(
        min(longest_cluster_weeks) - 0.5,
        max(longest_cluster_weeks) + 0.5,
        color  = "#CCCCCC",
        alpha  = 0.25
    )


def plot_on_above_threshold_lakes_ax(
    above_threshold_lakes_ax: plt.Axes,
    *,
    above_high_lakes_df:         pd.DataFrame,
    above_low_lakes_df:          pd.DataFrame,
    above_high_mean_ser:         pd.Series,
    above_low_mean_ser:          pd.Series,
    above_longest_cluster_weeks: list[int]
) -> None:
    """
    Plots `above_high_lakes_df`, `above_low_lakes_df`,
    `above_high_mean_ser`, `above_low_mean_ser`, and
    `above_longest_cluster_weeks` onto `above_threshold_lakes_ax`.

    Parameters
    ----------
    above_threshold_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    above_high_lakes_df : :class:`pandas.DataFrame`
        Above-threshold lakes during a high smoke season

    above_low_lakes_df : :class:`pandas.DataFrame`
        Above-threshold lakes during a low smoke season

    above_high_mean_ser : :class:`pandas.Series`
        `above_high_lakes_df`'s weekly means, as returned by
        `get_mean_high_ser`

    above_low_mean_ser : :class:`pandas.Series`
        `above_low_lakes_df`'s weekly means, as returned by
        `get_mean_low_ser`

    above_longest_cluster_weeks : list[:class:`int`]
        The weeks, as returned by `get_longest_cluster_weeks`

    Returns
    -------
    None
    """
    plot_significant_cluster_span(
        above_threshold_lakes_ax,
        longest_cluster_weeks = above_longest_cluster_weeks
    )

    plot_lakes_df_scatterplot(
        above_threshold_lakes_ax,
        above_high_lakes_df,
        color = "#FF0000"
    )
    plot_lakes_df_lineplot(
        above_threshold_lakes_ax,
        above_high_mean_ser,
        color = "#FF0000",
        label = "High Smoke Season (Mean)"
    )

    plot_lakes_df_scatterplot(
        above_threshold_lakes_ax,
        above_low_lakes_df,
        color = "#0000FF"
    )
    plot_lakes_df_lineplot(
        above_threshold_lakes_ax,
        above_low_mean_ser,
        color = "#0000FF",
        label = "Low Smoke Season (Mean)"
    )


def plot_on_below_threshold_lakes_ax(
    below_threshold_lakes_ax: plt.Axes,
    *,
    below_high_lakes_df:         pd.DataFrame,
    below_low_lakes_df:          pd.DataFrame,
    below_high_mean_ser:         pd.Series,
    below_low_mean_ser:          pd.Series,
    below_longest_cluster_weeks: list[int]
) -> None:
    """
    Plots `below_high_lakes_df`, `below_low_lakes_df`,
    `below_high_mean_ser`, `below_low_mean_ser`, and
    `below_longest_cluster_weeks` onto `below_threshold_lakes_ax`.

    Parameters
    ----------
    below_threshold_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    below_high_lakes_df : :class:`pandas.DataFrame`
        Below-threshold lakes during a high smoke season

    below_low_lakes_df : :class:`pandas.DataFrame`
        Below-threshold lakes during a low smoke season

    below_high_mean_ser : :class:`pandas.Series`
        `below_high_lakes_df`'s weekly means, as returned by
        `get_mean_high_ser`

    below_low_mean_ser : :class:`pandas.Series`
        `below_low_lakes_df`'s weekly means, as returned by
        `get_mean_low_ser`

    below_longest_cluster_weeks : list[:class:`int`]
        The weeks, as returned by `get_longest_cluster_weeks`

    Returns
    -------
    None
    """
    plot_significant_cluster_span(
        below_threshold_lakes_ax,
        longest_cluster_weeks = below_longest_cluster_weeks
    )

    plot_lakes_df_scatterplot(
        below_threshold_lakes_ax,
        below_high_lakes_df,
        color = "#FF0000"
    )
    plot_lakes_df_lineplot(
        below_threshold_lakes_ax,
        below_high_mean_ser,
        color = "#FF0000",
        label = "High Smoke Season (Mean)"
    )

    plot_lakes_df_scatterplot(
        below_threshold_lakes_ax,
        below_low_lakes_df,
        color = "#0000FF"
    )
    plot_lakes_df_lineplot(
        below_threshold_lakes_ax,
        below_low_mean_ser,
        color = "#0000FF",
        label = "Low Smoke Season (Mean)"
    )


def set_above_threshold_lakes_ax_properties(
    above_threshold_lakes_ax: plt.Axes,
    *,
    esacci_lakes_variable: str,
    hylak_field:           str,
    threshold:             float,
    form:                  str
) -> None:
    """
    Sets `above_threshold_lakes_ax`'s properties.

    Parameters
    ----------
    above_threshold_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to set properties on

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    hylak_field : :class:`str`
        The HydroLAKES field id

    threshold : :class:`float`
        The value `hylak_field` was split on

    form : :class:`str`
        The form of the input data. One of `FORMS`

    Returns
    -------
    None
    """
    esacci_lakes_variable_long_name = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].long_name
    esacci_lakes_variable_units     = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].units
    hylak_field_long_name           = HYLAK_FIELDS[hylak_field].long_name
    hylak_field_display_units       = HYLAK_FIELDS[hylak_field].display_units or HYLAK_FIELDS[hylak_field].units
    hylak_field_display_scale       = HYLAK_FIELDS[hylak_field].display_scale or HYLAK_FIELDS[hylak_field].scale
    threshold_display               = threshold / hylak_field_display_scale
    form_qualifier                  = "" if form == "Absolute" else f" {form}"

    above_threshold_lakes_ax.set_title(
        f"""Weekly {esacci_lakes_variable_long_name}{form_qualifier} for lakes with {hylak_field_long_name} > {threshold_display:g} {hylak_field_display_units}""",
        fontsize = 10
    )
    above_threshold_lakes_ax.set_xlabel(
        "Week relative to start of smoke season",
        fontsize = 10
    )
    above_threshold_lakes_ax.set_ylabel(
        f"""{esacci_lakes_variable_long_name} ({esacci_lakes_variable_units}){form_qualifier}""",
        fontsize = 10
    )
    above_threshold_lakes_ax.set_xticks(np.arange(-3, 21).tolist())

    force_ax_xtick_visibility(above_threshold_lakes_ax)


def set_below_threshold_lakes_ax_properties(
    below_threshold_lakes_ax: plt.Axes,
    *,
    esacci_lakes_variable: str,
    hylak_field:           str,
    threshold:             float,
    form:                  str
) -> None:
    """
    Sets `below_threshold_lakes_ax`'s properties.

    Parameters
    ----------
    below_threshold_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to set properties on

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    hylak_field : :class:`str`
        The HydroLAKES field id

    threshold : :class:`float`
        The value `hylak_field` was split on

    form : :class:`str`
        The form of the input data. One of `FORMS`

    Returns
    -------
    None
    """
    esacci_lakes_variable_long_name = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].long_name
    esacci_lakes_variable_units     = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].units
    hylak_field_long_name           = HYLAK_FIELDS[hylak_field].long_name
    hylak_field_display_units       = HYLAK_FIELDS[hylak_field].display_units or HYLAK_FIELDS[hylak_field].units
    hylak_field_display_scale       = HYLAK_FIELDS[hylak_field].display_scale or HYLAK_FIELDS[hylak_field].scale
    threshold_display               = threshold / hylak_field_display_scale
    form_qualifier                  = "" if form == "Absolute" else f" {form}"

    below_threshold_lakes_ax.set_title(
        f"""Weekly {esacci_lakes_variable_long_name}{form_qualifier} for lakes with {hylak_field_long_name} <= {threshold_display:g} {hylak_field_display_units}""",
        fontsize = 10
    )
    below_threshold_lakes_ax.set_xlabel(
        "Week relative to start of smoke season",
        fontsize = 10
    )
    below_threshold_lakes_ax.set_ylabel(
        f"""{esacci_lakes_variable_long_name} ({esacci_lakes_variable_units}){form_qualifier}""",
        fontsize = 10
    )
    below_threshold_lakes_ax.set_xticks(np.arange(-3, 21).tolist())

    force_ax_xtick_visibility(below_threshold_lakes_ax)


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    above_high_lakes_df = read_lakes_csv(args.above_high_lakes_csv_path)
    above_low_lakes_df  = read_lakes_csv(args.above_low_lakes_csv_path)
    below_high_lakes_df = read_lakes_csv(args.below_high_lakes_csv_path)
    below_low_lakes_df  = read_lakes_csv(args.below_low_lakes_csv_path)

    above_results_df = read_results_csv(args.above_results_csv_path)
    below_results_df = read_results_csv(args.below_results_csv_path)

    above_summary_ser = read_summary_csv(args.above_summary_csv_path)
    below_summary_ser = read_summary_csv(args.below_summary_csv_path)

    above_high_mean_ser = get_mean_high_ser(above_results_df)
    above_low_mean_ser  = get_mean_low_ser(above_results_df)
    below_high_mean_ser = get_mean_high_ser(below_results_df)
    below_low_mean_ser  = get_mean_low_ser(below_results_df)

    above_longest_cluster_weeks = get_longest_cluster_weeks(above_summary_ser)
    below_longest_cluster_weeks = get_longest_cluster_weeks(below_summary_ser)

    fig, (
        above_threshold_lakes_ax,
        below_threshold_lakes_ax
    ) = plt.subplots(
        nrows   = 2,
        ncols   = 1,
        sharex  = True,
        sharey  = True,
        figsize = (10, 10)
    )
    plt.subplots_adjust(hspace = 0.25)

    plot_on_above_threshold_lakes_ax(
        above_threshold_lakes_ax,
        above_high_lakes_df         = above_high_lakes_df,
        above_low_lakes_df          = above_low_lakes_df,
        above_high_mean_ser         = above_high_mean_ser,
        above_low_mean_ser          = above_low_mean_ser,
        above_longest_cluster_weeks = above_longest_cluster_weeks
    )
    plot_on_below_threshold_lakes_ax(
        below_threshold_lakes_ax,
        below_high_lakes_df         = below_high_lakes_df,
        below_low_lakes_df          = below_low_lakes_df,
        below_high_mean_ser         = below_high_mean_ser,
        below_low_mean_ser          = below_low_mean_ser,
        below_longest_cluster_weeks = below_longest_cluster_weeks
    )

    set_above_threshold_lakes_ax_properties(
        above_threshold_lakes_ax,
        esacci_lakes_variable = args.esacci_lakes_variable,
        hylak_field           = args.hylak_field,
        threshold             = args.threshold,
        form                  = args.form
    )
    set_below_threshold_lakes_ax_properties(
        below_threshold_lakes_ax,
        esacci_lakes_variable = args.esacci_lakes_variable,
        hylak_field           = args.hylak_field,
        threshold             = args.threshold,
        form                  = args.form
    )

    above_threshold_lakes_ax.legend(loc = "upper left")
    below_threshold_lakes_ax.legend(loc = "upper left")

    save_figure(
        fig,
        args.output
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
