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


# Argument functions
# ==================================================================================================
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
    Argument `nc_path` is of type :class:`Path`.
    """
    parser.add_argument(
        "nc_path",
        type = Path,
        help = """path to some netCDF file"""
    )


def argument_nc_path_exists(
    nc_path: Path,
    *,
    loud:    bool = False
) -> bool:
    """
    Validates `nc_path`.

    Parameters
    ----------
    nc_path : :class:`pathlib.Path`
        The argument `nc_path`

    loud : bool
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `nc_path` exists. `False` otherwise.
    """
    if nc_path.exists():
        return True

    if loud:
        print(f"""error: argument nc_path: no such file or directory: {nc_path}""")

    return False


def build_parser(
    prog: str
) -> argparse.ArgumentParser:
    """
    Builds a :class:`ArgumentParser`.

    Parameters
    ----------
    prog : :class:`str`
        The program name

    Returns
    -------
    A :class:`ArgumentParser`.
    """
    parser = argparse.ArgumentParser(
        prog        = prog,
        usage       = "%(prog)s [options]",
        description = """Prints netCDF file metadata to `sys.stdout`."""
    )

    # Positional arguments
    add_argument_nc_path(parser)

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
    if not argument_nc_path_exists(
        args.nc_path,
        loud = True
    ):
        return False

    return True


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
    None
    """
    with xr.open_dataset(nc_path) as ds:
        print(ds)


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()

    if not arguments_are_valid(args): 
        return RETURN_FAILURE

    print_nc(args.nc_path)

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
