r'''
comp_esacci_lakes_variable_relative_to_smoke_season.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import collections
import pathlib
import sys

# Related Third-party Imports
import numpy   as np
import pandas  as pd
import psycopg

from tqdm import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils import (add_argument_esacci_lakes_variable, 
                                    add_argument_esacci_lakes_metadata_filtered_csv_path, 
                                    add_argument_esacci_lakes_average_depths_csv_path, 
                                    add_argument_esacci_lakes_counts_of_smoke_days_csv_path, 
                                    add_argument_esacci_lakes_data_dir_path,
                                    argument_esacci_lakes_variable_is_in_esacci_lakes_variables, 
                                    argument_esacci_lakes_metadata_filtered_csv_path_exists, 
                                    argument_esacci_lakes_average_depths_csv_path_exists, 
                                    argument_esacci_lakes_counts_of_smoke_days_csv_path_exists, 
                                    argument_esacci_lakes_data_dir_path_exists)
from lib.esacci_lakes.vars  import (COUNT_OF_SMOKE_DAYS_LOWER_BOUND, 
                                    COUNT_OF_SMOKE_DAYS_UPPER_BOUND, 
                                    ESACCI_LAKES_VARIABLES)
from lib.io.vars            import (RETURN_FAILURE, 
                                    RETURN_SUCCESS)


PROG='comp_esacci_lakes_variable_relative_to_smoke_season.py'
NUMBER_OF_DAYS_IN_A_PERIOD = 7
NUMBER_OF_LOOKBACK_PERIODS = 3

def week_index(day:    int, 
               anchor: int) -> int:
    '''
    Returns a week index given an arbitrary julian day and an anchor
    julian day.

    Parameters
    ----------
    day : int
        An arbitrary julian day

    anchor: int
        An anchor julian day
    '''
    return (day - anchor) // NUMBER_OF_DAYS_IN_A_PERIOD


def first_day_in_week(week_idx: int, 
                      anchor:   int) -> int:
    '''
    Returns the first julian day in a week given an arbitrary week index
    and an anchor julian day.

    Parameters
    ----------
    week_idx : int
        An arbitrary week index

    anchor: int
        An anchor julian day
    '''
    return anchor + week_idx * NUMBER_OF_DAYS_IN_A_PERIOD


def last_day_in_week(week_idx: int, 
                     anchor:   int) -> int:
    '''
    Returns the last julian day in a week given an arbitrary week index
    and an anchor julian day.

    Parameters
    ----------
    week_idx : int
        An arbitrary week index

    anchor: int
        An anchor julian day
    '''
    return first_day_in_week(week_idx + 1, 
                             anchor) - 1


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog=f'{PROG}.py', 
                                     usage='%(prog)s [options]', 
                                     description='''''')

    # Positional arguments
    add_argument_esacci_lakes_variable(parser)
    add_argument_esacci_lakes_metadata_filtered_csv_path(parser)
    add_argument_esacci_lakes_average_depths_csv_path(parser)
    add_argument_esacci_lakes_counts_of_smoke_days_csv_path(parser)
    add_argument_esacci_lakes_data_dir_path(parser)

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not argument_esacci_lakes_variable_is_in_esacci_lakes_variables(args.esacci_lakes_variable, 
                                                                       loud=True):
        return RETURN_FAILURE
    
    if not argument_esacci_lakes_metadata_filtered_csv_path_exists(args.esacci_lakes_metadata_filtered_csv_path, 
                                                                   loud=True):
        return RETURN_FAILURE

    if not argument_esacci_lakes_average_depths_csv_path_exists(args.esacci_lakes_average_depths_csv_path, 
                                                                loud=True):
        return RETURN_FAILURE

    if not argument_esacci_lakes_counts_of_smoke_days_csv_path_exists(args.esacci_lakes_counts_of_smoke_days_csv_path, 
                                                                      loud=True):
        return RETURN_FAILURE

    if not argument_esacci_lakes_data_dir_path_exists(args.esacci_lakes_data_dir_path, 
                                                      loud=True):
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================      
    hi_records = []
    lo_records = []

    esacci_lakes_metadata_filtered_csv    = pd.read_csv(args.esacci_lakes_metadata_filtered_csv_path, 
                                                        delimiter=';', 
                                                        index_col='id')
    esacci_lakes_average_depths_csv       = pd.read_csv(args.esacci_lakes_average_depths_csv_path, 
                                                        index_col='esacci_lakes_id')
    esacci_lakes_counts_of_smoke_days_csv = pd.read_csv(args.esacci_lakes_counts_of_smoke_days_csv_path, 
                                                        index_col='esacci_lakes_id')

    for esacci_lakes_id in tqdm(esacci_lakes_metadata_filtered_csv.index):
        hi_record                          = {'esacci_lakes_id': esacci_lakes_id}
        hi_esacci_lakes_variable_values = collections.defaultdict(list)
        lo_record                          = {'esacci_lakes_id': esacci_lakes_id}
        lo_esacci_lakes_variable_values = collections.defaultdict(list)

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

        if min(esacci_lakes_counts_of_smoke_days) > COUNT_OF_SMOKE_DAYS_LOWER_BOUND:
            continue

        hi_year = f'{esacci_lakes_counts_of_smoke_days[esacci_lakes_counts_of_smoke_days >= COUNT_OF_SMOKE_DAYS_UPPER_BOUND].index[-1]}'
        lo_year = f'{esacci_lakes_counts_of_smoke_days[esacci_lakes_counts_of_smoke_days <= COUNT_OF_SMOKE_DAYS_LOWER_BOUND].index[-1]}'
            
        with psycopg.connect('dbname=spatial') as conn:
            with conn.cursor() as cur:
                table = f'hms_smokes{hi_year}'
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

        hi_files = sorted(pathlib.Path(args.esacci_lakes_data_dir_path / hi_year).glob('**/*.csv'))
        lo_files = sorted(pathlib.Path(args.esacci_lakes_data_dir_path / lo_year).glob('**/*.csv'))

        day_0 = -1
        day_N = -1

        for i in range(3, len(esacci_lakes_smoke_days)):
            if esacci_lakes_smoke_days[i] < esacci_lakes_smoke_days[i - 3] + 7:
                day_0 = esacci_lakes_smoke_days[i]

                break

        for i in reversed(range(3, len(esacci_lakes_smoke_days))):
            if esacci_lakes_smoke_days[i] < esacci_lakes_smoke_days[i - 3] + 7:
                day_N = esacci_lakes_smoke_days[i]

                break

        if (day_0 == -1 or 
            day_N == -1):
            continue

        start = day_0 - NUMBER_OF_LOOKBACK_PERIODS * NUMBER_OF_DAYS_IN_A_PERIOD
        stop  = last_day_in_week(week_index(day_N, 
                                            day_0), 
                                 day_0)

        if (start < 1             or 
            stop  > len(hi_files) or
            stop  > len(lo_files)):
            continue

        for day_n in range(start, 
                           stop + 1):
            hi_df                              = pd.read_csv(hi_files[day_n - 1], 
                                                             index_col='id')
            hi_esacci_lakes_variable_value  = (hi_df[f'{ESACCI_LAKES_VARIABLES[args.esacci_lakes_variable].var_id}_mean'].loc[esacci_lakes_id]
                                                                                                                         .item())

            lo_df                              = pd.read_csv(lo_files[day_n - 1], 
                                                             index_col='id')
            lo_esacci_lakes_variable_value  = (lo_df[f'{ESACCI_LAKES_VARIABLES[args.esacci_lakes_variable].var_id}_mean'].loc[esacci_lakes_id]
                                                                                                                         .item())

            week_idx = week_index(day_n, 
                                  day_0)

            hi_esacci_lakes_variable_values[week_idx].append(hi_esacci_lakes_variable_value)
            lo_esacci_lakes_variable_values[week_idx].append(lo_esacci_lakes_variable_value)

        for i, l in hi_esacci_lakes_variable_values.items():
            hi_record[f'w{i}'] = np.nanmean(l)

        for i, l in lo_esacci_lakes_variable_values.items():
            lo_record[f'w{i}'] = np.nanmean(l)

        for i in set(hi_esacci_lakes_variable_values) | set(lo_esacci_lakes_variable_values):
            key    = f'w{i}'
            hi_val = hi_record.get(key, np.nan)
            lo_val = lo_record.get(key, np.nan)

            if pd.isna(hi_val) or pd.isna(lo_val):
                hi_record[key] = np.nan
                lo_record[key] = np.nan

        # --- normalisation block: comment out to run unnormalised ---
        hi_normal = np.nanmean([hi_record.get('w-1')])
        lo_normal = np.nanmean([lo_record.get('w-1')])

        if pd.isna(hi_normal) or pd.isna(lo_normal):
            continue

        for key in hi_record:
            if key != 'esacci_lakes_id':
                hi_record[key] -= hi_normal

        for key in lo_record:
            if key != 'esacci_lakes_id':
                lo_record[key] -= lo_normal
        # --- end normalisation block ---

        hi_records.append(hi_record)
        lo_records.append(lo_record)

    hi_df = pd.DataFrame(hi_records)
    lo_df = pd.DataFrame(lo_records)

    hi_df.to_csv(f'hi_{ESACCI_LAKES_VARIABLES[args.esacci_lakes_variable].var_id}_normalised.csv', 
                 index=False)
    lo_df.to_csv(f'lo_{ESACCI_LAKES_VARIABLES[args.esacci_lakes_variable].var_id}_normalised.csv', 
                 index=False)

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == '__main__':
   sys.exit(main())