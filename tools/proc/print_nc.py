r"""
print_nc.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from pathlib import Path

# Related Third-party Imports
import xarray as xr

# Local Application/Library Specific Imports
from lib.proc.utils import (
    arguments_are_valid as _arguments_are_valid,
    build_parser        as _build_parser
)
from lib.proc.vars  import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)


# Constants
# ==================================================================================================
PROG = "print_nc.py"


# ==================================================================================================


# Parser functions
# ==================================================================================================
def add_argument_nc_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `nc_path` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `nc_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "nc_path",
        type = Path,
        help = "path to some netCDF file"
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
        "Prints netCDF file metadata to `sys.stdout`.",
        positional_arguments = [
            add_argument_nc_path
        ]
    )


# ==================================================================================================


# Print functions
# ==================================================================================================
def print_nc(
    nc_path: Path
) -> None:
    """
    Prints a netCDF file's metadata to `sys.stdout`.

    Parameters
    ----------
    nc_path : :class:`pathlib.Path`
        The path to some netCDF file

    Returns
    -------
    None.
    """
    with xr.open_dataset(nc_path) as ds:
        print(ds)


# ==================================================================================================


# Validator functions
# ==================================================================================================
def argument_nc_path_exists(
    nc_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `nc_path`.

    Parameters
    ----------
    nc_path : :class:`pathlib.Path`
        The argument `nc_path`

    loud : :class:`bool`
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `nc_path` exists. `False` otherwise.
    """
    if nc_path.exists():
        return True

    if loud:
        print(
            f"error: argument nc_path: no such file or directory: {nc_path}",
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
                argument_nc_path_exists,
                "nc_path"
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

    print_nc(args.nc_path)

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
