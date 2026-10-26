"""
build_esacci_lakes_merged_product_coverage_csv.py.

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse   import (
                    ArgumentParser,
                    Namespace,
                )

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
                                                    argument_is_directory,
                                                    argument_is_file,
                                                )

PROG    = "build_esacci_lakes_merged_product_coverage_csv.py"
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
                                    "esacci_lakes_merged_product_dir_path":                         argument_is_directory,
                                }

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


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

    records = []

    for esacci_lakes_id in tqdm(metadata_df.index):
        try:
            high_smoke_year = get_most_smoke_year(
                                esacci_lakes_id,
                                counts_of_distinct_start_days_by_high_smoke_year_df_long,
                            )
        except ValueError:
            continue

        high_smoke_year_observations_ser    = get_observations_ser(
                                                esacci_lakes_id,
                                                high_smoke_year,
                                                args.esacci_lakes_merged_product_dir_path,
                                            )
        high_smoke_year_coverage            = (
                                                high_smoke_year_observations_ser
                                                .notna()
                                                .sum()
                                            ) 

        records.append(
            {
                "esacci_lakes_id":          esacci_lakes_id,
                "high_smoke_year_coverage": high_smoke_year_coverage,
            }
        )

    coverage_df = pd.DataFrame(records).set_index("esacci_lakes_id")

    to_csv(
        coverage_df,
        args.output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
