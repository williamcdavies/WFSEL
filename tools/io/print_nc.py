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
from lib.io.vars import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)

PROG = "print_nc.py"


def add_argument_nc_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `nc_path` argument to a :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `nc_path` is of type :class:`Path`
    """
    parser.add_argument(
        "nc_path",
        type=Path,
        help=f"""path to netCDF file"""
    )


def argument_nc_path_exists(
    nc_path: Path,
    *,
    loud: bool = False
):
    """
    Validates args.nc_path.

    Parameters
    ----------
    nc_path : :class:`pathlib.Path`
        The argument `nc_path`

    Returns
    -------
    `True` if `nc_path` exists. Returns `False` otherwise.

    loud : bool
        If `True`, prints an error message to stdout. default=False
    """
    if nc_path.exists():
        return True

    if loud:
        print(f"""error: argument nc_path: no such file or directory: {nc_path}""")

    return False


def build_parser(
) -> argparse.ArgumentParser:
    """
    Builds a :class:`ArgumentParser`.

    Returns
    -------
    A :class:`ArgumentParser`.
    """
    parser = argparse.ArgumentParser(
        prog=PROG,
        usage="%(prog)s [options]",
        description="""Prints netCDF file metadata to `sys.stdout`."""
    )

    # Positional arguments
    add_argument_nc_path(parser)

    return parser


def arguments_are_valid(
    args: argparse.Namespace
) -> bool:
    """
    Validates args.

    Returns
    -------
    `True` if all arguments are successfully validated. `False` otherwise.
    """
    if not argument_nc_path_exists(args.nc_path, loud=True): 
        return False

    return True


def main() -> int:
    """
    Orchestration layer.

    Returns
    -------
    0 if program completes successfully. 1 otherwise.
    """
    args = build_parser().parse_args()

    if not arguments_are_valid(args): 
        return RETURN_FAILURE

    with xr.open_dataset(args.nc_path) as ds:
        print(ds)

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
