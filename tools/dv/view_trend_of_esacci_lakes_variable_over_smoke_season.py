r"""
view_trend_of_esacci_lakes_variable_over_smoke_season.py

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

PROG  = "view_trend_of_esacci_lakes_variable_over_smoke_season.py"
FORMS = [
    "Absolute",
    "Anomaly"
]


# Argument functions
# ==================================================================================================
def add_argument_upper_high_lakes_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `upper_high_lakes_csv_path` argument to a
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
    Argument `upper_high_lakes_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "upper_high_lakes_csv_path",
        type = Path,
        help = """path to some upper-bounds high-smoke-season lakes csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py"""
    )


def add_argument_upper_low_lakes_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `upper_low_lakes_csv_path` argument to a
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
    Argument `upper_low_lakes_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "upper_low_lakes_csv_path",
        type = Path,
        help = """path to some upper-bounds low-smoke-season lakes csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py"""
    )


def add_argument_middle_high_lakes_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `middle_high_lakes_csv_path` argument to a
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
    Argument `middle_high_lakes_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "middle_high_lakes_csv_path",
        type = Path,
        help = """path to some middle-bounds high-smoke-season lakes csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py"""
    )


def add_argument_middle_low_lakes_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `middle_low_lakes_csv_path` argument to a
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
    Argument `middle_low_lakes_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "middle_low_lakes_csv_path",
        type = Path,
        help = """path to some middle-bounds low-smoke-season lakes csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py"""
    )


def add_argument_lower_high_lakes_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `lower_high_lakes_csv_path` argument to a
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
    Argument `lower_high_lakes_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "lower_high_lakes_csv_path",
        type = Path,
        help = """path to some lower-bounds high-smoke-season lakes csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py"""
    )


def add_argument_lower_low_lakes_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `lower_low_lakes_csv_path` argument to a
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
    Argument `lower_low_lakes_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "lower_low_lakes_csv_path",
        type = Path,
        help = """path to some lower-bounds low-smoke-season lakes csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py"""
    )


def add_argument_upper_results_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `upper_results_csv_path` argument to a
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
    Argument `upper_results_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "upper_results_csv_path",
        type = Path,
        help = """path to some upper-bounds results csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py"""
    )


def add_argument_middle_results_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `middle_results_csv_path` argument to a
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
    Argument `middle_results_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "middle_results_csv_path",
        type = Path,
        help = """path to some middle-bounds results csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py"""
    )


def add_argument_lower_results_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `lower_results_csv_path` argument to a
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
    Argument `lower_results_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "lower_results_csv_path",
        type = Path,
        help = """path to some lower-bounds results csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py"""
    )


def add_argument_upper_summary_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `upper_summary_csv_path` argument to a
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
    Argument `upper_summary_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "upper_summary_csv_path",
        type = Path,
        help = """path to some upper-bounds summary csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py"""
    )


def add_argument_middle_summary_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `middle_summary_csv_path` argument to a
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
    Argument `middle_summary_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "middle_summary_csv_path",
        type = Path,
        help = """path to some middle-bounds summary csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py"""
    )


def add_argument_lower_summary_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `lower_summary_csv_path` argument to a
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
    Argument `lower_summary_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "lower_summary_csv_path",
        type = Path,
        help = """path to some lower-bounds summary csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py"""
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
    Argument `form` is of type :class:`str`. default=Absolute.
    """
    parser.add_argument(
        "-f", "--form",
        default = "Absolute",
        type    = str,
        choices = FORMS,
        help    = """the form of the input data. default=Absolute"""
    )


def argument_upper_high_lakes_csv_path_exists(
    upper_high_lakes_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `upper_high_lakes_csv_path`.

    Parameters
    ----------
    upper_high_lakes_csv_path : :class:`pathlib.Path`
        The argument `upper_high_lakes_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `upper_high_lakes_csv_path` exists. `False` otherwise.
    """
    if upper_high_lakes_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument upper_high_lakes_csv_path: no such file or directory: {upper_high_lakes_csv_path}""")

    return False


def argument_upper_low_lakes_csv_path_exists(
    upper_low_lakes_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `upper_low_lakes_csv_path`.

    Parameters
    ----------
    upper_low_lakes_csv_path : :class:`pathlib.Path`
        The argument `upper_low_lakes_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `upper_low_lakes_csv_path` exists. `False` otherwise.
    """
    if upper_low_lakes_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument upper_low_lakes_csv_path: no such file or directory: {upper_low_lakes_csv_path}""")

    return False


