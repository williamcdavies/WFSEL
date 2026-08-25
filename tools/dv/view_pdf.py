r'''
view_pdf.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import sys

# Related Third-party Imports
import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd
import seaborn           as sns

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils import (add_argument_esacci_lakes_counts_of_smoke_days_csv_path, 
                                    argument_esacci_lakes_counts_of_smoke_days_csv_path_exists)
from lib.io.vars            import (RETURN_FAILURE, 
                                    RETURN_SUCCESS)


PROG='view_pdf.py'


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog=f'{PROG}',
                                     usage='%(prog)s [options]', 
                                     description='''Produces a distribution visualisation of the "count of smoke days" for all lake-smoke years from [2011, 2023].''')

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
    wide_df = pd.read_csv(args.esacci_lakes_counts_of_smoke_days_csv_path)
    long_df = wide_df.melt(id_vars='esacci_lakes_id', 
                           var_name='year', 
                           value_name='count_of_smoke_days')
    p25 = np.percentile(long_df['count_of_smoke_days'], 
                        25)
    p75 = np.percentile(long_df['count_of_smoke_days'], 
                        75)
    
    # fig, (ax1, ax2) = plt.subplots(
    #     nrows=2,
    #     sharex=True,
    #     gridspec_kw={'height_ratios': (0.10, 0.90)}
    # )

    fig, ax2 = plt.subplots()

    # sns.boxplot(data=long_df,
    #             x='count_of_smoke_days',
    #             color='black',
    #             fill=False,
    #             ax=ax1)    
    sns.histplot(data=long_df,
                 x='count_of_smoke_days',
                #  hue='year',
                 stat='density',
                 binwidth=5,
                 binrange=(0, 365),
                 cumulative=True,
                #  multiple='stack',
                 element='step',
                 fill=False,
                 color='black',
                 ax=ax2)
    # sns.kdeplot(data=long_df,
    #             x='count_of_smoke_days',
    #             color='black',
    #             ax=ax2)

    ax2.axvline(p25, 
                color='red', 
                linestyle='--', 
                alpha=0.75, 
                label=f'25th Percentile: {p25:.0f}')
    ax2.axvline(p75, 
                color='blue', 
                linestyle='--', 
                alpha=0.75, 
                label=f'75th Percentile: {p75:.0f}')
    ax2.legend()
    
    # ax1.grid(True, alpha=0.25)
    ax2.grid(True, alpha=0.25)
    
    ax2.set_xlabel('Number of Smoke Days', 
                   fontsize=16,
                   labelpad=15)
    ax2.set_ylabel('Cumulative Percentage of Observations', 
                   fontsize=16,
                   labelpad=15)
    
    fig.suptitle('Cumulative Distribution of North American Lakes by Number of Smoke Days', 
                 fontsize=18, 
                 y=0.95)
    
    plt.show()

    return RETURN_SUCCESS
   # ==================================================================================================


if __name__ == '__main__':
    sys.exit(main())