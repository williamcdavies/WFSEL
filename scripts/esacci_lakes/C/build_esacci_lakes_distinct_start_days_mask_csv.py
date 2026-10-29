"""
Filename:   build_esacci_lakes_distinct_start_days_mask_csv.py
Author:     William Chuter-Davies
Modified:   29/10/26
"""

# Standard Library Imports
import sys

from argparse   import (
                    ArgumentParser,
                    Namespace,
                )

# Related Third-party Imports
import pandas as pd
import psycopg

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
                                                )
from wfsel.sources.esacci_lakes.builders        import build_distinct_labels_mask
from wfsel.sources.esacci_lakes.filters         import filter_counts_of_distinct_start_days_by_year_df_long_by_upper_bound
from wfsel.sources.esacci_lakes.getters         import get_most_smoke_year
from wfsel.sources.esacci_lakes.melters         import melt_esacci_lakes_counts_of_distinct_start_days_by_year_df
from wfsel.sources.esacci_lakes.queries         import query_distinct_start_days
from wfsel.sources.esacci_lakes.readers         import (
                                                    read_esacci_lakes_counts_of_distinct_start_days_by_year_csv,
                                                    read_esacci_lakes_metadata_csv,
                                                )
from wfsel.utils.argparse_utils                 import (
                                                    arguments_are_valid as _arguments_are_valid,
                                                    build_parser        as _build_parser,
                                                    argument_is_file,
                                                )

PROG    = "build_esacci_lakes_distinct_start_days_mask_csv.py"
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
        The arguments

    Returns
    -------
    bool
        True if all arguments are valid, False otherwise
    """
    argument_name_to_validator  = {
                                    "esacci_lakes_metadata_csv_path":                               argument_is_file,
                                    "esacci_lakes_counts_of_distinct_start_days_by_year_csv_path":  argument_is_file,
                                }

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


# ----------------------------------------------------------------------
# core
# ----------------------------------------------------------------------
def build_distinct_start_days_mask_column(
    esacci_lakes_id:                                            int,
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long: pd.DataFrame,
    connection:                                                 psycopg.Connection,
) -> pd.Series[int]:
    """
    Build a distinct start days mask column for a lake by its id.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA CCI Lakes counts of distinct start days by
        year dataframe
    connection : psycopg.Connection
        The connection

    Returns
    -------
    pd.Series[int]
        A distinct start days mask column
    """
    try:
        high_smoke_year = get_most_smoke_year(
                            esacci_lakes_id,
                            esacci_lakes_counts_of_distinct_start_days_by_year_df_long,
                        )
    except ValueError:
        column = pd.Series(name = esacci_lakes_id)

        return column

    distinct_start_days_ser = query_distinct_start_days(
                                esacci_lakes_id,
                                high_smoke_year,
                                connection,
                            )

    column      = build_distinct_labels_mask(
                    distinct_start_days_ser,
                    1,
                    367,
                )
    column.name = esacci_lakes_id

    return column


def comprehend_distinct_start_days_mask_df(
    esacci_lakes_metadata_df:                                   pd.DataFrame,
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long: pd.DataFrame,
    connection:                                                 psycopg.Connection,
) -> pd.DataFrame:
    """
    Comprehend a distinct start days mask dataframe.

    Parameters
    ----------
    esacci_lakes_metadata_df : pd.DataFrame
        The ESA CCI Lakes metadata dataframe
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA CCI Lakes counts of distinct start days by
        year dataframe
    connection : psycopg.Connection
        The connection

    Returns
    -------
    pd.DataFrame
        A distinct start days mask dataframe
    """
    df              = pd.DataFrame([
                        build_distinct_start_days_mask_column(
                            esacci_lakes_id,
                            esacci_lakes_counts_of_distinct_start_days_by_year_df_long,
                            connection,
                        )
                        for esacci_lakes_id
                        in tqdm(esacci_lakes_metadata_df.index)
                    ]).T
    df.index.name   = "day"

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
    counts_of_distinct_start_days_by_high_smoke_year_df_long    = filter_counts_of_distinct_start_days_by_year_df_long_by_upper_bound(
                                                                    counts_of_distinct_start_days_by_year_df_long,
                                                                )

    with psycopg.connect("dbname=spatial") as connection:
        distinct_start_days_mask_df = comprehend_distinct_start_days_mask_df(
                                        metadata_df,
                                        counts_of_distinct_start_days_by_high_smoke_year_df_long,
                                        connection,
                                    )

    to_csv(
        distinct_start_days_mask_df,
        args.output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
