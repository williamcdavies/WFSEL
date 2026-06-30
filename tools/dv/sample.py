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


# If argument count is not equal to 2, exit with `RETURN_FAILURE`
if len(sys.argv) != 2:
    print(f'fatal: unexpected argument count: {sys.argv}')

    sys.exit(RETURN_FAILURE)

target_dir = pathlib.Path(sys.argv[1])

# If `target_dir` does not exist, exit with `RETURN_FAILURE`
if not target_dir.exists():
    print(f'fatal: no such file or directory: {sys.argv[1]}')

    sys.exit(RETURN_FAILURE)

csv_files = list(target_dir.glob('*.csv'))

# > [!note]
# > It is assumed that `target_dir` does not contain any subdirectories
# > that would contain any target files. For this behaviour, replace
# > `pathlib.Path.glob()` with `pathlib.Path.rglob()`.

sns.set_style()
sns.set_palette('pastel')

for i in range(0, 5):
    data = []

    for csv_file in csv_files:
        data.append(pd.read_csv(csv_file).at[i, 'chla_mean'])

    x = np.arange(1, len(data) + 1)
    y = np.array(data)

    b = np.isnan(y)

    x_nonan = x[~b]
    y_nonan = y[~b]

    sns.regplot(x=x_nonan, 
                y=y_nonan,
                scatter=False,
                order=2,
                label=f'{i + 1}')

plt.yscale('log')
plt.legend()
plt.show()