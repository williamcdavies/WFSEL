r'''
comp_lakes_cci_id_trophic_class.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import sys

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils import (add_argument_esacci_lakes_counts_of_smoke_days_csv_path, 
                                    add_argument_esacci_lakes_data_dir_path, 
                                    argument_esacci_lakes_counts_of_smoke_days_csv_path_exists, 
                                    argument_esacci_lakes_data_dir_path_exists)
from lib.io.vars            import (RETURN_FAILURE, 
                                    RETURN_SUCCESS)

PROG='comp_lakes_cci_id_trophic_class.py'

def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog=f'{PROG}.py', 
                                     usage='%(prog)s [options]', 
                                     description='''Computes trophic state classifications for each lake in the candidate set.''')

    # Positional arguments
    add_argument_esacci_lakes_data_dir_path(parser)
    add_argument_esacci_lakes_counts_of_smoke_days_csv_path(parser)

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not argument_esacci_lakes_counts_of_smoke_days_csv_path_exists(args.lakes_cci_ecv_data_dir_path, 
                                                                      loud=True):
        return RETURN_FAILURE

    if not argument_esacci_lakes_data_dir_path_exists(args.lakes_cci_count_of_smoke_days_csv_path, 
                                                      loud=True):
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == '__main__':
   sys.exit(main())