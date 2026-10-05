r"""
variable_windows.py

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

PROG   = "variable_windows.py"
GROUPS = [
    "lower",
    "middle",
    "upper"
]
LOWER_BOUND = 0.5e9
UPPER_BOUND = 5e9


# Argument functions
# ==================================================================================================
def add_argument_group_high_lakes_csv_path(
    parser: argparse.ArgumentParser,
    *,
    group: str
) -> None:
    """
    Adds a `{group}_high_lakes_csv_path` argument to a
    :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    group : :class:`str`
        One of `GROUPS`

    Returns
    -------
    None

    Notes
    -----
    Argument `{group}_high_lakes_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        f"{group}_high_lakes_csv_path",
        type = Path,
        help = f"""path to some {group}-volume high-smoke-season lakes csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py"""
    )


def add_argument_group_low_lakes_csv_path(
    parser: argparse.ArgumentParser,
    *,
    group: str
) -> None:
    """
    Adds a `{group}_low_lakes_csv_path` argument to a
    :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    group : :class:`str`
        One of `GROUPS`

    Returns
    -------
    None

    Notes
    -----
    Argument `{group}_low_lakes_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        f"{group}_low_lakes_csv_path",
        type = Path,
        help = f"""path to some {group}-volume low-smoke-season lakes csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py"""
    )


def add_argument_group_summary_csv_path(
    parser: argparse.ArgumentParser,
    *,
    group: str
) -> None:
    """
    Adds a `{group}_summary_csv_path` argument to a
    :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    group : :class:`str`
        One of `GROUPS`

    Returns
    -------
    None

    Notes
    -----
    Argument `{group}_summary_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        f"{group}_summary_csv_path",
        type = Path,
        help = f"""path to some {group}-volume summary csv file as produced by comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_statistics.py"""
    )


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
        description = """Produces a csv file containing each lake's latitude, longitude, lake area, depth, elevation, and volume, alongside its mean delta over its own volume category's longest significant cluster of weeks of an ESA CCI Lakes variable's high- and low-smoke-season comparison."""
    )

    # Positional arguments
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_hylak_fields_csv_path(parser)

    for group in GROUPS:
        add_argument_group_high_lakes_csv_path(
            parser,
            group = group
        )
        add_argument_group_low_lakes_csv_path(
            parser,
            group = group
        )
        add_argument_group_summary_csv_path(
            parser,
            group = group
        )

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

    for group in GROUPS:
        for suffix in (
            "high_lakes_csv_path",
            "low_lakes_csv_path",
            "summary_csv_path"
        ):
            argument_name = f"{group}_{suffix}"
            argument_path = getattr(args, argument_name)

            if not argument_path.exists():
                print(f"""error: argument {argument_name}: no such file or directory: {argument_path}""")
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
        comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py

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


def get_volume_group(
    vol_total_m3: float
) -> str:
    """
    Returns `vol_total_m3`'s volume group.

    Parameters
    ----------
    vol_total_m3 : :class:`float`
        The lake's total volume

    Returns
    -------
    One of `GROUPS`. "lower" if `vol_total_m3` is at or below
    `LOWER_BOUND`, "upper" if at or above `UPPER_BOUND`, "middle"
    otherwise.
    """
    if vol_total_m3 <= LOWER_BOUND:
        return "lower"

    if vol_total_m3 >= UPPER_BOUND:
        return "upper"

    return "middle"


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
    A :class:`float`. `None` if `weeks` is empty, or if
    `esacci_lakes_id` is not present in
    `esacci_lakes_variable_over_high_smoke_season_df` or
    `esacci_lakes_variable_over_low_smoke_season_df`.
    """
    if not weeks:
        return None

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
    esacci_lakes_hylak_fields_df: pd.DataFrame,
    high_lakes_dfs_by_group:      dict[str, pd.DataFrame],
    low_lakes_dfs_by_group:       dict[str, pd.DataFrame],
    weeks_by_group:               dict[str, list[int]]
) -> pd.DataFrame:
    """
    Returns each of `esacci_lakes_metadata_df`'s lake's latitude,
    longitude, lake area, depth, elevation, volume, volume group, and
    mean delta over its own volume group's weeks.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_hylak_fields_df : :class:`pandas.DataFrame`
        The dataframe, as returned by
        `read_esacci_lakes_hylak_fields_csv`

    high_lakes_dfs_by_group : :class:`dict`
        A dict mapping each of `GROUPS` to a dataframe, as returned by
        `read_lakes_csv`

    low_lakes_dfs_by_group : :class:`dict`
        A dict mapping each of `GROUPS` to a dataframe, as returned by
        `read_lakes_csv`

    weeks_by_group : :class:`dict`
        A dict mapping each of `GROUPS` to the weeks, as returned by
        `get_longest_cluster`

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id", with
    columns "latitude", "longitude", "lake_area_m2", "depth_avg_m",
    "elevation_m", "vol_total_m3", "volume_group", and "mean_delta".
    """
    records = []

    for id_, row in esacci_lakes_metadata_df.iterrows():
        hylak_fields_row = esacci_lakes_hylak_fields_df.loc[id_] if id_ in esacci_lakes_hylak_fields_df.index else None
        vol_total_m3     = hylak_fields_row["vol_total_m3"] if hylak_fields_row is not None else None

        if vol_total_m3 is not None:
            group      = get_volume_group(vol_total_m3)
            mean_delta = get_esacci_lakes_mean_delta(
                id_,
                esacci_lakes_variable_over_high_smoke_season_df = high_lakes_dfs_by_group[group],
                esacci_lakes_variable_over_low_smoke_season_df  = low_lakes_dfs_by_group[group],
                weeks                                           = weeks_by_group[group]
            )
        else:
            group      = None
            mean_delta = None

        records.append(
            {
                "esacci_lakes_id": id_,
                "latitude":        row["lat_centre"],
                "longitude":       row["lon_centre"],
                "lake_area_m2":    hylak_fields_row["lake_area_m2"] if hylak_fields_row is not None else None,
                "depth_avg_m":     hylak_fields_row["depth_avg_m"]  if hylak_fields_row is not None else None,
                "elevation_m":     hylak_fields_row["elevation_m"]  if hylak_fields_row is not None else None,
                "vol_total_m3":    vol_total_m3,
                "volume_group":    group,
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

    high_lakes_dfs_by_group = {}
    low_lakes_dfs_by_group  = {}
    weeks_by_group          = {}

    for group in GROUPS:
        high_lakes_dfs_by_group[group] = read_lakes_csv(getattr(args, f"{group}_high_lakes_csv_path"))
        low_lakes_dfs_by_group[group]  = read_lakes_csv(getattr(args, f"{group}_low_lakes_csv_path"))

        summary_df             = read_summary_csv(getattr(args, f"{group}_summary_csv_path"))
        weeks_by_group[group]  = get_longest_cluster(summary_df)

    esacci_lakes_deltas_df = get_esacci_lakes_deltas_df(
        metadata_df,
        esacci_lakes_hylak_fields_df = hylak_fields_df,
        high_lakes_dfs_by_group      = high_lakes_dfs_by_group,
        low_lakes_dfs_by_group       = low_lakes_dfs_by_group,
        weeks_by_group               = weeks_by_group
    )

    write_df_to_csv(
        esacci_lakes_deltas_df,
        args.output
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
