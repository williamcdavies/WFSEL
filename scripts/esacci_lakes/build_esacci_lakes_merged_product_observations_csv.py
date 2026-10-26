"""
build_esacci_lakes_merged_product_observations_csv.py.

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse           import (
                            ArgumentParser,
                            Namespace,
                        )

# Related Third-party Imports
import numpy    as np
import pandas   as pd
import psycopg

# Local Application/Library Specific Imports
from wfsel.exit_codes                           import (
                                                    EXIT_FAILURE,
                                                    EXIT_SUCCESS,
                                                )
from wfsel.io.arguments                         import add_argument_output
from wfsel.io.writers                           import to_csv
from wfsel.sources.esacci_lakes.arguments       import (
                                                    add_argument_esacci_lakes_id,
                                                    add_argument_esacci_lakes_counts_of_distinct_start_days_by_year_csv_path,
                                                    add_argument_esacci_lakes_merged_product_dir_path,
                                                )
from wfsel.sources.esacci_lakes.callables       import (
                                                    season_function_sliding_window as _season_function_sliding_window,
                                                    apply_season_function,
                                                )
from wfsel.sources.esacci_lakes.comprehenders   import comprehend_observations
from wfsel.sources.esacci_lakes.computers       import (
                                                    mean_observations,
                                                    std_observations,
                                                )
from wfsel.sources.esacci_lakes.getters         import (
                                                    get_all_years,
                                                    get_most_smoke_year,
                                                    get_observations_ser,
                                                )
from wfsel.sources.esacci_lakes.literals        import (
                                                    COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND,
                                                    COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND,
                                                )
from wfsel.sources.esacci_lakes.melters         import melt_esacci_lakes_counts_of_distinct_start_days_by_year_df
from wfsel.sources.esacci_lakes.models          import Season
from wfsel.sources.esacci_lakes.queries         import query_distinct_start_days
from wfsel.sources.esacci_lakes.readers         import read_esacci_lakes_counts_of_distinct_start_days_by_year_csv
from wfsel.time.literals                        import DAYS_IN_A_WEEK
from wfsel.utils.argparse_utils                 import (
                                                    arguments_are_valid as _arguments_are_valid,
                                                    build_parser        as _build_parser,
                                                    argument_is_directory,
                                                    argument_is_file,
                                                )

PROG    = "build_esacci_lakes_merged_product_observations_csv.py"
DESC    = ""


# ----------------------------------------------------------------------
# setup functions
# ----------------------------------------------------------------------
def build_parser(
) -> ArgumentParser:
    """
    Wrap _build_parser.

    Returns
    -------
    ArgumentParser
        A parser
    """
    parser  = ArgumentParser(
                prog        = PROG,
                description = DESC,
                usage       = "%(prog)s [options]",
            )
    parser  = _build_parser(
                parser,
                positional_arguments    = [
                    add_argument_esacci_lakes_id,
                    add_argument_esacci_lakes_counts_of_distinct_start_days_by_year_csv_path,
                    add_argument_esacci_lakes_merged_product_dir_path,
                ],
                optional_arguments      = [
                    add_argument_output,
                ],
            )

    return parser


def arguments_are_valid(
    arguments: Namespace,
) -> bool:
    """
    Wrap _arguments_are_valid.

    Parameters
    ----------
    arguments : Namespace
        The arguments namespace

    Returns
    -------
    bool
        True if all arguments are valid, False otherwise
    """
    argument_name_to_validator  = {
                                    "esacci_lakes_counts_of_distinct_start_days_by_year_csv_path":  argument_is_file,
                                    "esacci_lakes_merged_product_dir_path":                         argument_is_directory,
                                }

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


# ----------------------------------------------------------------------
# computer functions
# ----------------------------------------------------------------------
def comp_reference(
    season: Season,
) -> float | None:
    """
    Compute the reference of a season.

    Parameters
    ----------
    season : Season
        The season

    Returns
    -------
    float | None
        The reference, or None if the reference was NaN
    """
    i       = season.first - 7
    j       = season.first - 1
    mean    = (
                season
                .observations_ser
                .loc[i:j]
                .mean()
            )

    if np.isnan(mean):
        return None

    return mean


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main(
) -> int:
    """
    Run program.

    Returns
    -------
    int
        0 if program runs successfully, 1 otherwise
    """
    args = build_parser().parse_args()

    if not arguments_are_valid(args):
        return EXIT_FAILURE

    counts_of_distinct_start_days_by_year_df                    = read_esacci_lakes_counts_of_distinct_start_days_by_year_csv(
                                                                    args.esacci_lakes_counts_of_distinct_start_days_by_year_csv_path,
                                                                )
    counts_of_distinct_start_days_by_year_df_long               = melt_esacci_lakes_counts_of_distinct_start_days_by_year_df(
                                                                    counts_of_distinct_start_days_by_year_df,
                                                                )
    counts_of_distinct_start_days_by_high_smoke_year_df_long    = counts_of_distinct_start_days_by_year_df_long[
                                                                    counts_of_distinct_start_days_by_year_df_long["count_of_distinct_start_days"]
                                                                    >= COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND
                                                                ]
    counts_of_distinct_start_days_by_low_smoke_year_df_long     = counts_of_distinct_start_days_by_year_df_long[
                                                                    counts_of_distinct_start_days_by_year_df_long["count_of_distinct_start_days"]
                                                                    <= COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND
                                                                ]

    try:
        high_smoke_year = get_most_smoke_year(
                            args.esacci_lakes_id,
                            counts_of_distinct_start_days_by_high_smoke_year_df_long,
                        )
    except ValueError as exc:
        message = f"fatal: lake {args.esacci_lakes_id} has no high smoke year"

        raise ValueError(message) from exc

    low_smoke_years = get_all_years(
                        args.esacci_lakes_id,
                        counts_of_distinct_start_days_by_low_smoke_year_df_long,
                    )

    if not low_smoke_years:
        message = f"fatal: lake {args.esacci_lakes_id} has no low smoke years"

        raise ValueError(message)

    high_smoke_year_observations_ser        = get_observations_ser(
                                                args.esacci_lakes_id,
                                                high_smoke_year,
                                                args.esacci_lakes_merged_product_dir_path,
                                            )
    low_smoke_year_observations             = comprehend_observations(
                                                args.esacci_lakes_id,
                                                low_smoke_years,
                                                args.esacci_lakes_merged_product_dir_path,
                                            )
    low_smoke_year_observations_mean_ser    = mean_observations(low_smoke_year_observations)
    low_smoke_year_observations_std_ser     = std_observations(low_smoke_year_observations)

    with psycopg.connect("dbname=spatial") as connection:
        high_smoke_year_distinct_start_days_ser = query_distinct_start_days(
                                                    args.esacci_lakes_id,
                                                    high_smoke_year,
                                                    connection,
                                                )

    if (smoke_season    := apply_season_function(
                            high_smoke_year_observations_ser,
                            lambda: _season_function_sliding_window(
                                high_smoke_year_distinct_start_days_ser,
                                width   = DAYS_IN_A_WEEK,
                                trigger = 4,
                                edge    = "right",
                            ),
                        )) is None:
        message = f"fatal: lake {args.esacci_lakes_id} has no smoke season"

        raise ValueError(message)

    if (reference := comp_reference(smoke_season)) is None:
        message = f"fatal: lake {args.esacci_lakes_id} has no reference"

        raise ValueError(message)

    high_smoke_year_observations_anomaly_ser        = high_smoke_year_observations_ser - reference
    low_smoke_year_observations_mean_anomaly_ser    = low_smoke_year_observations_mean_ser - reference

    observations_df = pd.DataFrame({
                        "high_smoke_year_observations":             high_smoke_year_observations_ser,
                        **{
                            f"low_smoke_year_observations_{i}": low_smoke_year_observations_ser
                            for (
                                    i,
                                    low_smoke_year_observations_ser,
                                )
                            in enumerate(low_smoke_year_observations)
                        },
                        "low_smoke_year_observations_mean":         low_smoke_year_observations_mean_ser,
                        "low_smoke_year_observations_std":          low_smoke_year_observations_std_ser,
                        "high_smoke_year_observations_anomaly":     high_smoke_year_observations_anomaly_ser,
                        "low_smoke_year_observations_mean_anomaly": low_smoke_year_observations_mean_anomaly_ser,
                    })

    to_csv(
        observations_df,
        args.output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
