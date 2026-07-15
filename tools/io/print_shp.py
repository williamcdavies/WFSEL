r'''
print_shp.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import pathlib
import sys

# Related Third-party Imports
import argparse
import geopandas

# Local Application/Library Specific Imports
from lib.io.vars import RETURN_SUCCESS, RETURN_FAILURE


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog='print_shp.py', 
                                     usage='%(prog)s [options]', 
                                     description='''Prints Shapefile
                                                 file metadata to
                                                 `sys.stdout`.''')
    
    # Positional arguments
    parser.add_argument('shp_path',
                        type=pathlib.Path,
                        help=f'''path to Shapefile file''')
    
    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    # If `args.shp_path` does not exist, return with `RETURN_FAILURE`
    if not args.shp_path.exists():
        print(f'''error: argument shp_path: no such file or directory:
               {args.shp_path}''')
        
        return RETURN_FAILURE
    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    # Attempt to ...
    try:
        # Read `args.shp_path` into `gdf`
        gdf = geopandas.read_file(args.shp_path)
    # On exception, return with `RETURN_FAILURE`
    except Exception as e:
        print(f'fatal: exception: {e}')
        
        return RETURN_FAILURE
    
    # Print `gdf` to `sys.stdout`
    print(gdf)

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == '__main__':
    sys.exit(main())