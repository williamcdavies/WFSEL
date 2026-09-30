r"""
comp_trend_of_esacci_lakes_variable_over_smoke_season_deltas.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import ast
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

PROG = "comp_trend_of_esacci_lakes_variable_over_smoke_season_deltas.py"


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


def add_argument_summary_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `summary_csv_path` argument to a
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
    Argument `summary_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "summary_csv_path",
        type = Path,
        help = """path to some summary csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py"""
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


def argument_summary_csv_path_exists(
    summary_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `summary_csv_path`.

    Parameters
    ----------
    summary_csv_path : :class:`pathlib.Path`
        The argument `summary_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `summary_csv_path` exists. `False` otherwise.
    """
    if summary_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument summary_csv_path: no such file or directory: {summary_csv_path}""")

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
        description = """Produces a csv file containing each lake's latitude, longitude, and volume, alongside its mean delta over the longest significant cluster of weeks of an ESA CCI Lakes variable's high- and low-smoke-season comparison."""
    )

    # Positional arguments
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_hylak_fields_csv_path(parser)
    add_argument_esacci_lakes_variable_over_high_smoke_season_csv_path(parser)
    add_argument_esacci_lakes_variable_over_low_smoke_season_csv_path(parser)
    add_argument_summary_csv_path(parser)

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

    if not argument_summary_csv_path_exists(
        args.summary_csv_path,
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


def read_summary_csv(
    summary_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `summary_csv_path` into a :class:`pandas.DataFrame`.

    Parameters
    ----------
    summary_csv_path : :class:`pathlib.Path`
        The path to some summary csv file as produced by
        comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py

    Returns
    -------
    A single-row :class:`pandas.DataFrame`.
    """
    return pd.read_csv(summary_csv_path)


# ==================================================================================================


# Data functions
# ==================================================================================================
def get_longest_cluster(
    summary_df: pd.DataFrame
) -> list[int]:
    """
    Returns `summary_df`'s "longest_cluster_weeks" field, parsed from
    its string representation.

    Parameters
    ----------
    summary_df : :class:`pandas.DataFrame`
        The dataframe, as returned by `read_summary_csv`

    Returns
    -------
    A list of :class:`int`.
    """
    return ast.literal_eval(summary_df["longest_cluster_weeks"].iloc[0])


def get_esacci_lakes_mean_delta(
    esacci_lakes_id: int,
    *,
    esacci_lakes_variable_over_high_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable_over_low_smoke_season_df:  pd.DataFrame,
    longest_cluster_weeks:                           list[int]
) -> float | None:
    """
    Returns `esacci_lakes_id`'s mean delta over `longest_cluster_weeks`.

    Parameters
    ----------
    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    esacci_lakes_variable_over_high_smoke_season_df : :class:`pandas.DataFrame`
        The dataframe, as returned by `read_lakes_csv`

    esacci_lakes_variable_over_low_smoke_season_df : :class:`pandas.DataFrame`
        The dataframe, as returned by `read_lakes_csv`

    longest_cluster_weeks : list[:class:`int`]
        The weeks, as returned by `get_longest_cluster`

    Returns
    -------
    A :class:`float`. `None` if `longest_cluster_weeks` is empty, or if
    `esacci_lakes_id` is not present in
    `esacci_lakes_variable_over_high_smoke_season_df` or
    `esacci_lakes_variable_over_low_smoke_season_df`.
    """
    if not longest_cluster_weeks:
        return None

    if (
        esacci_lakes_id not in esacci_lakes_variable_over_high_smoke_season_df.index
        or esacci_lakes_id not in esacci_lakes_variable_over_low_smoke_season_df.index
    ):
        return None

    columns = [f"w_{week}" for week in longest_cluster_weeks]

    mean_high = esacci_lakes_variable_over_high_smoke_season_df.loc[esacci_lakes_id, columns].mean()
    mean_low  = esacci_lakes_variable_over_low_smoke_season_df.loc[esacci_lakes_id, columns].mean()

    return mean_high - mean_low # type: ignore


def get_esacci_lakes_deltas_df(
    esacci_lakes_metadata_df: pd.DataFrame,
    *,
    esacci_lakes_hylak_fields_df:                     pd.DataFrame,
    esacci_lakes_variable_over_high_smoke_season_df:  pd.DataFrame,
    esacci_lakes_variable_over_low_smoke_season_df:   pd.DataFrame,
    longest_cluster_weeks:                            list[int]
) -> pd.DataFrame:
    """
    Returns each of `esacci_lakes_metadata_df`'s lake's latitude,
    longitude, volume, and mean delta over `longest_cluster_weeks`.

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

    longest_cluster_weeks : list[:class:`int`]
        The weeks, as returned by `get_longest_cluster`

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id", with
    columns "latitude", "longitude", "vol_total_m3", and "mean_delta".
    """
    records = []

    for id_, row in esacci_lakes_metadata_df.iterrows():
        vol_total_m3 = esacci_lakes_hylak_fields_df["vol_total_m3"].get(id_)

        mean_delta = get_esacci_lakes_mean_delta(
            id_, # type: ignore
            esacci_lakes_variable_over_high_smoke_season_df = esacci_lakes_variable_over_high_smoke_season_df,
            esacci_lakes_variable_over_low_smoke_season_df  = esacci_lakes_variable_over_low_smoke_season_df,
            longest_cluster_weeks                           = longest_cluster_weeks
        )

        records.append(
            {
                "esacci_lakes_id": id_,
                "latitude":        row["lat_centre"],
                "longitude":       row["lon_centre"],
                "vol_total_m3":    vol_total_m3,
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

    metadata_df      = read_esacci_lakes_metadata_csv(args.esacci_lakes_metadata_csv_path)
    hylak_fields_df  = read_esacci_lakes_hylak_fields_csv(args.esacci_lakes_hylak_fields_csv_path)
    high_lakes_df    = read_lakes_csv(args.esacci_lakes_variable_over_high_smoke_season_csv_path)
    low_lakes_df     = read_lakes_csv(args.esacci_lakes_variable_over_low_smoke_season_csv_path)
    summary_df       = read_summary_csv(args.summary_csv_path)

    longest_cluster_weeks = get_longest_cluster(summary_df)

    esacci_lakes_deltas_df = get_esacci_lakes_deltas_df(
        metadata_df,
        esacci_lakes_hylak_fields_df                     = hylak_fields_df,
        esacci_lakes_variable_over_high_smoke_season_df  = high_lakes_df,
        esacci_lakes_variable_over_low_smoke_season_df   = low_lakes_df,
        longest_cluster_weeks                            = longest_cluster_weeks
    )

    write_df_to_csv(
        esacci_lakes_deltas_df,
        args.output
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
