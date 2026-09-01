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


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(
        prog=PROG,
        usage="%(prog)s [options]",
        description="""Prints Shapefile file metadata to `sys.stdout`."""
    )

    # Positional arguments
    parser.add_argument(
        "shp_path",
        type=Path,
        required=True,
        help=f"""path to Shapefile file"""
    )

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not args.shp_path.exists():
        print(f"""error: argument shp_path: no such file or directory: {args.shp_path}""")

        return RETURN_FAILURE
    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    print(gpd.read_file(args.shp_path))

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == "__main__":
    sys.exit(main())
