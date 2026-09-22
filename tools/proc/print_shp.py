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
from lib.proc.vars import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)

PROG = "print_shp.py"


# Argument functions
# ==================================================================================================
def add_argument_shp_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `shp_path` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `shp_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "shp_path",
        type = Path,
        help = """path to some Shapefile"""
    )


def argument_shp_path_exists(
    shp_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `shp_path`.

    Parameters
    ----------
    shp_path : :class:`pathlib.Path`
        The argument `shp_path`

    loud : :class:`bool`
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
        description = """Prints Shapefile metadata to `sys.stdout`."""
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
    `True` if all arguments are successfully validated. `False`
    otherwise.
    """
    if not argument_shp_path_exists(
        args.shp_path,
        loud = True
    ):
        return False

    return True


# ==================================================================================================


# Print functions
# ==================================================================================================
def print_shp(
    shp_path: Path
) -> None:
    """
    Prints a Shapefile's metadata to `sys.stdout`.

    Parameters
    ----------
    shp_path : :class:`pathlib.Path`
        The path to some Shapefile

    Returns
    -------
    None
    """
    gdf = gpd.read_file(shp_path)

    print(gdf)


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    print_shp(args.shp_path)

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
