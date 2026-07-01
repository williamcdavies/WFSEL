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

data = []

for csv_file in csv_files:
    data.append(pd.read_csv(csv_file).at[0, 'chla_mean'])

x = np.arange(1, len(data) + 1)
y = np.array(data)

b = np.isnan(y)

x_nonan = x[~b]
y_nonan = y[~b]

sns.regplot(x=x_nonan, 
            y=y_nonan,
            order=2)

plt.yscale('log')
plt.xlim(1, 365)
plt.ylim(0.01, 10)
plt.xlabel('Day')
plt.ylabel("Concentration of Chlorophyll-A (mg/m^3)")
plt.title("Lake Superior: Mean Chlorophyll-A Measurements")
plt.show()