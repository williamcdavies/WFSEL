r"""
print_shp.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from pathlib import Path

# Related Third-party Imports
import geopandas as gpd

# Local Application/Library Specific Imports
from lib.io.vars import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)

PROG = "print_shp.py"


def add_argument_shp_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `shp_path` argument to a :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `shp_path` is of type :class:`Path`
    """
    parser.add_argument(
        "shp_path",
        type=Path,
        help=f"""path to a Shapefile file"""
    )


def argument_shp_path_exists(
    shp_path: Path,
    *,
    loud:     bool = False
) -> bool:
    """
    Validates `args.shp_path`.

    Parameters
    ----------
    shp_path : :class:`pathlib.Path`
        The argument `shp_path`

    loud : bool
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `shp_path` exists. `False` otherwise.
    """
    if shp_path.exists():
        return True

    if loud:
        print(f"""error: argument shp_path: no such file or directory: {shp_path}""")

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
        description="""Prints Shapefile file metadata to `sys.stdout`."""
    )

    # Positional arguments
    add_argument_shp_path(parser)

    return parser


def arguments_are_valid(
    args: argparse.Namespace
) -> bool:
    """
    Validates `args`.

    Returns
    -------
    `True` if all arguments are successfully validated. `False` otherwise.
    """
    if not argument_shp_path_exists(args.shp_path, loud=True): 
        return False

    return True


def main(
) -> int:
    """
    Orchestration layer.

    Returns
    -------
    0 if program completes successfully. 1 otherwise.
    """
    args = build_parser().parse_args()
    
    if not arguments_are_valid(args): 
        return RETURN_FAILURE

    print(gpd.read_file(args.shp_path))

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
