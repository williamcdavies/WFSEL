r"""
comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_alt.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from pathlib  import Path

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from lib.dataframe.utils              import (
    filter_df_by_column_bounds,
    convert_df_from_kelvin_to_celsius
)
from lib.esacci_lakes.utils.dataframe import (
    drop_hylak_field_columns_from_df,
    merge_dfs_on_esacci_lakes_id
)
from lib.esacci_lakes.utils.proc      import (
    add_argument_esacci_lakes_variable,
    add_argument_hylak_field,
    add_argument_esacci_lakes_hylak_fields_csv_path,
    argument_esacci_lakes_variable_is_in_esacci_lakes_variables,
    argument_hylak_field_is_in_hylak_fields,
    argument_esacci_lakes_hylak_fields_csv_path_exists,
    read_esacci_lakes_hylak_fields_csv
)
from lib.proc.utils                   import (
    add_argument_output,
    argument_output_is_a_directory,
    write_df_to_csv
)
from lib.proc.vars                    import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)

PROG  = "comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_alt.py"
FORMS = [
    "Absolute",
    "Anomaly"
]


# Argument functions
# ==================================================================================================
def add_argument_esacci_lakes_variable_over_high_smoke_season_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `esacci_lakes_variable_over_high_smoke_season_csv_path`
    argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `esacci_lakes_variable_over_high_smoke_season_csv_path` is
    of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "esacci_lakes_variable_over_high_smoke_season_csv_path",
        type = Path,
        help = """path to some csv file produced by comp_trend_of_esacci_lakes_variable_over_smoke_season.py"""
    )


def add_argument_esacci_lakes_variable_over_low_smoke_season_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `esacci_lakes_variable_over_low_smoke_season_csv_path`
    argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `esacci_lakes_variable_over_low_smoke_season_csv_path` is
    of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "esacci_lakes_variable_over_low_smoke_season_csv_path",
        type = Path,
        help = """path to some csv file produced by comp_trend_of_esacci_lakes_variable_over_smoke_season.py"""
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
        help = """the value to split `hylak_field` on"""
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


def argument_esacci_lakes_variable_over_high_smoke_season_csv_path_exists(
    esacci_lakes_variable_over_high_smoke_season_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `esacci_lakes_variable_over_high_smoke_season_csv_path`.

    Parameters
    ----------
    esacci_lakes_variable_over_high_smoke_season_csv_path : :class:`pathlib.Path`
        The argument
        `esacci_lakes_variable_over_high_smoke_season_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `esacci_lakes_variable_over_high_smoke_season_csv_path`
    exists. `False` otherwise.
    """
    if esacci_lakes_variable_over_high_smoke_season_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument esacci_lakes_variable_over_high_smoke_season_csv_path: no such file or directory: {esacci_lakes_variable_over_high_smoke_season_csv_path}""")

    return False


def argument_esacci_lakes_variable_over_low_smoke_season_csv_path_exists(
    esacci_lakes_variable_over_low_smoke_season_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `esacci_lakes_variable_over_low_smoke_season_csv_path`.

    Parameters
    ----------
    esacci_lakes_variable_over_low_smoke_season_csv_path : :class:`pathlib.Path`
        The argument
        `esacci_lakes_variable_over_low_smoke_season_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `esacci_lakes_variable_over_low_smoke_season_csv_path`
    exists. `False` otherwise.
    """
    if esacci_lakes_variable_over_low_smoke_season_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument esacci_lakes_variable_over_low_smoke_season_csv_path: no such file or directory: {esacci_lakes_variable_over_low_smoke_season_csv_path}""")

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
        description = """Produces at-or-below- and at-or-above- threshold high- and low-smoke-season lakes csv files, split by a HydroLAKES field's value against an explicit threshold."""
    )

    # Positional arguments
    add_argument_esacci_lakes_variable(parser)
    add_argument_esacci_lakes_variable_over_high_smoke_season_csv_path(parser)
    add_argument_esacci_lakes_variable_over_low_smoke_season_csv_path(parser)
    add_argument_hylak_field(parser)
    add_argument_threshold(parser)
    add_argument_esacci_lakes_hylak_fields_csv_path(parser)

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

    if not argument_esacci_lakes_variable_over_high_smoke_season_csv_path_exists(
        args.esacci_lakes_variable_over_high_smoke_season_csv_path,
        loud = True
    ):
        return False

    if not argument_esacci_lakes_variable_over_low_smoke_season_csv_path_exists(
        args.esacci_lakes_variable_over_low_smoke_season_csv_path,
        loud = True
    ):
        return False

    if not argument_hylak_field_is_in_hylak_fields(
        args.hylak_field,
        loud = True
    ):
        return False

    if not argument_esacci_lakes_hylak_fields_csv_path_exists(
        args.esacci_lakes_hylak_fields_csv_path,
        loud = True
    ):
        return False

    if not argument_form_is_in_forms(
        args.form,
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
def read_esacci_lakes_variable_over_high_smoke_season_csv(
    esacci_lakes_variable_over_high_smoke_season_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `esacci_lakes_variable_over_high_smoke_season_csv_path` into a
    dataframe.

    Parameters
    ----------
    esacci_lakes_variable_over_high_smoke_season_csv_path : :class:`pathlib.Path`
        The path to some csv file as produced by
        comp_trend_of_esacci_lakes_variable_over_smoke_season.py

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        esacci_lakes_variable_over_high_smoke_season_csv_path,
        index_col = "esacci_lakes_id"
    )


def read_esacci_lakes_variable_over_low_smoke_season_csv(
    esacci_lakes_variable_over_low_smoke_season_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `esacci_lakes_variable_over_low_smoke_season_csv_path` into a
    dataframe.

    Parameters
    ----------
    esacci_lakes_variable_over_low_smoke_season_csv_path : :class:`pathlib.Path`
        The path to some csv file as produced by
        comp_trend_of_esacci_lakes_variable_over_smoke_season.py

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        esacci_lakes_variable_over_low_smoke_season_csv_path,
        index_col = "esacci_lakes_id"
    )


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


def get_at_or_below_threshold_lakes_df(
    df:          pd.DataFrame,
    hylak_field: str,
    threshold:   float
) -> pd.DataFrame:
    """
    Returns `df` filtered to lakes at or below `threshold`, with all
    `HYLAK_FIELDS` columns dropped.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The dataframe

    hylak_field : :class:`str`
        The HydroLAKES field id

    threshold : :class:`float`
        The value to split `hylak_field` on

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    filtered_df = filter_df_by_column_bounds(
        df     = df,
        column = hylak_field,
        lower  = None,
        upper  = threshold
    )

    return drop_hylak_field_columns_from_df(filtered_df)


def get_at_or_above_threshold_lakes_df(
    df:          pd.DataFrame,
    hylak_field: str,
    threshold:   float
) -> pd.DataFrame:
    """
    Returns `df` filtered to lakes at or above `threshold`, with all
    `HYLAK_FIELDS` columns dropped.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The dataframe

    hylak_field : :class:`str`
        The HydroLAKES field id

    threshold : :class:`float`
        The value to split `hylak_field` on

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    filtered_df = filter_df_by_column_bounds(
        df     = df,
        column = hylak_field,
        lower  = threshold,
        upper  = None
    )

    return drop_hylak_field_columns_from_df(filtered_df)


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    variable_over_high_smoke_season_df = read_esacci_lakes_variable_over_high_smoke_season_csv(args.esacci_lakes_variable_over_high_smoke_season_csv_path)
    variable_over_low_smoke_season_df  = read_esacci_lakes_variable_over_low_smoke_season_csv(args.esacci_lakes_variable_over_low_smoke_season_csv_path)
    hylak_fields_df                    = read_esacci_lakes_hylak_fields_csv(args.esacci_lakes_hylak_fields_csv_path)

    if (
        args.form == "Absolute"
        and args.esacci_lakes_variable == "lake_surface_water_temperature"
    ):
        variable_over_high_smoke_season_df = convert_df_from_kelvin_to_celsius(variable_over_high_smoke_season_df)
        variable_over_low_smoke_season_df  = convert_df_from_kelvin_to_celsius(variable_over_low_smoke_season_df)

    variable_over_high_smoke_season_hylak_fields_df = merge_dfs_on_esacci_lakes_id(
        variable_over_high_smoke_season_df,
        hylak_fields_df
    )
    variable_over_low_smoke_season_hylak_fields_df  = merge_dfs_on_esacci_lakes_id(
        variable_over_low_smoke_season_df,
        hylak_fields_df
    )

    above_high_lakes_df = get_at_or_above_threshold_lakes_df(
        variable_over_high_smoke_season_hylak_fields_df,
        args.hylak_field,
        args.threshold
    )
    above_low_lakes_df  = get_at_or_above_threshold_lakes_df(
        variable_over_low_smoke_season_hylak_fields_df,
        args.hylak_field,
        args.threshold
    )
    below_high_lakes_df = get_at_or_below_threshold_lakes_df(
        variable_over_high_smoke_season_hylak_fields_df,
        args.hylak_field,
        args.threshold
    )
    below_low_lakes_df  = get_at_or_below_threshold_lakes_df(
        variable_over_low_smoke_season_hylak_fields_df,
        args.hylak_field,
        args.threshold
    )

    write_df_to_csv(
        above_high_lakes_df,
        args.output,
        name = "above_high_lakes"
    )
    write_df_to_csv(
        above_low_lakes_df,
        args.output,
        name = "above_low_lakes"
    )
    write_df_to_csv(
        below_high_lakes_df,
        args.output,
        name = "below_high_lakes"
    )
    write_df_to_csv(
        below_low_lakes_df,
        args.output,
        name = "below_low_lakes"
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())