def argument_middle_high_lakes_csv_path_exists(
    middle_high_lakes_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `middle_high_lakes_csv_path`.

    Parameters
    ----------
    middle_high_lakes_csv_path : :class:`pathlib.Path`
        The argument `middle_high_lakes_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `middle_high_lakes_csv_path` exists. `False` otherwise.
    """
    if middle_high_lakes_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument middle_high_lakes_csv_path: no such file or directory: {middle_high_lakes_csv_path}""")

    return False


def argument_middle_low_lakes_csv_path_exists(
    middle_low_lakes_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `middle_low_lakes_csv_path`.

    Parameters
    ----------
    middle_low_lakes_csv_path : :class:`pathlib.Path`
        The argument `middle_low_lakes_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `middle_low_lakes_csv_path` exists. `False` otherwise.
    """
    if middle_low_lakes_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument middle_low_lakes_csv_path: no such file or directory: {middle_low_lakes_csv_path}""")

    return False


def argument_lower_high_lakes_csv_path_exists(
    lower_high_lakes_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `lower_high_lakes_csv_path`.

    Parameters
    ----------
    lower_high_lakes_csv_path : :class:`pathlib.Path`
        The argument `lower_high_lakes_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `lower_high_lakes_csv_path` exists. `False` otherwise.
    """
    if lower_high_lakes_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument lower_high_lakes_csv_path: no such file or directory: {lower_high_lakes_csv_path}""")

    return False


def argument_lower_low_lakes_csv_path_exists(
    lower_low_lakes_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `lower_low_lakes_csv_path`.

    Parameters
    ----------
    lower_low_lakes_csv_path : :class:`pathlib.Path`
        The argument `lower_low_lakes_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `lower_low_lakes_csv_path` exists. `False` otherwise.
    """
    if lower_low_lakes_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument lower_low_lakes_csv_path: no such file or directory: {lower_low_lakes_csv_path}""")

    return False


def argument_upper_results_csv_path_exists(
    upper_results_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `upper_results_csv_path`.

    Parameters
    ----------
    upper_results_csv_path : :class:`pathlib.Path`
        The argument `upper_results_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `upper_results_csv_path` exists. `False` otherwise.
    """
    if upper_results_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument upper_results_csv_path: no such file or directory: {upper_results_csv_path}""")

    return False


def argument_middle_results_csv_path_exists(
    middle_results_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `middle_results_csv_path`.

    Parameters
    ----------
    middle_results_csv_path : :class:`pathlib.Path`
        The argument `middle_results_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `middle_results_csv_path` exists. `False` otherwise.
    """
    if middle_results_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument middle_results_csv_path: no such file or directory: {middle_results_csv_path}""")

    return False


def argument_lower_results_csv_path_exists(
    lower_results_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `lower_results_csv_path`.

    Parameters
    ----------
    lower_results_csv_path : :class:`pathlib.Path`
        The argument `lower_results_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `lower_results_csv_path` exists. `False` otherwise.
    """
    if lower_results_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument lower_results_csv_path: no such file or directory: {lower_results_csv_path}""")

    return False


def argument_upper_summary_csv_path_exists(
    upper_summary_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `upper_summary_csv_path`.

    Parameters
    ----------
    upper_summary_csv_path : :class:`pathlib.Path`
        The argument `upper_summary_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `upper_summary_csv_path` exists. `False` otherwise.
    """
    if upper_summary_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument upper_summary_csv_path: no such file or directory: {upper_summary_csv_path}""")

    return False


