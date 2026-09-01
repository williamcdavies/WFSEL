r"""
print_nc.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from pathlib  import Path

# Related Third-party Imports
import xarray as xr

# Local Application/Library Specific Imports
from lib.io.vars import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)

PROG = "print_nc.py"


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(
        prog=PROG,
        usage="%(prog)s [options]",
        description="""Prints netCDF file metadata to `sys.stdout`."""
    )

    # Positional arguments
    parser.add_argument(
        "nc_path",
        type=Path,
        required=True,
        help=f"""path to netCDF file"""
    )

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not args.nc_path.exists():
        print(f"""error: argument nc_path: no such file or directory: {args.nc_path}""")

        return RETURN_FAILURE
    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    with xr.open_dataset(args.nc_path) as ds:
        print(ds)

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == "__main__":
    sys.exit(main())
