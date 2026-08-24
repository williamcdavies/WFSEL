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
from lib.io.vars            import (RETURN_FAILURE, 
                                    RETURN_SUCCESS)
from lib.esacci_lakes.utils import (add_argument_esacci_lakes_counts_of_smoke_days_csv_path, 
                                    add_argument_esacci_lakes_data_dir_path, 
                                    add_argument_esacci_lakes_id, 
                                    add_argument_esacci_lakes_smoke_days_csv_path,
                                    add_argument_esacci_lakes_variable, 
                                    argument_esacci_lakes_counts_of_smoke_days_csv_path_exists, 
                                    argument_esacci_lakes_data_dir_path_exists, 
                                    argument_esacci_lakes_smoke_days_csv_path_exists, 
                                    argument_esacci_lakes_variable_is_in_esacci_lakes_variables)
from lib.esacci_lakes.vars  import (COUNT_OF_SMOKE_DAYS_LOWER_BOUND, 
                                    COUNT_OF_SMOKE_DAYS_UPPER_BOUND, 
                                    ESACCI_LAKES_VARIABLES)


PROG='view_all_low_smoke_years_and_one_high_smoke_year.py'


def fit(df:                    pd.DataFrame, 
        esacci_lakes_variable: str) -> LinearGAM:
    df_nonan = df.dropna(subset=[f'{esacci_lakes_variable}_mean'])
    X        = df_nonan['index'].values
    y        = df_nonan[f'{esacci_lakes_variable}_mean'].values

    return LinearGAM(s(0)).fit(X, y) # type: ignore[arg-type]