def argument_middle_summary_csv_path_exists(
    middle_summary_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `middle_summary_csv_path`.

    Parameters
    ----------
    middle_summary_csv_path : :class:`pathlib.Path`
        The argument `middle_summary_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `middle_summary_csv_path` exists. `False` otherwise.
    """
    if middle_summary_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument middle_summary_csv_path: no such file or directory: {middle_summary_csv_path}""")

    return False


def argument_lower_summary_csv_path_exists(
    lower_summary_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `lower_summary_csv_path`.

    Parameters
    ----------
    lower_summary_csv_path : :class:`pathlib.Path`
        The argument `lower_summary_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `lower_summary_csv_path` exists. `False` otherwise.
    """
    if lower_summary_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument lower_summary_csv_path: no such file or directory: {lower_summary_csv_path}""")

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
        description = """Produces a trend visualisation of an ESA CCI Lakes variable over the smoke season, split by a HydroLAKES field's bounds, from precomputed lakes, results, and summary csv files."""
    )

    # Positional arguments
    add_argument_esacci_lakes_variable(parser)
    add_argument_hylak_field(parser)
    add_argument_upper_high_lakes_csv_path(parser)
    add_argument_upper_low_lakes_csv_path(parser)
    add_argument_middle_high_lakes_csv_path(parser)
    add_argument_middle_low_lakes_csv_path(parser)
    add_argument_lower_high_lakes_csv_path(parser)
    add_argument_lower_low_lakes_csv_path(parser)
    add_argument_upper_results_csv_path(parser)
    add_argument_middle_results_csv_path(parser)
    add_argument_lower_results_csv_path(parser)
    add_argument_upper_summary_csv_path(parser)
    add_argument_middle_summary_csv_path(parser)
    add_argument_lower_summary_csv_path(parser)

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

    if not argument_upper_high_lakes_csv_path_exists(
        args.upper_high_lakes_csv_path,
        loud = True
    ):
        return False

    if not argument_upper_low_lakes_csv_path_exists(
        args.upper_low_lakes_csv_path,
        loud = True
    ):
        return False

    if not argument_middle_high_lakes_csv_path_exists(
        args.middle_high_lakes_csv_path,
        loud = True
    ):
        return False

    if not argument_middle_low_lakes_csv_path_exists(
        args.middle_low_lakes_csv_path,
        loud = True
    ):
        return False

    if not argument_lower_high_lakes_csv_path_exists(
        args.lower_high_lakes_csv_path,
        loud = True
    ):
        return False

    if not argument_lower_low_lakes_csv_path_exists(
        args.lower_low_lakes_csv_path,
        loud = True
    ):
        return False

    if not argument_upper_results_csv_path_exists(
        args.upper_results_csv_path,
        loud = True
    ):
        return False

    if not argument_middle_results_csv_path_exists(
        args.middle_results_csv_path,
        loud = True
    ):
        return False

    if not argument_lower_results_csv_path_exists(
        args.lower_results_csv_path,
        loud = True
    ):
        return False

    if not argument_upper_summary_csv_path_exists(
        args.upper_summary_csv_path,
        loud = True
    ):
        return False

    if not argument_middle_summary_csv_path_exists(
        args.middle_summary_csv_path,
        loud = True
    ):
        return False

    if not argument_lower_summary_csv_path_exists(
        args.lower_summary_csv_path,
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
        comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py

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
        n = int(label_.removeprefix(prefix)) # type: ignore

        if (
            n < -3
            or n > 20
        ):
            continue

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
    ax:       plt.Axes, # type: ignore
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
    ax:       plt.Axes, # type: ignore
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
    ax: plt.Axes, # type: ignore
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
        alpha  = 0.3,
        zorder = 0
    )


