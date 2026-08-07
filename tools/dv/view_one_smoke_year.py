r'''
view_one_smoke_year.py

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
from lib.io.vars         import (RETURN_FAILURE, 
                                 RETURN_SUCCESS)
from lib.lakes_cci.utils import (add_argument_lakes_cci_ecv_data_dir_path, 
                                 add_argument_lakes_cci_ecv, 
                                 add_argument_lakes_cci_id, 
                                 add_argument_lakes_cci_measure, 
                                 add_argument_lakes_cci_smoke_days_csv_path, 
                                 argument_lakes_cci_ecv_data_dir_path_exists, 
                                 argument_lakes_cci_ecv_is_in_lakes_cci_ecvs, 
                                 argument_lakes_cci_measure_is_in_lakes_cci_measures, 
                                 argument_lakes_cci_smoke_days_csv_path_exists)
from lib.lakes_cci.vars  import (COUNT_OF_SMOKE_DAYS_LOWER_BOUND,
                                 COUNT_OF_SMOKE_DAYS_UPPER_BOUND)


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog='view_one_smoke_year.py',
                                     usage='%(prog)s [options]', 
                                     description='''Produces a
                                                 time-series
                                                 visualisation of a
                                                 Lakes ECV for a single
                                                 lake.''')

    # Positional arguments
    add_argument_lakes_cci_id(parser)
    add_argument_lakes_cci_ecv(parser)
    add_argument_lakes_cci_measure(parser)
    add_argument_lakes_cci_ecv_data_dir_path(parser)
    add_argument_lakes_cci_smoke_days_csv_path(parser)

    # Optional arguments
    parser.add_argument('--x_label', 
                        default='',
                        type=str,
                        help=f'''x-axis label''')
    parser.add_argument('--y_label', 
                        default='',
                        type=str,
                        help=f'''y-axis label''')
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

    # If `args.lakes_cci_smoke_days_csv_path` does not exist, return
    # with `RETURN_FAILURE`
    if not argument_lakes_cci_smoke_days_csv_path_exists(args.lakes_cci_smoke_days_csv_path, 
                                                            loud=True):
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    # Read `args.lakes_cci_ecv_data_dir_path` into
    # `lakes_cci_ecv_data_csv_paths`
    lakes_cci_ecv_data_csv_paths = sorted(args.lakes_cci_ecv_data_dir_path.glob('*.csv'))

    # > [!note] 
    # > It is assumed that `args.lakes_cci_ecv_data_dir_path` does not
    # > contain any subdirectories that would contain any target csvs.
    # > i.e., `pathlib.Path.glob()` is not recursive

    lakes_cci_ecv_data = []

    # For each `lakes_cci_ecv_data_csv_path` in
    # `lakes_cci_ecv_data_csv_paths` ...
    for lakes_cci_ecv_data_csv_path in lakes_cci_ecv_data_csv_paths:
        # Read `lakes_cci_ecv_data_csv_path` into
        # `lakes_cci_ecv_data_csv`
        lakes_cci_ecv_data_csv = pd.read_csv(lakes_cci_ecv_data_csv_path)
        
        # Append the Lakes ECV value at `[lakes_cci_ecv_data_csv['id']
        # == args.lakes_cci_id,
        # f'{args.lakes_cci_ecv}_{args.lakes_cci_measure}']` to
        # `ecv_data`
        lakes_cci_ecv_data.append(lakes_cci_ecv_data_csv.loc[lakes_cci_ecv_data_csv['id'] == args.lakes_cci_id, 
                                                             f'{args.lakes_cci_ecv}_{args.lakes_cci_measure}'].item()) # type: ignore[attr-defined]

    lakes_cci_ecv_x       = np.arange(1, 
                            len(lakes_cci_ecv_data) + 1)
    lakes_cci_ecv_y       = np.array(lakes_cci_ecv_data)
    lakes_cci_ecv_b       = np.isnan(lakes_cci_ecv_y)
    lakes_cci_ecv_x_nonan = lakes_cci_ecv_x[~lakes_cci_ecv_b]
    lakes_cci_ecv_y_nonan = lakes_cci_ecv_y[~lakes_cci_ecv_b]

    # > [!note] 
    # > `lakes_cci_ecv_x` is 1-indexed to prevent misalignment between
    # > regression and histogram plots.

    # Read `args.lakes_cci_smoke_days_csv_path` into `lakes_cci_smoke_days_csv``
    lakes_cci_smoke_days_csv = (pd.read_csv(args.lakes_cci_smoke_days_csv_path)
                                  .drop_duplicates('day'))

    _, ax_regplot = plt.subplots()
    ax_histplot   = ax_regplot.twinx()

    sns.regplot(x=lakes_cci_ecv_x_nonan,
                y=lakes_cci_ecv_y_nonan, 
                ax=ax_regplot,
                order=4,
                color=args.reg_colour)
    ax_regplot.set_xlim(1,
                        len(lakes_cci_ecv_data))
    ax_regplot.set_ylim(0,
                        0)
    ax_regplot.set_xlabel(args.x_label)
    ax_regplot.set_ylabel(args.y_label)
    ax_histplot.set_axis_on()

    sns.histplot(x=lakes_cci_smoke_days_csv.day, 
                bins=lakes_cci_ecv_x,
                ax=ax_histplot,
                color=args.hist_colour,
                alpha=0.25,
                linewidth=0.00)
    ax_histplot.set_xlim(1,
                        len(lakes_cci_ecv_data))
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