def dfs(esacci_lakes_data_dir_paths: list[pathlib.Path], 
        esacci_lakes_id:             int) -> list[pd.DataFrame]:
    dfs = []

    for esacci_lakes_data_dir_path in esacci_lakes_data_dir_paths:
        esacci_lakes_data_csv_paths = sorted(esacci_lakes_data_dir_path.glob('*.csv'))
        esacci_lakes_data           = [(pd.read_csv(esacci_lakes_data_csv_path, 
                                                     index_col='id')
                                            .loc[esacci_lakes_id]) for esacci_lakes_data_csv_path in esacci_lakes_data_csv_paths]

        dfs.append(pd.DataFrame(esacci_lakes_data).reset_index(drop=True))

    return dfs


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog=f'{PROG}',
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
    add_argument_esacci_lakes_counts_of_smoke_days_csv_path(parser)
    add_argument_esacci_lakes_data_dir_path(parser)
    add_argument_esacci_lakes_id(parser)
    add_argument_esacci_lakes_smoke_days_csv_path(parser)
    add_argument_esacci_lakes_variable(parser)
    
    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not argument_esacci_lakes_counts_of_smoke_days_csv_path_exists(args.esacci_lakes_counts_of_smoke_days_csv_path, 
                                                                      loud=True):
        return RETURN_FAILURE

    if not argument_esacci_lakes_data_dir_path_exists(args.esacci_lakes_data_dir_path, 
                                                      loud=True):
        return RETURN_FAILURE

    if not argument_esacci_lakes_smoke_days_csv_path_exists(args.esacci_lakes_smoke_days_csv_path, 
                                                            loud=True):
        return RETURN_FAILURE
    
    if not argument_esacci_lakes_variable_is_in_esacci_lakes_variables(args.esacci_lakes_variable, 
                                                                       loud=True):
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    esacci_lakes_counts_of_smoke_days_csv = pd.read_csv(args.esacci_lakes_counts_of_smoke_days_csv_path, 
                                                        index_col='esacci_lakes_id')
    esacci_lakes_smoke_days_csv           = pd.read_csv(args.esacci_lakes_smoke_days_csv_path)
    low_smoke_years                       = [year for (year, count_of_smoke_days) in (esacci_lakes_counts_of_smoke_days_csv.loc[args.esacci_lakes_id]
                                                                                                                           .items()) if count_of_smoke_days <= COUNT_OF_SMOKE_DAYS_LOWER_BOUND]
    high_smoke_year                       = (esacci_lakes_counts_of_smoke_days_csv.loc[args.esacci_lakes_id]
                                                                                  .idxmax())
    low_smoke_year_dataframes             = [dataframe[[f'{args.esacci_lakes_variable}_mean']].reset_index() for dataframe in dfs([pathlib.Path(args.esacci_lakes_data_dir_path / f'{year}') for year in low_smoke_years], 
                                                                                                                                  args.esacci_lakes_id)]
    high_smoke_year_dataframes            = [dataframe[[f'{args.esacci_lakes_variable}_mean']].reset_index() for dataframe in dfs([pathlib.Path(args.esacci_lakes_data_dir_path / f'{year}') for year in [high_smoke_year]], 
                                                                                                                                  args.esacci_lakes_id)]
    low_smoke_years_dataframe             = pd.concat(low_smoke_year_dataframes, 
                                                      ignore_index=True)
    high_smoke_years_dataframe            = pd.concat(high_smoke_year_dataframes, 
                                                      ignore_index=True)

    low_smoke_years_dataframe[f'{args.esacci_lakes_variable}_mean']  = low_smoke_years_dataframe[f'{args.esacci_lakes_variable}_mean'].apply(lambda x: x - 273.15)
    high_smoke_years_dataframe[f'{args.esacci_lakes_variable}_mean'] = high_smoke_years_dataframe[f'{args.esacci_lakes_variable}_mean'].apply(lambda x: x - 273.15)

    low_smoke_years_gam  = fit(low_smoke_years_dataframe, 
                               args.esacci_lakes_variable)
    high_smoke_years_gam = fit(high_smoke_years_dataframe, 
                               args.esacci_lakes_variable)

    _, ax       = plt.subplots()
    ax_histplot = ax.twinx()

    sns.scatterplot(data=low_smoke_years_dataframe,
                    x='index',
                    y=f'{args.esacci_lakes_variable}_mean', 
                    ax=ax,
                    alpha=0.25,
                    edgecolor='none',
                    color='grey')
    low_smoke_years_nonan = low_smoke_years_dataframe.dropna(subset=[f'{args.esacci_lakes_variable}_mean'])
    low_smoke_years_X     = np.linspace(low_smoke_years_nonan['index'].min(), 
                                        low_smoke_years_nonan['index'].max(), 
                                        300)
    ax.plot(low_smoke_years_X, 
            low_smoke_years_gam.predict(low_smoke_years_X), 
            color='grey',
            label=f'Low smoke years: {low_smoke_years}')
    
    sns.scatterplot(data=high_smoke_years_dataframe,
                    x='index',
                    y=f'{args.esacci_lakes_variable}_mean', 
                    ax=ax,
                    alpha=0.25,
                    edgecolor='none',
                    color='orange')
    high_smoke_years_nonan = high_smoke_years_dataframe.dropna(subset=[f'{args.esacci_lakes_variable}_mean'])
    high_smoke_years_X     = np.linspace(high_smoke_years_nonan['index'].min(), 
                                         high_smoke_years_nonan['index'].max(), 
                                         300)
    ax.plot(high_smoke_years_X, 
            high_smoke_years_gam.predict(high_smoke_years_X), 
            color='orange',
            label=f'High smoke year: {high_smoke_year}')

    sns.histplot(x=esacci_lakes_smoke_days_csv.day, 
                 bins=np.arange(1, 
                                366), 
                 ax=ax_histplot, 
                 color='grey', 
                 alpha=0.25, 
                 linewidth=0.00)
    
    ax.set_xlabel('Day', 
                  fontsize=14)
    ax.set_ylabel(f'{ESACCI_LAKES_VARIABLES[args.esacci_lakes_variable].long_name} ({ESACCI_LAKES_VARIABLES[args.esacci_lakes_variable].units})', 
                  fontsize=14)
    ax.grid(True, 
            alpha=0.25)
    ax.legend()
    ax_histplot.set_xlim(1, 
                         366)
    ax_histplot.set_ylim(0, 
                         1)
    ax_histplot.set_axis_off()

    plt.title(f'_ ({args.esacci_lakes_id}): Mean {args.esacci_lakes_variable} Measurements', 
              fontsize=18)
    plt.show()

    return RETURN_SUCCESS
   # ==================================================================================================


if __name__ == '__main__':
    sys.exit(main())