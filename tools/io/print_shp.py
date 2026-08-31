r"""
print_shp.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse import ArgumentParser
from pathlib  import Path

# Related Third-party Imports
import geopandas as gpd

# Local Application/Library Specific Imports
from lib.io.vars import (
    RETURN_SUCCESS,
    RETURN_FAILURE,
)


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = ArgumentParser(
        prog="print_shp.py",
        usage="%(prog)s [options]",
        description="""Prints Shapefile file metadata to `sys.stdout`."""
    )

    # Positional arguments
    parser.add_argument(
        "shp_path",
        type=Path,
        help=f"""path to Shapefile file"""
    )

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not args.shp_path.exists():
        print(
            f"""error: argument shp_path: no such file or directory: {args.shp_path}"""
        )

        return RETURN_FAILURE
    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    gdf = gpd.read_file(args.shp_path)

    print(gdf)

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == "__main__":
    sys.exit(main())
