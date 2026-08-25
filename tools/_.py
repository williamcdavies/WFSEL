r'''
_.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import sys

# Related Third-party Imports
import pandas  as pd
import psycopg

from tqdm import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils import (add_argument_esacci_lakes_metadata_csv_path, 
                                    add_argument_esacci_lakes_average_depths_csv_path, 
                                    add_argument_esacci_lakes_counts_of_smoke_days_csv_path, 
                                    argument_esacci_lakes_metadata_csv_path_exists, 
                                    argument_esacci_lakes_average_depths_csv_path_exists, 
                                    argument_esacci_lakes_counts_of_smoke_days_csv_path_exists)
from lib.esacci_lakes.vars  import (COUNT_OF_SMOKE_DAYS_LOWER_BOUND, 
                                    COUNT_OF_SMOKE_DAYS_UPPER_BOUND)
from lib.io.vars            import (RETURN_FAILURE, 
                                    RETURN_SUCCESS)

PROG='_.py'

def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog=f'{PROG}.py', 
                                     usage='%(prog)s [options]', 
                                     description='''''')

    # Positional arguments
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_average_depths_csv_path(parser)
    add_argument_esacci_lakes_counts_of_smoke_days_csv_path(parser)

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not argument_esacci_lakes_metadata_csv_path_exists(args.esacci_lakes_metadata_csv_path, 
                                                          loud=True):
        return RETURN_FAILURE

    if not argument_esacci_lakes_average_depths_csv_path_exists(args.esacci_lakes_average_depths_csv_path, 
                                                                loud=True):
        return RETURN_FAILURE

    if not argument_esacci_lakes_counts_of_smoke_days_csv_path_exists(args.esacci_lakes_counts_of_smoke_days_csv_path, 
                                                                      loud=True):
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================  
    esacci_lakes_metadata_csv             = pd.read_csv(args.esacci_lakes_metadata_csv_path, 
                                                        delimiter=';', 
                                                        index_col='id')
    esacci_lakes_average_depths_csv       = pd.read_csv(args.esacci_lakes_average_depths_csv_path, 
                                                        index_col='esacci_lakes_id')
    esacci_lakes_counts_of_smoke_days_csv = pd.read_csv(args.esacci_lakes_counts_of_smoke_days_csv_path, 
                                                        index_col='esacci_lakes_id')

    for esacci_lakes_id in esacci_lakes_metadata_csv.index:
        esacci_lakes_average_depth        = esacci_lakes_average_depths_csv.loc[esacci_lakes_id]
        assert isinstance(esacci_lakes_average_depth, 
                          pd.Series)

        esacci_lakes_counts_of_smoke_days = esacci_lakes_counts_of_smoke_days_csv.loc[esacci_lakes_id]
        assert isinstance(esacci_lakes_counts_of_smoke_days, 
                          pd.Series)

        if pd.isna(esacci_lakes_average_depth.item()):
            continue

        if max(esacci_lakes_counts_of_smoke_days) < COUNT_OF_SMOKE_DAYS_UPPER_BOUND:
            continue

        with psycopg.connect('dbname=spatial') as conn:
            with conn.cursor() as cur:
                table = f'hms_smokes{esacci_lakes_counts_of_smoke_days[esacci_lakes_counts_of_smoke_days == max(esacci_lakes_counts_of_smoke_days)].index[-1]}'
                query = f'''
                    WITH xref as (
                        SELECT
                            l.geom
                        FROM esacci_lakes AS l
                        WHERE l.id = {esacci_lakes_id}
                    )
                    SELECT DISTINCT ON (s.start_day)
                        s.start_day AS "day"
                    FROM {table} AS s
                    JOIN xref AS x
                        ON ST_INTERSECTS(s.geom, x.geom)
                    WHERE s.density > 1
                    ORDER BY s.start_day
                    '''
                
                cur.execute(query) # type: ignore

                esacci_lakes_smoke_days = pd.Series([tuple[0] for tuple in cur.fetchall()], 
                                                    name=esacci_lakes_id)

                if (len(esacci_lakes_smoke_days) < 4):
                    continue

        for i in range(len(esacci_lakes_smoke_days) - 3):
            if esacci_lakes_smoke_days[i + 3] < esacci_lakes_smoke_days[i] + 7:
                w_0 = i

                break

        for i in range(len(esacci_lakes_smoke_days[::-1]) - 3): 
            if esacci_lakes_smoke_days[i + 3] < esacci_lakes_smoke_days[i] + 7:
                w_n = i

                break
    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == '__main__':
   sys.exit(main())