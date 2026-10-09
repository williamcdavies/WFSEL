r"""
summary.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import ast
import sys

from pathlib import Path
from typing  import Any

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.proc import (
    add_argument_local_data_dir_path,
    argument_local_data_dir_path_is_dir
)
from lib.proc.utils              import (
    arguments_are_valid as _arguments_are_valid,
    build_parser        as _build_parser,

    add_argument_output,
    argument_output_is_file_or_missing
)
from lib.proc.vars               import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)


# Constants
# ==================================================================================================
PROG       = "summary.py"
ENTRIES    = [
    (
        "depth_avg_m_anomaly",
        "lower",
        "Depth",
        "Low"
    ),
    (
        "depth_avg_m_anomaly",
        "middle",
        "Depth",
        "Middle"
    ),
    (
        "depth_avg_m_anomaly",
        "upper",
        "Depth",
        "High"
    ),
    (
        "elevation_m_anomaly",
        "below",
        "Elevation",
        "Low"
    ),
    (
        "elevation_m_anomaly",
        "above",
        "Elevation",
        "High"
    ),
    (
        "lake_area_m2_anomaly",
        "lower",
        "Area",
        "Low"
    ),
    (
        "lake_area_m2_anomaly",
        "middle",
        "Area",
        "Middle"
    ),
    (
        "lake_area_m2_anomaly",
        "upper",
        "Area",
        "High"
    ),
    (
        "pour_lat_anomaly",
        "below",
        "Latitude",
        "Low"
    ),
    (
        "pour_lat_anomaly",
        "above",
        "Latitude",
        "High"
    ),
    (
        "vol_total_m3_anomaly",
        "lower",
        "Volume",
        "Low"
    ),
    (
        "vol_total_m3_anomaly",
        "middle",
        "Volume",
        "Middle"
    ),
    (
        "vol_total_m3_anomaly",
        "upper",
        "Volume",
        "High"
    )
]
VARIATIONS = [
    "A",
    "B",
    "C",
    "D"
]


# ==================================================================================================


# DataFrame functions
# ==================================================================================================
def get_summary_df(
    results_dir_path: Path
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of the `ENTRIES` summary.

    Parameters
    ----------
    results_dir_path : :class:`pathlib.Path`
        The results directory path

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.DataFrame(
        [
            get_summary_record(
                results_dir_path,
                folder    = folder,
                subfolder = subfolder,
                variable  = variable,
                group     = group
            )
            for (
                folder,
                subfolder,
                variable,
                group
            )
            in ENTRIES
        ]
    )


def get_summary_record(
    results_dir_path: Path,
    *,
    folder:           str,
    subfolder:        str,
    variable:         str,
    group:            str
) -> dict[str, Any]:
    """
    Returns a record summarising the results of `folder` and `subfolder`,
    labelled with `variable` and `group`.

    Parameters
    ----------
    results_dir_path : :class:`pathlib.Path`
        The results directory path

    folder : :class:`str`
        The field folder name

    subfolder : :class:`str`
        The group subfolder name

    variable : :class:`str`
        The display name of the field

    group : :class:`str`
        The display name of the group

    Returns
    -------
    A :class:`dict`.
    """
    directory = results_dir_path / folder / subfolder

    results_df = pd.read_csv(
        directory / "results.csv",
        index_col = "w"
    )
    summary_df = pd.read_csv(
        directory / "summary.csv",
        index_col = 0
    )

    longest_cluster_weeks = ast.literal_eval(summary_df["longest_cluster_weeks"].iloc[0])

    if longest_cluster_weeks:
        range_of_significant_weeks  = f"{min(longest_cluster_weeks)}-{max(longest_cluster_weeks)}"
        number_of_significant_weeks = len(longest_cluster_weeks)
        min_significant_delta       = round(
            summary_df["longest_cluster_min_delta"].iloc[0],
            3
        )
        max_significant_delta       = round(
            summary_df["longest_cluster_max_delta"].iloc[0],
            3
        )
        average_significant_delta   = round(
            results_df.loc[
                longest_cluster_weeks,
                "mean_delta"
            ].mean(),
            3
        )
    else:
        range_of_significant_weeks  = "None"
        number_of_significant_weeks = 0
        min_significant_delta       = None
        max_significant_delta       = None
        average_significant_delta   = None

    return {
        "Variable":                          variable,
        "Group":                             group,
        "Range of Significant Weeks":        range_of_significant_weeks,
        "Number of Significant Weeks":       number_of_significant_weeks,
        "Min Significant Delta (deg C)":     min_significant_delta,
        "Max Significant Delta (deg C)":     max_significant_delta,
        "Average Significant Delta (deg C)": average_significant_delta
    }


# ==================================================================================================


# Parser functions
# ==================================================================================================
def add_argument_variation(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `variation` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `variation` is of type :class:`str`.
    """
    parser.add_argument(
        "variation",
        type = str,
        help = f"one of {", ".join(VARIATIONS)}"
    )


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
        "Produces a .csv file containing results summary for one variation of strategies A-D.",
        positional_arguments = [
            add_argument_local_data_dir_path,
            add_argument_variation
        ],
        optional_arguments   = [
            add_argument_output
        ]
    )


# ==================================================================================================


# System functions
# ==================================================================================================
def get_results_dir_path(
    local_data_dir_path: Path,
    variation:           str
) -> Path:
    """
    Returns the results directory path for `variation`.

    Parameters
    ----------
    local_data_dir_path : :class:`pathlib.Path`
        The local data directory path

    variation : :class:`str`
        One of `VARIATIONS`

    Returns
    -------
    A :class:`pathlib.Path`.
    """
    return local_data_dir_path / "results" / variation / "results"


# ==================================================================================================


# Validator functions
# ==================================================================================================
def argument_variation_is_in_variations(
    variation: str,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `variation`.

    Parameters
    ----------
    variation : :class:`str`
        The argument `variation`

    loud : :class:`bool`
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `variation` is in `VARIATIONS`. `False` otherwise.
    """
    if variation in VARIATIONS:
        return True

    if loud:
        print(
            f"error: argument variation: not in {VARIATIONS}: {variation}",
            file = sys.stderr
        )

    return False


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
    `True` if all arguments are successfully validated. `False` otherwise.
    """
    return _arguments_are_valid(
        args,
        [
            (
                argument_local_data_dir_path_is_dir,
                "local_data_dir_path"
            ),
            (
                argument_variation_is_in_variations,
                "variation"
            ),
            (
                argument_output_is_file_or_missing,
                "output"
            )
        ]
    )


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser().parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    results_dir_path = get_results_dir_path(
        args.local_data_dir_path,
        args.variation
    )

    if not results_dir_path.is_dir():
        print(
            f"error: no such directory: {results_dir_path}",
            file = sys.stderr
        )

        return RETURN_FAILURE

    summary_df = get_summary_df(results_dir_path)

    args.output.parent.mkdir(
        parents  = True,
        exist_ok = True
    )
    summary_df.to_csv(
        args.output,
        index = False
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
