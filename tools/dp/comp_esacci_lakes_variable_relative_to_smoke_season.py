r"""
comp_esacci_lakes_variable_relative_to_smoke_season.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path

# Related Third-party Imports
import numpy as np
import pandas as pd
import psycopg

from tqdm import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.argparse import (
    add_argument_esacci_lakes_variable,
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_average_depths_csv_path,
    add_argument_esacci_lakes_counts_of_distinct_start_days_csv_path,
    add_argument_local_data_dir_path,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_average_depths_csv_path_exists,
    argument_esacci_lakes_counts_of_distinct_start_days_csv_path_exists,
    argument_local_data_dir_path_exists,
)
from lib.esacci_lakes.utils.pandas import (
    read_esacci_lakes_metadata_csv,
    read_esacci_lakes_average_depths_csv,
    read_esacci_lakes_counts_of_distinct_start_days_csv,
)
from lib.esacci_lakes.vars import (
    COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND,
    COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND,
    COUNT_OF_DISTINCT_START_DAYS_QUERY,
)
from lib.io.vars import (
    RETURN_FAILURE,
    RETURN_SUCCESS,
)

PROG = "comp_esacci_lakes_variable_relative_to_smoke_season.py"
NUMBER_OF_DAYS_IN_A_WEEK = 7
NUMBER_OF_LOOKBACK_WEEKS = 3


def comp_week_index(
    day: int,
    anchor: int,
) -> int:
    """
    Returns a week index given an arbitrary julian day and an anchor
    julian day.

    Parameters
    ----------
    day : int
        An arbitrary julian day

    anchor: int
        An anchor julian day
    """
    return (day - anchor) // NUMBER_OF_DAYS_IN_A_WEEK


def comp_first_day_in_week(
    week_idx: int,
    anchor: int,
) -> int:
    """
    Returns the first julian day in a week given an arbitrary week index
    and an anchor julian day.

    Parameters
    ----------
    week_idx : int
        An arbitrary week index

    anchor: int
        An anchor julian day
    """
    return anchor + week_idx * NUMBER_OF_DAYS_IN_A_WEEK


def comp_last_day_in_week(
    week_idx: int,
    anchor: int,
) -> int:
    """
    Returns the last julian day in a week given an arbitrary week index
    and an anchor julian day.

    Parameters
    ----------
    week_idx : int
        An arbitrary week index

    anchor: int
        An anchor julian day
    """
    return comp_first_day_in_week(week_idx + 1, anchor) - 1


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = ArgumentParser(
        prog=f"{PROG}.py",
        usage="%(prog)s [options]",
        description="""""",
    )

    # Positional arguments
    add_argument_esacci_lakes_variable(parser)
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_average_depths_csv_path(parser)
    add_argument_esacci_lakes_counts_of_distinct_start_days_csv_path(parser)
    add_argument_local_data_dir_path(parser)

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not argument_esacci_lakes_metadata_csv_path_exists(
        args.esacci_lakes_metadata_csv_path,
        loud=True,
    ):
        return RETURN_FAILURE

    if not argument_esacci_lakes_average_depths_csv_path_exists(
        args.esacci_lakes_average_depths_csv_path,
        loud=True,
    ):
        return RETURN_FAILURE

    if not argument_esacci_lakes_counts_of_distinct_start_days_csv_path_exists(
        args.esacci_lakes_counts_of_distinct_start_days_csv_path,
        loud=True,
    ):
        return RETURN_FAILURE

    if not argument_local_data_dir_path_exists(
        args.local_data_dir_path,
        loud=True,
    ):
        return RETURN_FAILURE
    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    high_smoke_year_records = []
    low_smoke_year_records = []

    esacci_lakes_metadata_df = read_esacci_lakes_metadata_csv(
        args.esacci_lakes_metadata_csv_path,
    )
    esacci_lakes_average_depths_df = read_esacci_lakes_average_depths_csv(
        args.esacci_lakes_average_depths_csv_path,
    )
    esacci_lakes_counts_of_distinct_start_days_df = (
        read_esacci_lakes_counts_of_distinct_start_days_csv(
            args.esacci_lakes_counts_of_distinct_start_days_csv_path,
        )
    )

    for esacci_lakes_id in tqdm(
        esacci_lakes_metadata_df.index,
    ):
        esacci_lakes_average_depth = esacci_lakes_average_depths_df.loc[esacci_lakes_id]
        assert isinstance(esacci_lakes_average_depth, pd.Series)

        esacci_lakes_counts_of_distinct_start_days = (
            esacci_lakes_counts_of_distinct_start_days_df.loc[esacci_lakes_id]
        )
        assert isinstance(esacci_lakes_counts_of_distinct_start_days, pd.Series)

        if pd.isna(esacci_lakes_average_depth.item()):
            continue

        if (
            max(esacci_lakes_counts_of_distinct_start_days)
            < COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND
        ):
            continue

        if (
            min(esacci_lakes_counts_of_distinct_start_days)
            > COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND
        ):
            continue

        high_smoke_year_record = {"esacci_lakes_id": esacci_lakes_id}
        high_smoke_year_esacci_lakes_variable_values = defaultdict(list)
        high_smoke_year = f"{esacci_lakes_counts_of_distinct_start_days[esacci_lakes_counts_of_distinct_start_days >= COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND].index[-1]}"

        low_smoke_year_record = {"esacci_lakes_id": esacci_lakes_id}
        low_smoke_year_esacci_lakes_variable_values = defaultdict(list)
        low_smoke_year = f"{esacci_lakes_counts_of_distinct_start_days[esacci_lakes_counts_of_distinct_start_days <= COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND].index[-1]}"

        with psycopg.connect("dbname=spatial") as conn:
            with conn.cursor() as cur:
                cur.execute(
                    COUNT_OF_DISTINCT_START_DAYS_QUERY.format(
                        id=esacci_lakes_id,
                        year=high_smoke_year,
                    )  # type: ignore
                )

                esacci_lakes_distinct_start_days = pd.Series(
                    [tuple[0] for tuple in cur.fetchall()]
                )

        high_smoke_year_files = sorted(
            Path(args.local_data_dir_path / high_smoke_year).glob("**/*.csv")
        )
        low_smoke_year_files = sorted(
            Path(args.local_data_dir_path / low_smoke_year).glob("**/*.csv")
        )

        day_0 = -1

        for i in range(
            3,
            len(esacci_lakes_distinct_start_days),
        ):
            if (
                esacci_lakes_distinct_start_days[i]
                < esacci_lakes_distinct_start_days[i - 3] + 7
            ):
                day_0 = esacci_lakes_distinct_start_days[i]

                break

        day_N = -1

        for i in reversed(
            range(
                3,
                len(esacci_lakes_distinct_start_days),
            )
        ):
            if (
                esacci_lakes_distinct_start_days[i]
                < esacci_lakes_distinct_start_days[i - 3] + 7
            ):
                day_N = esacci_lakes_distinct_start_days[i]

                break

        if day_0 == -1 or day_N == -1:
            continue

        start = day_0 - NUMBER_OF_LOOKBACK_WEEKS * NUMBER_OF_DAYS_IN_A_WEEK
        stop = comp_last_day_in_week(comp_week_index(day_N, day_0), day_0)

        if (
            start < 1
            or stop > len(high_smoke_year_files)
            or stop > len(low_smoke_year_files)
        ):
            continue

        for day_n in range(
            start,
            stop + 1,
        ):
            high_smoke_year_df = pd.read_csv(
                high_smoke_year_files[day_n - 1],
                index_col="id",
            )
            high_smoke_year_esacci_lakes_variable_value = (
                high_smoke_year_df[f"{args.esacci_lakes_variable}_mean"]
                .loc[esacci_lakes_id]
                .item()
            )

            low_smoke_year_df = pd.read_csv(
                low_smoke_year_files[day_n - 1],
                index_col="id",
            )
            lo_esacci_lakes_variable_value = (
                low_smoke_year_df[f"{args.esacci_lakes_variable}_mean"]
                .loc[esacci_lakes_id]
                .item()
            )

            week_idx = comp_week_index(day_n, day_0)

            high_smoke_year_esacci_lakes_variable_values[week_idx].append(
                high_smoke_year_esacci_lakes_variable_value
            )
            low_smoke_year_esacci_lakes_variable_values[week_idx].append(
                lo_esacci_lakes_variable_value
            )

        for i, l in high_smoke_year_esacci_lakes_variable_values.items():
            high_smoke_year_record[f"w{i}"] = np.nanmean(l)

        for i, l in low_smoke_year_esacci_lakes_variable_values.items():
            low_smoke_year_record[f"w{i}"] = np.nanmean(l)

        for i in set(high_smoke_year_esacci_lakes_variable_values) | set(
            low_smoke_year_esacci_lakes_variable_values
        ):
            key = f"w{i}"
            high_smoke_year_val = high_smoke_year_record.get(key, np.nan)
            low_smoke_year_val = low_smoke_year_record.get(key, np.nan)

            if pd.isna(high_smoke_year_val) or pd.isna(low_smoke_year_val):
                high_smoke_year_record[key] = np.nan
                low_smoke_year_record[key] = np.nan

        # --- normalisation block: comment out to run unnormalised ---
        high_smoke_year_normal = np.nanmean([high_smoke_year_record.get("w-1")])  # type: ignore
        low_smoke_year_normal = np.nanmean([low_smoke_year_record.get("w-1")])  # type: ignore

        if pd.isna(high_smoke_year_normal) or pd.isna(low_smoke_year_normal):
            continue

        for key in high_smoke_year_record:
            if key != "esacci_lakes_id":
                high_smoke_year_record[key] -= high_smoke_year_normal

        for key in low_smoke_year_record:
            if key != "esacci_lakes_id":
                low_smoke_year_record[key] -= low_smoke_year_normal
        # --- end normalisation block ---

        high_smoke_year_records.append(high_smoke_year_record)
        low_smoke_year_records.append(low_smoke_year_record)

    high_smoke_year_df = pd.DataFrame(high_smoke_year_records)
    low_smoke_year_df = pd.DataFrame(low_smoke_year_records)

    high_smoke_year_df.to_csv(
        f"high_smoke_year_{args.esacci_lakes_variable}_normalised.csv",
        index=False,
    )
    low_smoke_year_df.to_csv(
        f"low_smoke_year_{args.esacci_lakes_variable}_normalised.csv",
        index=False,
    )

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == "__main__":
    sys.exit(main())
