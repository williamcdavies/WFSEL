r'''
comp_lakes_cci_id_trophic_class.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import pathlib
import sys

# Related Third-party Imports
import tqdm

import numpy  as np
import pandas as pd

# Local Application/Library Specific Imports
from lib.io.vars         import (RETURN_FAILURE, 
                                 RETURN_SUCCESS)
from lib.lakes_cci.utils import (add_argument_lakes_cci_count_of_smoke_days_csv_path, 
                                 add_argument_lakes_cci_ecv_data_dir_path, 
                                 argument_lakes_cci_count_of_smoke_days_csv_path_exists, 
                                 argument_lakes_cci_ecv_data_dir_path_exists)
from lib.lakes_cci.vars  import (COUNT_OF_SMOKE_DAYS_LOWER_BOUND,
                                 COUNT_OF_SMOKE_DAYS_UPPER_BOUND)

def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog='comp_lakes_cci_id_trophic_class.py', 
                                     usage='%(prog)s [options]', 
                                     description='''Computes trophic
                                                 state classifications
                                                 for each lake in the
                                                 candidate set.''')

    # Positional arguments
    add_argument_lakes_cci_ecv_data_dir_path(parser)
    add_argument_lakes_cci_count_of_smoke_days_csv_path(parser)

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    # If `args.lakes_cci_ecv_data_dir_path` does not exist, return with
    # `RETURN_FAILURE`
    if not argument_lakes_cci_ecv_data_dir_path_exists(args.lakes_cci_ecv_data_dir_path, 
                                                       loud=True):
        return RETURN_FAILURE

    # If `args.lakes_cci_count_of_smoke_days_csv_path` does not exist,
    # return with `RETURN_FAILURE`
    if not argument_lakes_cci_count_of_smoke_days_csv_path_exists(args.lakes_cci_count_of_smoke_days_csv_path, 
                                                                  loud=True):
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    lakes_cci_ecv_data_csv_paths = list(args.lakes_cci_ecv_data_dir_path.glob('**/ESA*.csv'))
    data      = []
    
    for lakes_cci_ecv_data_csv_path in tqdm.tqdm(lakes_cci_ecv_data_csv_paths):
        lakes_cci_ecv_data_csv  = pd.read_csv(lakes_cci_ecv_data_csv_path, 
                                              index_col='id')
        chla_mean_ser = lakes_cci_ecv_data_csv['chla_mean']
        chla_mean_ser = chla_mean_ser.dropna()
        it            = chla_mean_ser.items()

        data.extend(list(it))

    df                  = pd.DataFrame(data, 
                                       columns=['lakes_cci_id', 
                                                'chla_mean'])
    df                  = (df.groupby('lakes_cci_id')
                             .agg('mean'))
    df['trophic_class'] = np.select([df['chla_mean'] < 2.6, 
                                     df['chla_mean'] < 7.3, 
                                     df['chla_mean'] < 56], 
                                     ['Oligotrophic', 
                                      'Mesotrophic', 
                                      'Eutrophic'], 
                                     'Hypertrophic')
    df                  = df.drop('chla_mean', 
                                  axis=1)

    df.to_csv('data/lakes_cci_trophic_class.csv')

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == '__main__':
   sys.exit(main())