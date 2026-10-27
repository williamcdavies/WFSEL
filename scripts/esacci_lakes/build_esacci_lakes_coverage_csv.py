"""
build_esacci_lakes_coverage_csv.py.

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse   import (
                    ArgumentParser,
                    Namespace,
                )
from pathlib    import Path

# Related Third-party Imports
import pandas as pd

from tqdm import tqdm

# Local Application/Library Specific Imports
from wfsel.exit_codes                           import (
                                                    EXIT_FAILURE,
                                                    EXIT_SUCCESS,
                                                )
from wfsel.io.arguments                         import add_argument_output
from wfsel.io.writers                           import to_csv
from wfsel.sources.esacci_lakes.arguments       import (
                                                    add_argument_esacci_lakes_metadata_csv_path,
                                                    add_argument_esacci_lakes_counts_of_distinct_start_days_by_year_csv_path,
                                                    add_argument_esacci_lakes_merged_product_dir_path,
                                                )
from wfsel.sources.esacci_lakes.getters         import (
                                                    get_most_smoke_year,
                                                    get_observations_ser,
                                                )
from wfsel.sources.esacci_lakes.literals        import COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND
from wfsel.sources.esacci_lakes.melters         import melt_esacci_lakes_counts_of_distinct_start_days_by_year_df
from wfsel.sources.esacci_lakes.readers         import (
                                                    read_esacci_lakes_counts_of_distinct_start_days_by_year_csv,
                                                    read_esacci_lakes_metadata_csv,
                                                )
from wfsel.utils.argparse_utils                 import (
                                                    arguments_are_valid as _arguments_are_valid,
                                                    build_parser        as _build_parser,
                                                    argument_is_dir,
                                                    argument_is_file,
                                                )

PROG    = "build_esacci_lakes_coverage_csv.py"
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
                    add_argument_esacci_lakes_metadata_csv_path,
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
                                    "esacci_lakes_metadata_csv_path":                               argument_is_file,
                                    "esacci_lakes_counts_of_distinct_start_days_by_year_csv_path":  argument_is_file,
                                    "esacci_lakes_merged_product_dir_path":                         argument_is_dir,
                                }

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


# ----------------------------------------------------------------------
# core
# ----------------------------------------------------------------------
def build_coverage_row(
    esacci_lakes_id:                                            int,
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long: pd.DataFrame,
    esacci_lakes_merged_product_dir_path:                       Path,
) -> dict[str, int]:
    """
    Build a coverage row.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA CCI Lakes counts of distinct start days by
        year dataframe
    esacci_lakes_merged_product_dir_path : Path
        The ESA CCI Lakes merged product directory path

    Returns
    -------
    dict[str, int]
        A coverage row
    """
    try:
        high_smoke_year                     = get_most_smoke_year(
                                                esacci_lakes_id,
                                                esacci_lakes_counts_of_distinct_start_days_by_year_df_long,
                                            )
        high_smoke_year_observations_ser    = get_observations_ser(
                                                esacci_lakes_id,
                                                high_smoke_year,
                                                esacci_lakes_merged_product_dir_path,
                                            )
        high_smoke_year_coverage            = (
                                                high_smoke_year_observations_ser
                                                .notna()
                                                .sum()
                                            )
    except ValueError:
        high_smoke_year_coverage = 0

    row = {
            "esacci_lakes_id":          esacci_lakes_id,
            "high_smoke_year_coverage": high_smoke_year_coverage,
        }

    return row


def comprehend_coverage_df(
    esacci_lakes_metadata_df:                                   pd.DataFrame,
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long: pd.DataFrame,
    esacci_lakes_merged_product_dir_path:                       Path,
) -> pd.DataFrame:
    """
    Comprehend a coverage dataframe.

    Parameters
    ----------
    esacci_lakes_metadata_df : pd.DataFrame
        The ESA CCI Lakes metadata
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA CCI Lakes counts of distinct start days by
        year dataframe
    esacci_lakes_merged_product_dir_path : Path
        The ESA CCI Lakes merged product directory path

    Returns
    -------
    pd.DataFrame
        A coverage dataframe
    """
    df  = pd.DataFrame(
            [
                build_coverage_row(
                    esacci_lakes_id,
                    esacci_lakes_counts_of_distinct_start_days_by_year_df_long,
                    esacci_lakes_merged_product_dir_path,
                )
                for esacci_lakes_id
                in tqdm(esacci_lakes_metadata_df.index)
            ]
        ).set_index("esacci_lakes_id")
    
    return df


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

    metadata_df                                                 = read_esacci_lakes_metadata_csv(
                                                                    args.esacci_lakes_metadata_csv_path,
                                                                )
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

    coverage_df = comprehend_coverage_df(
                    metadata_df,
                    counts_of_distinct_start_days_by_high_smoke_year_df_long,
                    args.esacci_lakes_merged_product_dir_path,
                )

    to_csv(
        coverage_df,
        args.output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
