r'''
_.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import sys

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from lib.io.vars            import (RETURN_FAILURE, 
                                    RETURN_SUCCESS)
from lib.esacci_lakes.utils import (add_argument_esacci_lakes_counts_of_smoke_days_csv_path, 
                                    argument_esacci_lakes_counts_of_smoke_days_csv_path_exists)
from lib.esacci_lakes.vars  import (COUNT_OF_SMOKE_DAYS_LOWER_BOUND, 
                                    COUNT_OF_SMOKE_DAYS_UPPER_BOUND)

PROG='_.py'

def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog=f'_.py', 
                                     usage='%(prog)s [options]', 
                                     description='''''')

    # Positional arguments
    add_argument_esacci_lakes_counts_of_smoke_days_csv_path(parser)

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not argument_esacci_lakes_counts_of_smoke_days_csv_path_exists(args.esacci_lakes_counts_of_smoke_days_csv_path, 
                                                                  loud=True): 
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    esacci_lakes_counts_of_smoke_days_csv = pd.read_csv(args.esacci_lakes_counts_of_smoke_days_csv_path, 
                                                        index_col='esacci_lakes_id')
    l                                     = []

    for row in esacci_lakes_counts_of_smoke_days_csv.itertuples():
        index  = row[0]
        values = row[1:]
        count_of_low_smoke_years  = sum(1 for value in values if value <= COUNT_OF_SMOKE_DAYS_LOWER_BOUND)
        count_of_high_smoke_years = sum(1 for value in values if value >= COUNT_OF_SMOKE_DAYS_UPPER_BOUND)

        if (count_of_low_smoke_years >= 5 
            and count_of_high_smoke_years >= 1):
            l.append(index)

    print(l)
    
    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == '__main__':
   sys.exit(main())