def plot_on_upper_bounds_lakes_ax(
    upper_bounds_lakes_ax: plt.Axes, # type: ignore
    *,
    upper_high_lakes_df:         pd.DataFrame,
    upper_low_lakes_df:          pd.DataFrame,
    upper_high_mean_ser:         pd.Series,
    upper_low_mean_ser:          pd.Series,
    upper_longest_cluster_weeks: list[int]
) -> None:
    """
    Plots `upper_high_lakes_df`, `upper_low_lakes_df`,
    `upper_high_mean_ser`, `upper_low_mean_ser`, and
    `upper_longest_cluster_weeks` onto `upper_bounds_lakes_ax`.

    Parameters
    ----------
    upper_bounds_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    upper_high_lakes_df : :class:`pandas.DataFrame`
        Upper-bounds-depth lakes during a high smoke season

    upper_low_lakes_df : :class:`pandas.DataFrame`
        Upper-bounds-depth lakes during a low smoke season

    upper_high_mean_ser : :class:`pandas.Series`
        `upper_high_lakes_df`'s weekly means, as returned by
        `get_mean_high_ser`

    upper_low_mean_ser : :class:`pandas.Series`
        `upper_low_lakes_df`'s weekly means, as returned by
        `get_mean_low_ser`

    upper_longest_cluster_weeks : list[:class:`int`]
        The weeks, as returned by `get_longest_cluster_weeks`

    Returns
    -------
    None
    """
    plot_significant_cluster_span(
        upper_bounds_lakes_ax,
        longest_cluster_weeks = upper_longest_cluster_weeks
    )

    plot_lakes_df_scatterplot(
        upper_bounds_lakes_ax,
        upper_high_lakes_df,
        color = "#FF0000"
    )
    plot_lakes_df_lineplot(
        upper_bounds_lakes_ax,
        upper_high_mean_ser,
        color = "#FF0000",
        label = "High Smoke Season (Mean)"
    )

    plot_lakes_df_scatterplot(
        upper_bounds_lakes_ax,
        upper_low_lakes_df,
        color = "#0000FF"
    )
    plot_lakes_df_lineplot(
        upper_bounds_lakes_ax,
        upper_low_mean_ser,
        color = "#0000FF",
        label = "Low Smoke Season (Mean)"
    )


def plot_on_middle_bounds_lakes_ax(
    middle_bounds_lakes_ax: plt.Axes, # type: ignore
    *,
    middle_high_lakes_df:         pd.DataFrame,
    middle_low_lakes_df:          pd.DataFrame,
    middle_high_mean_ser:         pd.Series,
    middle_low_mean_ser:          pd.Series,
    middle_longest_cluster_weeks: list[int]
) -> None:
    """
    Plots `middle_high_lakes_df`, `middle_low_lakes_df`,
    `middle_high_mean_ser`, `middle_low_mean_ser`, and
    `middle_longest_cluster_weeks` onto `middle_bounds_lakes_ax`.

    Parameters
    ----------
    middle_bounds_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    middle_high_lakes_df : :class:`pandas.DataFrame`
        Middle-bounds-depth lakes during a high smoke season

    middle_low_lakes_df : :class:`pandas.DataFrame`
        Middle-bounds-depth lakes during a low smoke season

    middle_high_mean_ser : :class:`pandas.Series`
        `middle_high_lakes_df`'s weekly means, as returned by
        `get_mean_high_ser`

    middle_low_mean_ser : :class:`pandas.Series`
        `middle_low_lakes_df`'s weekly means, as returned by
        `get_mean_low_ser`

    middle_longest_cluster_weeks : list[:class:`int`]
        The weeks, as returned by `get_longest_cluster_weeks`

    Returns
    -------
    None
    """
    plot_significant_cluster_span(
        middle_bounds_lakes_ax,
        longest_cluster_weeks = middle_longest_cluster_weeks
    )

    plot_lakes_df_scatterplot(
        middle_bounds_lakes_ax,
        middle_high_lakes_df,
        color = "#FF0000"
    )
    plot_lakes_df_lineplot(
        middle_bounds_lakes_ax,
        middle_high_mean_ser,
        color = "#FF0000",
        label = "High Smoke Season (Mean)"
    )

    plot_lakes_df_scatterplot(
        middle_bounds_lakes_ax,
        middle_low_lakes_df,
        color = "#0000FF"
    )
    plot_lakes_df_lineplot(
        middle_bounds_lakes_ax,
        middle_low_mean_ser,
        color = "#0000FF",
        label = "Low Smoke Season (Mean)"
    )


