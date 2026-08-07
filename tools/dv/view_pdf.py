r'''
view_ecv.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import pathlib
import sys

# Related Third-party Imports
import matplotlib.pyplot
import numpy
import pandas
import seaborn

# Local Application/Library Specific Imports
from lib.io.vars import (RETURN_FAILURE, 
                         RETURN_SUCCESS)


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog='view_pdf.py',
                                     usage='%(prog)s [options]', 
                                     description='''Produces a
                                                 distribution
                                                 visualisation of the
                                                 "count of smoke days"
                                                 for all lake-smoke
                                                 years from [2011,
                                                 2023].''')

    # Positional arguments
    parser.add_argument('lakes_cci_id_count_of_smoke_days_csv_path', 
                        type=pathlib.Path,
                        help=f'''path to smoke days data csv as produced
                              by
                              tools/db/query_lakes_cci_id_count_of_smoke_days.sql''')
    
    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    # If `args.lakes_cci_id_count_of_smoke_days_csv_path` does not exist, return with
    # `RETURN_FAILURE`
    if not args.lakes_cci_id_count_of_smoke_days_csv_path.exists():
        print(f'''error: argument
               lakes_cci_id_count_of_smoke_days_csv_path: no such file
               or directory:
               {args.lakes_cci_id_count_of_smoke_days_csv_path}''')
        
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    wide_df = pandas.read_csv(args.lakes_cci_id_count_of_smoke_days_csv_path)
    long_df = wide_df.melt(id_vars='lakes_cci_id', 
                           var_name='year', 
                           value_name='count_of_smoke_days')
    p25 = numpy.percentile(long_df['count_of_smoke_days'], 
                           25)
    p75 = numpy.percentile(long_df['count_of_smoke_days'], 
                           75)
    
    # fig, (ax1, ax2) = matplotlib.pyplot.subplots(
    #     nrows=2,
    #     sharex=True,
    #     gridspec_kw={'height_ratios': (0.10, 0.90)}
    # )

    fig, ax2 = matplotlib.pyplot.subplots()

    # seaborn.boxplot(data=long_df,
    #                 x='count_of_smoke_days',
    #                 color='black',
    #                 fill=False,
    #                 ax=ax1)    
    seaborn.histplot(data=long_df,
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
    # seaborn.kdeplot(data=long_df,
    #                 x='count_of_smoke_days',
    #                 color='black',
    #                 ax=ax2)

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
    
    matplotlib.pyplot.show()

    return RETURN_SUCCESS
   # ==================================================================================================


if __name__ == '__main__':
    sys.exit(main())