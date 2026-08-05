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
from lib.lakes_cci.vars import (ECVS, 
                                MEASURES,
                                LOWER_QUARTILE,
                                UPPER_QUARTILE)
from lib.io.vars        import (RETURN_FAILURE, 
                                RETURN_SUCCESS)


def fit(df: pd.DataFrame, 
        ecv: str, 
        measure: str) -> LinearGAM:
    df_nonan = df.dropna(subset=[f'{ecv}_{measure}'])
    X        = df_nonan['index'].values
    y        = df_nonan[f'{ecv}_{measure}'].values

    return LinearGAM(s(0)).fit(X, y)


def load(dir_paths: list[pathlib.Path], 
         lakes_cci_id: int) -> list[pd.DataFrame]:
    dataframes = []

    for dir_path in dir_paths:
        csv_paths = sorted(dir_path.glob('*.csv'))
        data      = [(pd.read_csv(csv_path, 
                                  index_col='id')
                        .loc[lakes_cci_id]) for csv_path in csv_paths]

        dataframes.append(pd.DataFrame(data).reset_index(drop=True))

    return dataframes 


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog='view_all_low_smoke_years_and_one_high_smoke_year.py',
                                     usage='%(prog)s [options]', 
                                     description='''''')

    # Positional arguments
    parser.add_argument('lakes_cci_id', 
                        type=int,
                        help='''CCI_lakeid as provided by ESA Lakes
                             Climate Change Initiative (Lakes_cci): Lake
                             products, Version 3.0''')
    parser.add_argument('ecv',
                        type=str,
                        help=f'''one of {ECVS}''')
    parser.add_argument('measure',
                        type=str,
                        help=f'''one of {MEASURES}''')
    parser.add_argument('ecv_data_dir_path',
                        type=pathlib.Path,
                        help=f'''path to Lakes ECV data directory as
                              produced by main.py''')
    parser.add_argument('count_of_smoke_days_csv_path',
                        type=pathlib.Path,
                        help=f'''path to smoke days data csv as produced
                              by
                              tools/db/query_count_of_smoke_days.sql''')
    parser.add_argument('smoke_days_csv_path',
                            type=pathlib.Path,
                            help=f'''path to smoke days csv as produced by
                                  tools/db/query_smoke_days.sql''')

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    # If `args.count_of_smoke_days_csv_path` does not exist, return with
    # `RETURN_FAILURE`
    if not args.count_of_smoke_days_csv_path.exists():
        print(f'''error: argument count_of_smoke_days_csv_path: no such
               file or directory:
               {args.count_of_smoke_days_csv_path}''')
        
        return RETURN_FAILURE

    # If `args.smoke_days_csv_path` does not exist, return with
    # `RETURN_FAILURE`
    if not args.smoke_days_csv_path.exists():
        print(f'''error: argument smoke_days_csv_path: no such file or
                directory: {args.smoke_days_csv_path}''')
        
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    # 1. Load `count_of_smoke_days.csv` (/output produced by
    #    `query_count_of_smoke_days.sql`) and `smoke_days.csv` (/output
    #    produced by `query_smoke_days.sql`)
    count_of_smoke_days_csv = pd.read_csv(args.count_of_smoke_days_csv_path, 
                                          index_col='lakes_cci_id')
    smoke_days_csv          = pd.read_csv(args.smoke_days_csv_path)
    
    # 2. Determine high smoke year and low smoke years
    low_smoke_years = [year 
                       for (year, 
                            count_of_smoke_days) 
                       in (count_of_smoke_days_csv.loc[args.lakes_cci_id]
                                                  .items()) 
                       if count_of_smoke_days <= LOWER_QUARTILE]
    high_smoke_year = (count_of_smoke_days_csv.loc[args.lakes_cci_id]
                                              .idxmax())

    # 2. Create paths to ecv data directories. 
    low_smoke_year_dir_paths  = [pathlib.Path(args.ecv_data_dir_path / f'{year}_3x3') 
                                 for year 
                                 in low_smoke_years]
    high_smoke_year_dir_paths = [pathlib.Path(args.ecv_data_dir_path / f'{year}_3x3') 
                                 for year 
                                 in [high_smoke_year]]
    
    # 3. Create dataframes from ecv data directories (one dataframe
    #    represents one year)
    low_smoke_year_dataframes  = load(low_smoke_year_dir_paths, 
                                      args.lakes_cci_id)
    high_smoke_year_dataframes = load(high_smoke_year_dir_paths, 
                                      args.lakes_cci_id)
    
    # 4. Remove excess columns from dataframes
    low_smoke_year_dataframes = [dataframe[[f'{args.ecv}_{args.measure}']] 
                                 for dataframe 
                                 in low_smoke_year_dataframes]
    high_smoke_year_dataframes = [dataframe[[f'{args.ecv}_{args.measure}']] 
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

    # low_smoke_years_dataframe[f'{args.ecv}_{args.measure}']  = low_smoke_years_dataframe[f'{args.ecv}_{args.measure}'].apply(lambda x: x - 273.15)
    # high_smoke_years_dataframe[f'{args.ecv}_{args.measure}'] = high_smoke_years_dataframe[f'{args.ecv}_{args.measure}'].apply(lambda x: x - 273.15)

    # 7. GAM!
    high_smoke_years_gam = fit(high_smoke_years_dataframe, 
                                args.ecv, 
                                args.measure)
    low_smoke_years_gam  = fit(low_smoke_years_dataframe, 
                               args.ecv, 
                               args.measure)

    # 8. Plot
    _, ax       = plt.subplots()
    ax_histplot = ax.twinx()

    sns.scatterplot(data=low_smoke_years_dataframe,
                    x='index',
                    y=f'{args.ecv}_{args.measure}',
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
                    y=f'{args.ecv}_{args.measure}',
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

    sns.histplot(x=smoke_days_csv.day, 
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

    plt.title(f'_ ({args.lakes_cci_id}): Mean {args.ecv} Measurements', 
              fontsize=18)
    plt.show()

    return RETURN_SUCCESS
   # ==================================================================================================


if __name__ == '__main__':
    sys.exit(main())