def plot_on_lower_bounds_lakes_ax(
    lower_bounds_lakes_ax: plt.Axes, # type: ignore
    *,
    lower_high_lakes_df:         pd.DataFrame,
    lower_low_lakes_df:          pd.DataFrame,
    lower_high_mean_ser:         pd.Series,
    lower_low_mean_ser:          pd.Series,
    lower_longest_cluster_weeks: list[int]
) -> None:
    """
    Plots `lower_high_lakes_df`, `lower_low_lakes_df`,
    `lower_high_mean_ser`, `lower_low_mean_ser`, and
    `lower_longest_cluster_weeks` onto `lower_bounds_lakes_ax`.

    Parameters
    ----------
    lower_bounds_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    lower_high_lakes_df : :class:`pandas.DataFrame`
        Lower-bounds-depth lakes during a high smoke season

    lower_low_lakes_df : :class:`pandas.DataFrame`
        Lower-bounds-depth lakes during a low smoke season

    lower_high_mean_ser : :class:`pandas.Series`
        `lower_high_lakes_df`'s weekly means, as returned by
        `get_mean_high_ser`

    lower_low_mean_ser : :class:`pandas.Series`
        `lower_low_lakes_df`'s weekly means, as returned by
        `get_mean_low_ser`

    lower_longest_cluster_weeks : list[:class:`int`]
        The weeks, as returned by `get_longest_cluster_weeks`

    Returns
    -------
    None
    """
    plot_significant_cluster_span(
        lower_bounds_lakes_ax,
        longest_cluster_weeks = lower_longest_cluster_weeks
    )

    plot_lakes_df_scatterplot(
        lower_bounds_lakes_ax,
        lower_high_lakes_df,
        color = "#FF0000"
    )
    plot_lakes_df_lineplot(
        lower_bounds_lakes_ax,
        lower_high_mean_ser,
        color = "#FF0000",
        label = "High Smoke Season (Mean)"
    )

    plot_lakes_df_scatterplot(
        lower_bounds_lakes_ax,
        lower_low_lakes_df,
        color = "#0000FF"
    )
    plot_lakes_df_lineplot(
        lower_bounds_lakes_ax,
        lower_low_mean_ser,
        color = "#0000FF",
        label = "Low Smoke Season (Mean)"
    )


