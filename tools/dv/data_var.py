r"""
data_var.py

Description: 
   The purpose of this file is to produce a time-series visualisation of
   a Lakes ECV for a single lake. 

Usage:
   python data_var.py <target_csv_dir> <target_csv>

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
LAKE_IDX       = 5
DATA_VAR       = 'chla_mean'
X_LABEL        = 'Day'
Y_LABEL        = 'Concentration of Chlorophyll-a (mg.m-3)'
T_LABEL        = 'Lake Erie: Mean Chlorophyll-a Measurements of 3x3 Centroid (2023)'


# ===================================================================================================
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
csv_files                  = list(target_csv_dir.glob('*.csv'))

# > [!note]
# > It is assumed that `target_dir` does not contain any
# > subdirectories that would contain any target csvs.
# ===================================================================================================

# ===================================================================================================
data_var_data = []

# For each csv file in `csv_files` ...
for csv_file in csv_files:
    # Append the Lake `DATA_VAR` value to `data_var_data`
    data_var_data.append(pd.read_csv(csv_file)
                         .at[LAKE_IDX, 
                             DATA_VAR])

data_var_x       = np.arange(1, 
                             len(data_var_data) + 1)
data_var_y       = np.array(data_var_data)
data_var_b       = np.isnan(data_var_y)
data_var_x_nonan = data_var_x[~data_var_b]
data_var_y_nonan = data_var_y[~data_var_b]

if len(data_var_x_nonan) == 0 or len(data_var_y) == 0:
    print(f'fatal: no data: {LAKE_IDX}')
        
    sys.exit(RETURN_FAILURE)

# > [!note] 
# > `data_var_x` is 1-indexed to prevent misalignment between
# > regression and histogram plots.

smoke_data = (pd.read_csv(target_csv)
              .drop_duplicates('day'))
# ===================================================================================================

# ===================================================================================================
_, ax_regplot = plt.subplots()
ax_histplot   = ax_regplot.twinx()

sns.regplot(x=data_var_x_nonan,
            y=data_var_y_nonan, 
            ax=ax_regplot,
            order=4,
            color='blue')
ax_regplot.set_xlim(1,
                    len(data_var_data))
ax_regplot.set_ylim(0,
                    max(data_var_y_nonan))
ax_regplot.set_xlabel(X_LABEL)
ax_regplot.set_ylabel(Y_LABEL)
ax_histplot.set_axis_on()

sns.histplot(x=smoke_data.day, 
             bins=data_var_x,
             ax=ax_histplot,
             color='grey',
             alpha=0.25,
             linewidth=0.00)
ax_histplot.set_xlim(1,
                     len(data_var_data))
ax_histplot.set_ylim(0,
                     1)
ax_histplot.set_xlabel(X_LABEL)
ax_histplot.set_ylabel('')
ax_histplot.set_axis_off()

sns.set_style()
plt.title(T_LABEL)
plt.show()
# ===================================================================================================