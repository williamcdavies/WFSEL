r'''
view_all_low_smoke_years_and_one_high_smoke_year.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import pathlib
import sys

# Related Third-party Imports
import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd
import seaborn           as sns

from pygam import LinearGAM, s

# Local Application/Library Specific Imports
from lib.io.vars         import (RETURN_FAILURE, 
                                 RETURN_SUCCESS)
from lib.lakes_cci.utils import (add_argument_lakes_cci_count_of_smoke_days_csv_path, 
                                 add_argument_lakes_cci_ecv_data_dir_path, 
                                 add_argument_lakes_cci_ecv, 
                                 add_argument_lakes_cci_id, 
                                 add_argument_lakes_cci_measure, 
                                 add_argument_lakes_cci_smoke_days_csv_path, 
                                 argument_lakes_cci_count_of_smoke_days_csv_path_exists, 
                                 argument_lakes_cci_ecv_data_dir_path_exists, 
                                 argument_lakes_cci_ecv_is_in_lakes_cci_ecvs, 
                                 argument_lakes_cci_measure_is_in_lakes_cci_measures, 
                                 argument_lakes_cci_smoke_days_csv_path_exists)
from lib.lakes_cci.vars  import COUNT_OF_SMOKE_DAYS_LOWER_BOUND


def fit(df: pd.DataFrame, 
        lakes_cci_ecv: str, 
        lakes_cci_measure: str) -> LinearGAM:
    df_nonan = df.dropna(subset=[f'{lakes_cci_ecv}_{lakes_cci_measure}'])
    X        = df_nonan['index'].values
    y        = df_nonan[f'{lakes_cci_ecv}_{lakes_cci_measure}'].values

    return LinearGAM(s(0)).fit(X, y)


def dfs(lakes_cci_ecv_data_dir_paths: list[pathlib.Path], 
        lakes_cci_id:                 int) -> list[pd.DataFrame]:
    dfs = []

    for lakes_cci_ecv_data_dir_path in lakes_cci_ecv_data_dir_paths:
        lakes_cci_ecv_data_csv_paths = sorted(lakes_cci_ecv_data_dir_path.glob('*.csv'))
        lakes_cci_ecv_data_data      = [(pd.read_csv(lakes_cci_ecv_data_csv_path, 
                                                     index_col='id')
                                            .loc[lakes_cci_id]) for lakes_cci_ecv_data_csv_path in lakes_cci_ecv_data_csv_paths]

        dfs.append(pd.DataFrame(lakes_cci_ecv_data_data).reset_index(drop=True))

    return dfs


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog='view_all_low_smoke_years_and_one_high_smoke_year.py',
                                     usage='%(prog)s [options]', 
                                     description='''Produces a
                                                 time-series
                                                 visualisation of a
                                                 Lakes ECV for a single
                                                 lake. The lake-smoke
                                                 years with the highest
                                                 "count of smoke days"
                                                 value is considered the
                                                 "high smoke year".
                                                 Lake-smoke years whose
                                                 "count of smoke days"
                                                 is less than or equal
                                                 to
                                                 `COUNT_OF_SMOKE_DAYS_LOWER_BOUND`
                                                 are considered "low
                                                 smoke years".''')

    # Positional arguments
    add_argument_lakes_cci_id(parser)
    add_argument_lakes_cci_ecv(parser)
    add_argument_lakes_cci_measure(parser)
    add_argument_lakes_cci_ecv_data_dir_path(parser)
    add_argument_lakes_cci_count_of_smoke_days_csv_path(parser)
    add_argument_lakes_cci_smoke_days_csv_path(parser)
    
    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    # If `args.lakes_cci_ecv` is not in `LAKES_CCI_ECVS`, return with
    # `RETURN_FAILURE`
    if not argument_lakes_cci_ecv_is_in_lakes_cci_ecvs(args.lakes_cci_ecv, 
                                                        loud=True):
        return RETURN_FAILURE

    # If `args.lakes_cci_measure` is not in `LAKES_CCI_MEASURES`, return with
    # `RETURN_FAILURE`
    if not argument_lakes_cci_measure_is_in_lakes_cci_measures(args.lakes_cci_measure, 
                                                                loud=True):
        return RETURN_FAILURE
    
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

    # If `args.lakes_cci_smoke_days_csv_path` does not exist, return
    # with `RETURN_FAILURE`
    if not argument_lakes_cci_smoke_days_csv_path_exists(args.lakes_cci_smoke_days_csv_path, 
                                                         loud=True):
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    # 1. Load `lakes_cci_count_of_smoke_days.csv` (/output produced by
    #    `query_lakes_cci_count_of_smoke_days.sql`) and
    #    `lakes_cci_smoke_days.csv` (/output produced by
    #    `query_lakes_cci_smoke_days.sql`)
    lakes_cci_count_of_smoke_days_csv = pd.read_csv(args.lakes_cci_count_of_smoke_days_csv_path, 
                                                    index_col='lakes_cci_id')
    lakes_cci_smoke_days_csv          = pd.read_csv(args.lakes_cci_smoke_days_csv_path)
    
    # 2. Determine high smoke year and low smoke years
    low_smoke_years = [year 
                       for (year, 
                            count_of_smoke_days) 
                       in (lakes_cci_count_of_smoke_days_csv.loc[args.lakes_cci_id]
                                                            .items()) 
                       if count_of_smoke_days <= COUNT_OF_SMOKE_DAYS_LOWER_BOUND]
    high_smoke_year = (lakes_cci_count_of_smoke_days_csv.loc[args.lakes_cci_id]
                                                        .idxmax())

    # 2. Create paths to ecv data directories. 
    low_smoke_year_dir_paths  = [pathlib.Path(args.lakes_cci_ecv_data_dir_path / f'{year}_3x3') 
                                 for year 
                                 in low_smoke_years]
    high_smoke_year_dir_paths = [pathlib.Path(args.lakes_cci_ecv_data_dir_path / f'{year}_3x3') 
                                 for year 
                                 in [high_smoke_year]]
    
    # 3. Create dataframes from ecv data directories (one dataframe
    #    represents one year)
    low_smoke_year_dataframes  = dfs(low_smoke_year_dir_paths, 
                                     args.lakes_cci_id)
    high_smoke_year_dataframes = dfs(high_smoke_year_dir_paths, 
                                     args.lakes_cci_id)
    
    # 4. Remove excess columns from dataframes
    low_smoke_year_dataframes = [dataframe[[f'{args.lakes_cci_ecv}_{args.lakes_cci_measure}']] 
                                 for dataframe 
                                 in low_smoke_year_dataframes]
    high_smoke_year_dataframes = [dataframe[[f'{args.lakes_cci_ecv}_{args.lakes_cci_measure}']] 
                                 for dataframe 
                                 in high_smoke_year_dataframes]
    
    # 5. Add index column to dataframes (allows us to pass around the
    #    index column for plotting)
    low_smoke_year_dataframes = [dataframe.reset_index() 
                                 for dataframe 
                                 in low_smoke_year_dataframes]
    high_smoke_year_dataframes = [dataframe.reset_index() 
                                 for dataframe 
                                 in high_smoke_year_dataframes]
    
    # 6. Concatenate dataframes (allows us to include multiple
    #    dataframes in the sample set for our general additive models
    #    (GAMs))
    low_smoke_years_dataframe  = pd.concat(low_smoke_year_dataframes, 
                                           ignore_index=True)
    high_smoke_years_dataframe = pd.concat(high_smoke_year_dataframes, 
                                           ignore_index=True)

    # low_smoke_years_dataframe[f'{args.lakes_cci_ecv}_{args.lakes_cci_measure}']  = low_smoke_years_dataframe[f'{args.lakes_cci_ecv}_{args.lakes_cci_measure}'].apply(lambda x: x - 273.15)
    # high_smoke_years_dataframe[f'{args.lakes_cci_ecv}_{args.lakes_cci_measure}'] = high_smoke_years_dataframe[f'{args.lakes_cci_ecv}_{args.lakes_cci_measure}'].apply(lambda x: x - 273.15)

    # 7. GAM!
    high_smoke_years_gam = fit(high_smoke_years_dataframe, 
                                args.lakes_cci_ecv, 
                                args.lakes_cci_measure)
    low_smoke_years_gam  = fit(low_smoke_years_dataframe, 
                               args.lakes_cci_ecv, 
                               args.lakes_cci_measure)

    # 8. Plot
    _, ax       = plt.subplots()
    ax_histplot = ax.twinx()

    sns.scatterplot(data=low_smoke_years_dataframe,
                    x='index',
                    y=f'{args.lakes_cci_ecv}_{args.lakes_cci_measure}',
                    ax=ax,
                    alpha=0.5,
                    edgecolor='none',
                    color='grey')
    low_smoke_years_X = np.linspace(low_smoke_years_dataframe['index'].min(), 
                                    low_smoke_years_dataframe['index'].max(), 
                                    low_smoke_years_dataframe['index'].max())
    ax.plot(low_smoke_years_X, 
            low_smoke_years_gam.predict(low_smoke_years_X), 
            color='grey',
            label=f'Low smoke years: {low_smoke_years}')
    
    sns.scatterplot(data=high_smoke_years_dataframe,
                    x='index',
                    y=f'{args.lakes_cci_ecv}_{args.lakes_cci_measure}',
                    ax=ax,
                    alpha=0.5,
                    edgecolor='none',
                    color='blue')
    high_smoke_years_X = np.linspace(high_smoke_years_dataframe['index'].min(), 
                                     high_smoke_years_dataframe['index'].max(),
                                     high_smoke_years_dataframe['index'].max())
    ax.plot(high_smoke_years_X, 
            high_smoke_years_gam.predict(high_smoke_years_X), 
            color='blue',
            label=f'High smoke year: {high_smoke_year}')

    sns.histplot(x=lakes_cci_smoke_days_csv.day, 
                 bins=np.arange(1, 
                                366), 
                 ax=ax_histplot, 
                 color='grey', 
                 alpha=0.25, 
                 linewidth=0.00)
    
    ax.set_xlabel('Day', 
                  fontsize=14)
    ax.set_ylabel('_ (_)', 
                  fontsize=14)
    ax.grid(True, 
            alpha=0.25)
    ax.legend()
    ax_histplot.set_xlim(1, 
                         366)
    ax_histplot.set_ylim(0, 
                         1)
    ax_histplot.set_axis_off()

    plt.title(f'_ ({args.lakes_cci_id}): Mean {args.lakes_cci_ecv} Measurements', 
              fontsize=18)
    plt.show()

    return RETURN_SUCCESS
   # ==================================================================================================


if __name__ == '__main__':
    sys.exit(main())