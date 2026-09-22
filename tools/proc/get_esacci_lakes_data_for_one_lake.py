r"""
get_esacci_lakes_data_for_one_lake.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from datetime import datetime
from pathlib  import Path
from typing   import Any

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.proc import (
    add_argument_esacci_lakes_id,
    add_argument_local_data_dir_path,
    argument_local_data_dir_path_exists,
    read_local_data_csv
)
from lib.proc.utils              import (
    add_argument_output,
    argument_output_is_a_file
)
from lib.proc.vars               import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)

PROG = "get_esacci_lakes_data_for_one_lake.py"


# Argument functions
# ==================================================================================================
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
        description = """"""
    )

    # Positional arguments
    add_argument_esacci_lakes_id(parser)
    add_argument_local_data_dir_path(parser)

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
    if not argument_local_data_dir_path_exists(
        args.local_data_dir_path,
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


# Data functions
# ==================================================================================================
def get_local_data_csv_paths(
    local_data_dir_path: Path
) -> list[Path]:
    """
    Returns each local data csv file's path in
    `local_data_dir_path`.

    Parameters
    ----------
    local_data_dir_path : :class:`pathlib.Path`
        The directory

    Returns
    -------
    A sorted list of :class:`pathlib.Path`.
    """
    local_data_subdir_path = local_data_dir_path / "main.py" / "31-08-26"

    return sorted(local_data_subdir_path.glob("**/*.csv"))


def get_local_data_datetime(
    local_data_csv_path: Path
) -> datetime:
    """
    Returns the datetime for `local_data_csv_path`.

    Parameters
    ----------
    local_data_csv_path : :class:`pathlib.Path`
        The path to some local data csv file

    Returns
    -------
    A :class:`datetime.datetime`.
    """
    date_string = local_data_csv_path.stem.split("-")[5]
    
    return datetime.strptime(
        date_string,
        "%Y%m%d"
    )


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
    local_data_datetime = get_local_data_datetime(local_data_csv_path)
    local_data_df       = read_local_data_csv(local_data_csv_path)

    record: dict[str, Any] = {"esacci_lakes_id": esacci_lakes_id}
    record["date"]         = local_data_datetime.strftime("%Y-%m-%d")
    record.update(local_data_df.loc[esacci_lakes_id].to_dict()) # type: ignore

    return record


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


# ==================================================================================================


# Write functions
# ==================================================================================================

def write_local_lake_data_df_to_csv(
    lake_data_df: pd.DataFrame,
    output:       Path
) -> None:
    """
    Writes `lake_data_df` to `output`.

    Parameters
    ----------
    lake_data_df : :class:`pandas.DataFrame`
        The dataframe

    output : :class:`pathlib.Path`
        The output file path

    Returns
    -------
    None
    """
    output.parent.mkdir(
        parents  = True,
        exist_ok = True
    )

    lake_data_df.to_csv(output)


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    local_data_csv_paths = get_local_data_csv_paths(args.local_data_dir_path)
    local_lake_data_df   = get_lake_data_df(
        local_data_csv_paths,
        args.esacci_lakes_id
    )

    write_local_lake_data_df_to_csv(
        local_lake_data_df,
        args.output
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
