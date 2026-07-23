r'''
print_nc.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import pathlib
import sys

# Related Third-party Imports
import xarray

# Local Application/Library Specific Imports
from lib.io.vars import (RETURN_SUCCESS, 
                         RETURN_FAILURE)


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog='print_nc.py', 
                                     usage='%(prog)s [options]', 
                                     description='''Prints netCDF file
                                                 metadata to
                                                 `sys.stdout`.''')
    
    # Positional arguments
    parser.add_argument('nc_path',
                        type=pathlib.Path,
                        help=f'''path to netCDF file''')
    
    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    # If `args.nc_path` does not exist, return with `RETURN_FAILURE`
    if not args.nc_path.exists():
        print(f'''error: argument nc_path: no such file or directory:
               {args.nc_path}''')
        
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    # Attempt to ...
    try:
        # Open `xarray.Dataset` specified by `args.nc_path`
        with xarray.open_dataset(args.nc_path) as ds:
            print(ds)
    # On exception, return with `RETURN_FAILURE`
    except Exception as e:
        print(f'''error: exception: {e}''')
        
        return RETURN_FAILURE

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == '__main__':
    sys.exit(main())