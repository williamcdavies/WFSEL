r"""
get_esacci_lakes_data_for_one_lake.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from pathlib import Path
from typing  import Any

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.proc import (
    add_argument_esacci_lakes_id,
    add_argument_local_data_dir_path,
    argument_local_data_dir_path_is_dir,
    get_esacci_lakes_filename_time,
    read_local_data_csv
)
from lib.proc.utils              import (
    arguments_are_valid as _arguments_are_valid,
    build_parser        as _build_parser,

    add_argument_output,
    argument_output_is_file_or_missing,
    get_file_paths_from_dir_by_extension,
    write_df_to_csv
)
from lib.proc.vars               import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)


# Constants
# ==================================================================================================
PROG                = "get_esacci_lakes_data_for_one_lake.py"
LOCAL_DATA_RUN_DATE = "22-09-26"


# ==================================================================================================


# DataFrame functions
# ==================================================================================================
def get_lake_data_df(
    local_data_csv_paths: list[Path],
    esacci_lakes_id:      int
) -> pd.DataFrame:
    """
    Returns `esacci_lakes_id`'s record from each of
    `local_data_csv_paths`.

    Parameters
    ----------
    local_data_csv_paths : list[:class:`pathlib.Path`]
        The paths to some local data csv files

    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id".
    """
    records = [
        get_lake_data_record(
            local_data_csv_path,
            esacci_lakes_id
        )
        for local_data_csv_path
        in local_data_csv_paths
    ]

    return pd.DataFrame(records).set_index("esacci_lakes_id")


def get_lake_data_record(
    local_data_csv_path: Path,
    esacci_lakes_id:     int
) -> dict[str, Any]:
    """
    Returns `esacci_lakes_id`'s record from `local_data_csv_path`.

    Parameters
    ----------
    local_data_csv_path : :class:`pathlib.Path`
        The path to some local data csv file

    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    Returns
    -------
    A :class:`dict` with keys "esacci_lakes_id", "date", and
    `local_data_csv_path`'s columns.
    """
    local_data_datetime = get_esacci_lakes_filename_time(local_data_csv_path)
    local_data_df       = read_local_data_csv(local_data_csv_path)

    record         = {"esacci_lakes_id": esacci_lakes_id}
    record["date"] = local_data_datetime.strftime("%Y-%m-%d")
    record.update(local_data_df.loc[esacci_lakes_id].to_dict())

    return record


# ==================================================================================================


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
        "Produces a csv file containing all of one lake's local data records, indexed by date.",
        positional_arguments = [
            add_argument_esacci_lakes_id,
            add_argument_local_data_dir_path
        ],
        optional_arguments   = [
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

    local_data_csv_paths = get_file_paths_from_dir_by_extension(
        args.local_data_dir_path / "main.py" / LOCAL_DATA_RUN_DATE,
        "csv"
    )
    local_lake_data_df   = get_lake_data_df(
        local_data_csv_paths,
        args.esacci_lakes_id
    )

    write_df_to_csv(
        local_lake_data_df,
        args.output
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