def set_upper_bounds_lakes_ax_properties(
    upper_bounds_lakes_ax: plt.Axes, # type: ignore
    *,
    esacci_lakes_variable: str,
    hylak_field:           str,
    form:                  str
) -> None:
    """
    Sets `upper_bounds_lakes_ax`'s properties.

    Parameters
    ----------
    upper_bounds_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to set properties on

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    hylak_field : :class:`str`
        The HydroLAKES field id

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
    hylak_field_upper_bound         = HYLAK_FIELDS[hylak_field].upper_bound
    hylak_field_upper_bound_display = hylak_field_upper_bound / hylak_field_display_scale # type: ignore
    form_qualifier                  = "" if form == "Absolute" else f" {form}"

    upper_bounds_lakes_ax.set_title(f"""Weekly {esacci_lakes_variable_long_name}{form_qualifier} for lakes with {hylak_field_long_name} >= {hylak_field_upper_bound_display:g} {hylak_field_display_units}""")
    upper_bounds_lakes_ax.set_xlabel("Week relative to start of smoke season")
    upper_bounds_lakes_ax.set_ylabel(f"""{esacci_lakes_variable_long_name} ({esacci_lakes_variable_units}){form_qualifier}""")
    upper_bounds_lakes_ax.set_xticks(np.arange(-3, 21).tolist())

    force_ax_xtick_visibility(upper_bounds_lakes_ax)


def set_middle_bounds_lakes_ax_properties(
    middle_bounds_lakes_ax: plt.Axes, # type: ignore
    *,
    esacci_lakes_variable: str,
    hylak_field:           str,
    form:                  str
) -> None:
    """
    Sets `middle_bounds_lakes_ax`'s properties.

    Parameters
    ----------
    middle_bounds_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to set properties on

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    hylak_field : :class:`str`
        The HydroLAKES field id

    form : :class:`str`
        The form of the input data. One of `FORMS`

    Returns
    -------
    None
    """
    esacci_lakes_variable_long_name = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].long_name
    esacci_lakes_variable_units     = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].units
    hylak_field_long_name           = HYLAK_FIELDS[hylak_field].long_name
    hylak_field_lower_bound         = HYLAK_FIELDS[hylak_field].lower_bound
    hylak_field_upper_bound         = HYLAK_FIELDS[hylak_field].upper_bound
    hylak_field_display_units       = HYLAK_FIELDS[hylak_field].display_units or HYLAK_FIELDS[hylak_field].units
    hylak_field_display_scale       = HYLAK_FIELDS[hylak_field].display_scale or HYLAK_FIELDS[hylak_field].scale
    hylak_field_lower_bound_display = hylak_field_lower_bound / hylak_field_display_scale # type: ignore
    hylak_field_upper_bound_display = hylak_field_upper_bound / hylak_field_display_scale # type: ignore
    form_qualifier                  = "" if form == "Absolute" else f" {form}"

    middle_bounds_lakes_ax.set_title(f"""Weekly {esacci_lakes_variable_long_name}{form_qualifier} for lakes with {hylak_field_long_name} between {hylak_field_lower_bound_display:g} {hylak_field_display_units} and {hylak_field_upper_bound_display:g} {hylak_field_display_units}""")
    middle_bounds_lakes_ax.set_xlabel("Week relative to start of smoke season")
    middle_bounds_lakes_ax.set_ylabel(f"""{esacci_lakes_variable_long_name} ({esacci_lakes_variable_units}){form_qualifier}""")
    middle_bounds_lakes_ax.set_xticks(np.arange(-3, 21).tolist())

    force_ax_xtick_visibility(middle_bounds_lakes_ax)


def set_lower_bounds_lakes_ax_properties(
    lower_bounds_lakes_ax: plt.Axes, # type: ignore
    *,
    esacci_lakes_variable: str,
    hylak_field:           str,
    form:                  str
) -> None:
    """
    Sets `lower_bounds_lakes_ax`'s properties.

    Parameters
    ----------
    lower_bounds_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to set properties on

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    hylak_field : :class:`str`
        The HydroLAKES field id

    form : :class:`str`
        The form of the input data. One of `FORMS`

    Returns
    -------
    None
    """
    esacci_lakes_variable_long_name = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].long_name
    esacci_lakes_variable_units     = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].units
    hylak_field_long_name           = HYLAK_FIELDS[hylak_field].long_name
    hylak_field_lower_bound         = HYLAK_FIELDS[hylak_field].lower_bound
    hylak_field_display_units       = HYLAK_FIELDS[hylak_field].display_units or HYLAK_FIELDS[hylak_field].units
    hylak_field_display_scale       = HYLAK_FIELDS[hylak_field].display_scale or HYLAK_FIELDS[hylak_field].scale
    hylak_field_lower_bound_display = hylak_field_lower_bound / hylak_field_display_scale # type: ignore
    form_qualifier                  = "" if form == "Absolute" else f" {form}"

    lower_bounds_lakes_ax.set_title(f"""Weekly {esacci_lakes_variable_long_name}{form_qualifier} for lakes with {hylak_field_long_name} <= {hylak_field_lower_bound_display:g} {hylak_field_display_units}""")
    lower_bounds_lakes_ax.set_xlabel("Week relative to start of smoke season")
    lower_bounds_lakes_ax.set_ylabel(f"""{esacci_lakes_variable_long_name} ({esacci_lakes_variable_units}){form_qualifier}""")
    lower_bounds_lakes_ax.set_xticks(np.arange(-3, 21).tolist())

    force_ax_xtick_visibility(lower_bounds_lakes_ax)


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    upper_high_lakes_df  = read_lakes_csv(args.upper_high_lakes_csv_path)
    upper_low_lakes_df   = read_lakes_csv(args.upper_low_lakes_csv_path)
    middle_high_lakes_df = read_lakes_csv(args.middle_high_lakes_csv_path)
    middle_low_lakes_df  = read_lakes_csv(args.middle_low_lakes_csv_path)
    lower_high_lakes_df  = read_lakes_csv(args.lower_high_lakes_csv_path)
    lower_low_lakes_df   = read_lakes_csv(args.lower_low_lakes_csv_path)

    upper_results_df  = read_results_csv(args.upper_results_csv_path)
    middle_results_df = read_results_csv(args.middle_results_csv_path)
    lower_results_df  = read_results_csv(args.lower_results_csv_path)

    upper_summary_ser  = read_summary_csv(args.upper_summary_csv_path)
    middle_summary_ser = read_summary_csv(args.middle_summary_csv_path)
    lower_summary_ser  = read_summary_csv(args.lower_summary_csv_path)

    upper_high_mean_ser  = get_mean_high_ser(upper_results_df)
    upper_low_mean_ser   = get_mean_low_ser(upper_results_df)
    middle_high_mean_ser = get_mean_high_ser(middle_results_df)
    middle_low_mean_ser  = get_mean_low_ser(middle_results_df)
    lower_high_mean_ser  = get_mean_high_ser(lower_results_df)
    lower_low_mean_ser   = get_mean_low_ser(lower_results_df)

    upper_longest_cluster_weeks  = get_longest_cluster_weeks(upper_summary_ser)
    middle_longest_cluster_weeks = get_longest_cluster_weeks(middle_summary_ser)
    lower_longest_cluster_weeks  = get_longest_cluster_weeks(lower_summary_ser)

    fig, (
        upper_bounds_lakes_ax,
        middle_bounds_lakes_ax,
        lower_bounds_lakes_ax
    ) = plt.subplots(
        nrows   = 3,
        ncols   = 1,
        sharex  = True,
        sharey  = True,
        figsize = (12.8, 14.4)
    )
    plt.subplots_adjust(hspace = 0.25)

    plot_on_upper_bounds_lakes_ax(
        upper_bounds_lakes_ax,
        upper_high_lakes_df         = upper_high_lakes_df,
        upper_low_lakes_df          = upper_low_lakes_df,
        upper_high_mean_ser         = upper_high_mean_ser,
        upper_low_mean_ser          = upper_low_mean_ser,
        upper_longest_cluster_weeks = upper_longest_cluster_weeks
    )
    plot_on_middle_bounds_lakes_ax(
        middle_bounds_lakes_ax,
        middle_high_lakes_df         = middle_high_lakes_df,
        middle_low_lakes_df          = middle_low_lakes_df,
        middle_high_mean_ser         = middle_high_mean_ser,
        middle_low_mean_ser          = middle_low_mean_ser,
        middle_longest_cluster_weeks = middle_longest_cluster_weeks
    )
    plot_on_lower_bounds_lakes_ax(
        lower_bounds_lakes_ax,
        lower_high_lakes_df         = lower_high_lakes_df,
        lower_low_lakes_df          = lower_low_lakes_df,
        lower_high_mean_ser         = lower_high_mean_ser,
        lower_low_mean_ser          = lower_low_mean_ser,
        lower_longest_cluster_weeks = lower_longest_cluster_weeks
    )

    set_upper_bounds_lakes_ax_properties(
        upper_bounds_lakes_ax,
        esacci_lakes_variable = args.esacci_lakes_variable,
        hylak_field           = args.hylak_field,
        form                  = args.form
    )
    set_middle_bounds_lakes_ax_properties(
        middle_bounds_lakes_ax,
        esacci_lakes_variable = args.esacci_lakes_variable,
        hylak_field           = args.hylak_field,
        form                  = args.form
    )
    set_lower_bounds_lakes_ax_properties(
        lower_bounds_lakes_ax,
        esacci_lakes_variable = args.esacci_lakes_variable,
        hylak_field           = args.hylak_field,
        form                  = args.form
    )

    upper_bounds_lakes_ax.legend()
    middle_bounds_lakes_ax.legend()
    lower_bounds_lakes_ax.legend()

    save_figure(
        fig,
        args.output
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())