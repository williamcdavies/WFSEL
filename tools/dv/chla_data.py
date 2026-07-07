r"""
chla_data.py

Description: 
   The purpose of this file is to produce a time-series visualisation of
   mean concentration of chlorophyll-a (mg.m-3) measurements for a
   single lake. 

Usage:
   python chla_data.py <target_csv_dir> <target_csv>

Written by William Chuter-Davies
"""


# Standard Library Imports
import pathlib
import sys

# Related Third-party Imports
import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd
import seaborn           as sns

# Global Definitions
RETURN_SUCCESS = 0
RETURN_FAILURE = 1


# If argument count is not equal to 3, exit with `RETURN_FAILURE`
if len(sys.argv) != 3:
    print(f'fatal: unexpected argument count: {sys.argv}')

    sys.exit(RETURN_FAILURE)

# For each path in `sys.argv` create corresponding Path and read into
# `paths`
paths = [pathlib.Path(p) for p in sys.argv[1:]]

# For each path in `paths` ...
for path in paths:
    # If path does not exist, exit with `RETURN_FAILURE`
    if not path.exists():
        print(f'fatal: no such file or directory: {path}')
        
        sys.exit(RETURN_FAILURE)

# Read `paths` into `target_dir`, `target_csv`
target_csv_dir, target_csv = paths

csv_files = list(target_csv_dir.glob('*.csv'))

# > [!note]
# > It is assumed that `target_dir` does not contain any
# > subdirectories that would contain any target csvs.

chla_mean_data = []

# For each csv file in `csv_files`
for csv_file in csv_files:
    # Append the Lake Superior `chla_mean` value to `chla_mean_data`
    chla_mean_data.append(pd.read_csv(csv_file)
                .at[0, 
                    'chla_mean'])
    
# > [!warning]
# > `pandas.DataFrame.at` arguments should not be hard coded.

chla_mean_x       = np.arange(1, 
                              len(chla_mean_data) + 1)
chla_mean_y       = np.array(chla_mean_data)
chla_mean_b       = np.isnan(chla_mean_y)
chla_mean_x_nonan = chla_mean_x[~chla_mean_b]
chla_mean_y_nonan = chla_mean_y[~chla_mean_b]

# > [!note] 
# > `chla_mean_x` is 1-indexed to prevent misalignment between
# > regression and histogram plots.

smoke_data = (pd.read_csv(target_csv)
              .drop_duplicates('day'))

_, ax_regplot = plt.subplots()
ax_histplot   = ax_regplot.twinx()

sns.regplot(x=chla_mean_x_nonan,
            y=chla_mean_y_nonan, 
            ax=ax_regplot,
            color='green')
ax_regplot.set_xlim(1,
                    len(chla_mean_data))
ax_regplot.set_ylim(0,
                    max(chla_mean_y_nonan))
ax_regplot.set_xlabel('Day')
ax_regplot.set_ylabel('Concentration of Chlorophyll-a (mg.m-3)')
ax_histplot.set_axis_on()

sns.histplot(x=smoke_data.day, 
             bins=chla_mean_x,
             ax=ax_histplot,
             color='grey',
             alpha=0.25,
             linewidth=0.00)
ax_histplot.set_xlim(1,
                     len(chla_mean_data))
ax_histplot.set_ylim(0,
                     1)
ax_histplot.set_xlabel('Day')
ax_histplot.set_ylabel('')
ax_histplot.set_axis_off()

sns.set_style()
plt.title('Lake Superior: Mean Chlorophyll-a Measurements (2023)')
plt.show()