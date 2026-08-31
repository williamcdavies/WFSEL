r"""
view_all_low_smoke_years_and_all_high_smoke_years.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse import ArgumentParser
from pathlib  import Path

# Related Third-party Imports
import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd
import seaborn           as sns

from pygam import (
    LinearGAM, 
    s
)

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.argparse import (
    add_argument_esacci_lakes_id,
    add_argument_esacci_lakes_variable,
    add_argument_local_data_dir_path,
    add_argument_esacci_lakes_counts_of_distinct_start_days_csv_path,
    argument_local_data_dir_path_exists,
    argument_esacci_lakes_counts_of_distinct_start_days_csv_path_exists
)
from lib.esacci_lakes.utils.pandas   import read_esacci_lakes_counts_of_distinct_start_days_csv
from lib.esacci_lakes.vars           import (
    COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND,
    COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND,
    ESACCI_LAKES_VARIABLES
)
from lib.io.vars                     import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)

PROG = "view_all_low_smoke_years_and_all_high_smoke_years.py"


def fit(
    df: pd.DataFrame,
    esacci_lakes_variable: str,
) -> LinearGAM:
    df_nonan = df.dropna(subset=[f"{esacci_lakes_variable}_mean"])
    X        = df_nonan["index"].values
    y        = df_nonan[f"{esacci_lakes_variable}_mean"].values

    return LinearGAM(s(0)).fit(X, y)  # type: ignore


def to_dfs(
    local_data_dir_paths: list[Path],
    esacci_lakes_id: int,
) -> list[pd.DataFrame]:
    dfs = []

    for local_data_dir_path in local_data_dir_paths:
        local_data_csv_paths = sorted(local_data_dir_path.glob("*.csv"))
        local_data            = [pd.read_csv(local_data_csv_path, index_col="id").loc[esacci_lakes_id] for local_data_csv_path in local_data_csv_paths]

        dfs.append(pd.DataFrame(local_data).reset_index(drop=True))

    return dfs


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = ArgumentParser(
        prog=PROG,
        usage="%(prog)s [options]",
        description="""Produces a time-series visualisation of a Lakes ECV for a single lake. Lake-smoke years whose "count of smokedays" is greater than or equal to `COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND` are considered "high smoke years". Lake-smoke years whose "count of smoke days" is less than or equal to `COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND` are considered "low smoke years".""",
    )

    # Positional arguments
    add_argument_esacci_lakes_id(parser)
    add_argument_esacci_lakes_variable(parser)
    add_argument_local_data_dir_path(parser)
    add_argument_esacci_lakes_counts_of_distinct_start_days_csv_path(parser)

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not argument_local_data_dir_path_exists(
        args.local_data_dir_path,
        loud=True
    ):
        return RETURN_FAILURE

    if not argument_esacci_lakes_counts_of_distinct_start_days_csv_path_exists(
        args.esacci_lakes_counts_of_distinct_start_days_csv_path,
        loud=True
    ):
        return RETURN_FAILURE
    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    esacci_lakes_counts_of_distinct_start_days_df = read_esacci_lakes_counts_of_distinct_start_days_csv(args.esacci_lakes_counts_of_distinct_start_days_csv_path)

    low_smoke_years  = [
        year 
        for (year, count_of_smoke_days) 
        in esacci_lakes_counts_of_distinct_start_days_df.loc[args.esacci_lakes_id].items() if count_of_smoke_days <= COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND]
    high_smoke_years = [
        year 
        for (year, count_of_smoke_days) 
        in esacci_lakes_counts_of_distinct_start_days_df.loc[args.esacci_lakes_id].items() if count_of_smoke_days >= COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND]

    low_smoke_year_dataframes  = [
        dataframe[[f"{args.esacci_lakes_variable}_mean"]].reset_index()
        for dataframe 
        in to_dfs(
            [Path(args.local_data_dir_path / f"{year}") for year in low_smoke_years],
            args.esacci_lakes_id,
        )
    ]
    high_smoke_year_dataframes = [
        dataframe[[f"{args.esacci_lakes_variable}_mean"]].reset_index()
        for dataframe 
        in to_dfs(
            [Path(args.local_data_dir_path / f"{year}") for year in high_smoke_years],
            args.esacci_lakes_id,
        )
    ]

    low_smoke_years_dataframe = pd.concat(
        low_smoke_year_dataframes,
        ignore_index=True,
    )
    high_smoke_years_dataframe = pd.concat(
        high_smoke_year_dataframes,
        ignore_index=True,
    )

    # low_smoke_years_dataframe[f"{args.esacci_lakes_variable}_mean"] = (
    #     low_smoke_years_dataframe[f"{args.esacci_lakes_variable}_mean"].apply(
    #         lambda x: x - 273.15
    #     )
    # )
    # high_smoke_years_dataframe[f"{args.esacci_lakes_variable}_mean"] = (
    #     high_smoke_years_dataframe[f"{args.esacci_lakes_variable}_mean"].apply(
    #         lambda x: x - 273.15
    #     )
    # )

    low_smoke_years_gam  = fit(low_smoke_years_dataframe, args.esacci_lakes_variable)
    high_smoke_years_gam = fit(high_smoke_years_dataframe, args.esacci_lakes_variable)

    _, ax = plt.subplots()

    sns.scatterplot(
        data=low_smoke_years_dataframe,
        x="index",
        y=f"{args.esacci_lakes_variable}_mean",
        ax=ax,
        alpha=0.25,
        edgecolor="none",
        color="grey"
    )
    low_smoke_years_nonan = low_smoke_years_dataframe.dropna(subset=[f"{args.esacci_lakes_variable}_mean"])
    low_smoke_years_X = np.linspace(
        low_smoke_years_nonan["index"].min(),
        low_smoke_years_nonan["index"].max(),
        300
    )
    ax.plot(
        low_smoke_years_X,
        low_smoke_years_gam.predict(low_smoke_years_X),
        color="grey",
        label=f"Low smoke years: {low_smoke_years}"
    )

    sns.scatterplot(
        data=high_smoke_years_dataframe,
        x="index",
        y=f"{args.esacci_lakes_variable}_mean",
        ax=ax,
        alpha=0.25,
        edgecolor="none",
        color="blue"
    )
    high_smoke_years_nonan = high_smoke_years_dataframe.dropna(subset=[f"{args.esacci_lakes_variable}_mean"])
    high_smoke_years_X     = np.linspace(
        high_smoke_years_nonan["index"].min(),
        high_smoke_years_nonan["index"].max(),
        300
    )
    ax.plot(
        high_smoke_years_X,
        high_smoke_years_gam.predict(high_smoke_years_X),
        color="blue",
        label=f"High smoke years: {high_smoke_years}"
    )

    ax.set_xlabel(
        "Day",
        fontsize=14
    )
    ax.set_ylabel(
        f"{ESACCI_LAKES_VARIABLES[args.esacci_lakes_variable].long_name} ({ESACCI_LAKES_VARIABLES[args.esacci_lakes_variable].units})",
        fontsize=14
    )
    ax.grid(
        True,
        alpha=0.25
    )
    ax.legend()

    plt.title(
        f"_ ({args.esacci_lakes_id}): Mean {args.esacci_lakes_variable} Measurements",
        fontsize=18
    )
    plt.show()

    return RETURN_SUCCESS


# ==================================================================================================


if __name__ == "__main__":
    sys.exit(main())
