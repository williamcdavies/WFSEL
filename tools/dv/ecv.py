r'''
ecv.py

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

# Local Application/Library Specific Imports
from lib.esa.vars import (ECVS, 
                          MEASURES)
from lib.io.vars  import (RETURN_FAILURE, 
                          RETURN_SUCCESS)


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog='ecv.py',
                                     usage='%(prog)s [options]', 
                                     description='''Produces a
                                                 time-series
                                                 visualisation of a
                                                 Lakes ECV for a single
                                                 lake.''')

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
    parser.add_argument('smoke_days_data_csv_path',
                        type=pathlib.Path,
                        help=f'''path to smoke days data csv as produced
                              by tools/db/query_smoke_days.sql''')

    # Optional arguments
    parser.add_argument('--x_label', 
                        default='',
                        type=str,
                        help=f'''X-axis label''')
    parser.add_argument('--y_label', 
                        default='',
                        type=str,
                        help=f'''Y-axis label''')
    parser.add_argument('--t_label', 
                        default='',
                        type=str,
                        help=f'''figure title''')
    parser.add_argument('--reg_colour', 
                        default='blue',
                        type=str,
                        help=f'''regression plot colour''')
    parser.add_argument('--hist_colour', 
                        default='grey',
                        type=str,
                        help=f'''histogram plot colour''')

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
    
    # If `args.smoke_days_data_csv_path` does not exist, return with
    # `RETURN_FAILURE`
    if not args.smoke_days_data_csv_path.exists():
        print(f'''error: argument smoke_days_data_csv_path: no such file or
               directory: {args.smoke_days_data_csv_path}''')
        
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    # Read `args.ecv_data_dir_path` into `ecv_data_csv_paths`
    ecv_data_csv_paths = sorted(args.ecv_data_dir_path.glob('*.csv'))

    # > [!note]
    # > It is assumed that `args.ecv_data_dir_path` does not contain any
    # > subdirectories that would contain any target csvs. i.e.,
    # > `pathlib.Path.glob()` is not recursive

    ecv_data = []

    # For each `ecv_data_csv_path` in `ecv_data_csv_paths` ...
    for ecv_data_csv_path in ecv_data_csv_paths:
        # Read `ecv_data_csv_path` into `ecv_data_csv`
        ecv_data_csv = pd.read_csv(ecv_data_csv_path)
        
        # Append the Lakes ECV value at `[ecv_data_csv['id'] ==
        # args.lakes_cci_id, f'{args.ecv}_{args.measure}']` to
        # `ecv_data`
        ecv_data.append(ecv_data_csv.loc[ecv_data_csv['id'] == args.lakes_cci_id, 
                                         f'{args.ecv}_{args.measure}'].item()) # type: ignore[attr-defined]

    ecv_x       = np.arange(1, 
                            len(ecv_data) + 1)
    ecv_y       = np.array(ecv_data)
    ecv_b       = np.isnan(ecv_y)
    ecv_x_nonan = ecv_x[~ecv_b]
    ecv_y_nonan = ecv_y[~ecv_b]

    # > [!note] 
    # > `ecv_x` is 1-indexed to prevent misalignment between regression
    # > and histogram plots.

    # Read `smoke_days_data_csv` into `args.smoke_days_data_csv_path`
    smoke_days_data_csv = (pd.read_csv(args.smoke_days_data_csv_path)
                      .drop_duplicates('day'))

    _, ax_regplot = plt.subplots()
    ax_histplot   = ax_regplot.twinx()

    sns.regplot(x=ecv_x_nonan,
                y=ecv_y_nonan, 
                ax=ax_regplot,
                order=4,
                color=args.reg_colour)
    ax_regplot.set_xlim(1,
                        len(ecv_data))
    ax_regplot.set_ylim(0,
                        0)
    ax_regplot.set_xlabel(args.x_label)
    ax_regplot.set_ylabel(args.y_label)
    ax_histplot.set_axis_on()

    sns.histplot(x=smoke_days_data_csv.day, 
                bins=ecv_x,
                ax=ax_histplot,
                color=args.hist_colour,
                alpha=0.25,
                linewidth=0.00)
    ax_histplot.set_xlim(1,
                        len(ecv_data))
    ax_histplot.set_ylim(0,
                        1)
    ax_histplot.set_xlabel(args.x_label)
    ax_histplot.set_axis_off()

    sns.set_style()
    plt.title(args.t_label)
    plt.show()

    return RETURN_SUCCESS
   # ==================================================================================================


if __name__ == '__main__':
    sys.exit(main())