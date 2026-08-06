# Standard Library Imports
import argparse
import pathlib
import sys

# Related Third-party Imports
import tqdm

import numpy  as np
import pandas as pd

# Local Application/Library Specific Imports
from lib.io.vars import (RETURN_FAILURE, 
                         RETURN_SUCCESS)


CHLA_MEAN    = 'chla_mean'
LAKES_CCI_ID = 'lakes_cci_id'


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
    parser.add_argument('ecv_data_dir_path',
                        type=pathlib.Path,
                        help=f'''path to Lakes ECV data directory as
                              produced by main.py''')

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    # If `args.ecv_data_dir_path` does not exist, return with
    # `RETURN_FAILURE`
    if not args.ecv_data_dir_path.exists():
        print(f'''error: argument ecv_data_dir_path: no such file or
               directory: {args.ecv_data_dir_path}''')
        
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    csv_paths = list(args.ecv_data_dir_path.glob('**/ESA*.csv'))
    data      = []
    
    for csv_path in tqdm.tqdm(csv_paths):
        csv = pd.read_csv(csv_path, 
                          index_col='id')
        ser = csv[CHLA_MEAN]
        ser = ser.dropna()
        it  = ser.items()

        data.extend(list(it))

    df                  = pd.DataFrame(data, 
                                       columns=[LAKES_CCI_ID, 
                                                CHLA_MEAN])
    df                  = (df.groupby(LAKES_CCI_ID)
                             .agg('mean'))
    df['trophic_class'] = np.select([df[CHLA_MEAN] < 2.6, 
                                     df[CHLA_MEAN] < 7.3, 
                                     df[CHLA_MEAN] < 56], 
                                     ['Oligotrophic', 
                                      'Mesotrophic', 
                                      'Eutrophic'], 
                                     'Hypertrophic')
    df                  = df.drop(CHLA_MEAN, 
                                  axis=1)

    df.to_csv('data/lakes_cci_id_trophic_class.csv')

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == '__main__':
   sys.exit(main())