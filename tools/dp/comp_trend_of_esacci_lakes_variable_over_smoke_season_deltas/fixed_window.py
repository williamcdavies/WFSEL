r"""
fixed_window.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from pathlib import Path

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.proc import (
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_hylak_fields_csv_path,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_hylak_fields_csv_path_exists,
    read_esacci_lakes_metadata_csv,
    read_esacci_lakes_hylak_fields_csv
)
from lib.proc.utils               import (
    add_argument_output,
    argument_output_is_a_file,
    write_df_to_csv
)
from lib.proc.vars                import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)

PROG       = "fixed_window.py"
FIRST_WEEK = 0
LAST_WEEK  = 16


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
    `True` if
    `esacci_lakes_variable_over_high_smoke_season_csv_path` exists.
    `False` otherwise.
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
        description = f"""Produces a csv file containing each lake's latitude, longitude, area, depth, elevation, and volume, alongside its mean delta over a fixed week {FIRST_WEEK}-{LAST_WEEK} window of an ESA CCI Lakes variable's high- and low-smoke-season comparison."""
    )

    # Positional arguments
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_hylak_fields_csv_path(parser)
    add_argument_esacci_lakes_variable_over_high_smoke_season_csv_path(parser)
    add_argument_esacci_lakes_variable_over_low_smoke_season_csv_path(parser)

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
    if not argument_esacci_lakes_metadata_csv_path_exists(
        args.esacci_lakes_metadata_csv_path,
        loud = True
    ):
        return False

    if not argument_esacci_lakes_hylak_fields_csv_path_exists(
        args.esacci_lakes_hylak_fields_csv_path,
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
    Reads `lakes_csv_path` into a :class:`pandas.DataFrame`.

    Parameters
    ----------
    lakes_csv_path : :class:`pathlib.Path`
        The path to some lakes csv file as produced by
        comp_trend_of_esacci_lakes_variable_over_smoke_season.py

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id".
    """
    return pd.read_csv(
        lakes_csv_path,
        index_col = "esacci_lakes_id"
    )


# ==================================================================================================


# Data functions
# ==================================================================================================
def get_esacci_lakes_mean_delta(
    esacci_lakes_id: int,
    *,
    esacci_lakes_variable_over_high_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable_over_low_smoke_season_df:  pd.DataFrame,
    weeks:                                           list[int]
) -> float | None:
    """
    Returns `esacci_lakes_id`'s mean delta over `weeks`.

    Parameters
    ----------
    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    esacci_lakes_variable_over_high_smoke_season_df : :class:`pandas.DataFrame`
        The dataframe, as returned by `read_lakes_csv`

    esacci_lakes_variable_over_low_smoke_season_df : :class:`pandas.DataFrame`
        The dataframe, as returned by `read_lakes_csv`

    weeks : list[:class:`int`]
        The weeks to average over

    Returns
    -------
    A :class:`float`. `None` if `esacci_lakes_id` is not present in
    `esacci_lakes_variable_over_high_smoke_season_df` or
    `esacci_lakes_variable_over_low_smoke_season_df`.
    """
    if (
        esacci_lakes_id not in esacci_lakes_variable_over_high_smoke_season_df.index
        or esacci_lakes_id not in esacci_lakes_variable_over_low_smoke_season_df.index
    ):
        return None

    columns = [f"w_{week}" for week in weeks]

    mean_high = esacci_lakes_variable_over_high_smoke_season_df.loc[esacci_lakes_id, columns].mean()
    mean_low  = esacci_lakes_variable_over_low_smoke_season_df.loc[esacci_lakes_id, columns].mean()

    return mean_high - mean_low


def get_esacci_lakes_deltas_df(
    esacci_lakes_metadata_df: pd.DataFrame,
    *,
    esacci_lakes_hylak_fields_df:                    pd.DataFrame,
    esacci_lakes_variable_over_high_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable_over_low_smoke_season_df:  pd.DataFrame,
    weeks:                                           list[int]
) -> pd.DataFrame:
    """
    Returns each of `esacci_lakes_metadata_df`'s lake's latitude,
    longitude, lake area, depth, elevation, volume, and mean delta over
    `weeks`.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_hylak_fields_df : :class:`pandas.DataFrame`
        The dataframe, as returned by
        `read_esacci_lakes_hylak_fields_csv`

    esacci_lakes_variable_over_high_smoke_season_df : :class:`pandas.DataFrame`
        The dataframe, as returned by `read_lakes_csv`

    esacci_lakes_variable_over_low_smoke_season_df : :class:`pandas.DataFrame`
        The dataframe, as returned by `read_lakes_csv`

    weeks : list[:class:`int`]
        The weeks to average over

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id", with
    columns "latitude", "longitude", "lake_area_m2", "depth_avg_m",
    "elevation_m", "vol_total_m3", and "mean_delta".
    """
    records = []

    for id_, row in esacci_lakes_metadata_df.iterrows():
        hylak_fields_row = esacci_lakes_hylak_fields_df.loc[id_] if id_ in esacci_lakes_hylak_fields_df.index else None

        mean_delta = get_esacci_lakes_mean_delta(
            id_,
            esacci_lakes_variable_over_high_smoke_season_df = esacci_lakes_variable_over_high_smoke_season_df,
            esacci_lakes_variable_over_low_smoke_season_df  = esacci_lakes_variable_over_low_smoke_season_df,
            weeks                                           = weeks
        )

        records.append(
            {
                "esacci_lakes_id": id_,
                "latitude":        row["lat_centre"],
                "longitude":       row["lon_centre"],
                "lake_area_m2":    hylak_fields_row["lake_area_m2"] if hylak_fields_row is not None else None,
                "depth_avg_m":     hylak_fields_row["depth_avg_m"]  if hylak_fields_row is not None else None,
                "elevation_m":     hylak_fields_row["elevation_m"]  if hylak_fields_row is not None else None,
                "vol_total_m3":    hylak_fields_row["vol_total_m3"] if hylak_fields_row is not None else None,
                "mean_delta":      mean_delta
            }
        )

    return pd.DataFrame(records).set_index("esacci_lakes_id")


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    metadata_df     = read_esacci_lakes_metadata_csv(args.esacci_lakes_metadata_csv_path)
    hylak_fields_df = read_esacci_lakes_hylak_fields_csv(args.esacci_lakes_hylak_fields_csv_path)
    high_lakes_df   = read_lakes_csv(args.esacci_lakes_variable_over_high_smoke_season_csv_path)
    low_lakes_df    = read_lakes_csv(args.esacci_lakes_variable_over_low_smoke_season_csv_path)

    weeks = list(range(FIRST_WEEK, LAST_WEEK + 1))

    esacci_lakes_deltas_df = get_esacci_lakes_deltas_df(
        metadata_df,
        esacci_lakes_hylak_fields_df                     = hylak_fields_df,
        esacci_lakes_variable_over_high_smoke_season_df  = high_lakes_df,
        esacci_lakes_variable_over_low_smoke_season_df   = low_lakes_df,
        weeks                                            = weeks
    )

    write_df_to_csv(
        esacci_lakes_deltas_df,
        args.output
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
