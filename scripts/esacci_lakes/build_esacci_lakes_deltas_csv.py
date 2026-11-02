"""
Filename:   build_esacci_lakes_deltas_csv.py
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

# Local Application/Library Specific Imports
from wfsel.exit_codes                           import (
                                                    EXIT_FAILURE,
                                                    EXIT_SUCCESS,
                                                )
from wfsel.io.arguments                         import add_argument_output
from wfsel.io.writers                           import to_csv
from wfsel.sources.esacci_lakes.arguments       import (
                                                    add_argument_esacci_lakes_high_smoke_year_observations_anomaly_csv_path,
                                                    add_argument_esacci_lakes_low_smoke_year_observations_anomaly_csv_path,
                                                    add_argument_esacci_lakes_week_first,
                                                    add_argument_esacci_lakes_week_last,
                                                )
from wfsel.sources.esacci_lakes.comprehenders   import comprehend_column_names
from wfsel.sources.esacci_lakes.readers         import (
                                                    read_esacci_lakes_high_smoke_year_observations_anomaly_csv,
                                                    read_esacci_lakes_low_smoke_year_observations_anomaly_csv,
                                                )
from wfsel.utils.argparse_utils                 import (
                                                    arguments_are_valid as _arguments_are_valid,
                                                    build_parser        as _build_parser,
                                                    argument_is_file,
                                                )

PROG    = "build_esacci_lakes_deltas_csv.py"
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
                    add_argument_esacci_lakes_high_smoke_year_observations_anomaly_csv_path,
                    add_argument_esacci_lakes_low_smoke_year_observations_anomaly_csv_path,
                    add_argument_esacci_lakes_week_first,
                    add_argument_esacci_lakes_week_last,
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
                                    "esacci_lakes_high_smoke_year_observations_anomaly_csv_path":   argument_is_file,
                                    "esacci_lakes_low_smoke_year_observations_anomaly_csv_path":    argument_is_file,
                                }

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


# ----------------------------------------------------------------------
# core
# ----------------------------------------------------------------------
def build_deltas_df(
    esacci_lakes_high_smoke_year_observations_df:   pd.DataFrame,
    esacci_lakes_low_smoke_year_observations_df:    pd.DataFrame,
    column_names:                                   list[str],
) -> pd.DataFrame:
    """
    Build a deltas dataframe.

    Parameters
    ----------
    esacci_lakes_high_smoke_year_observations_df : pd.DataFrame
        The ESA CCI Lakes high smoke year observations dataframe
    esacci_lakes_low_smoke_year_observations_df : pd.DataFrame
        The ESA CCI Lakes low smoke year observations dataframe
    column_names : list[str]
        The list of column names

    Returns
    -------
    pd.DataFrame
        A deltas dataframe

    Raises
    ------
    ValueError
        If high smoke year observations dataframe and low smoke year
        observations dataframe are not of the same shape
    ValueError
        If high smoke year observations dataframe and low smoke year
        observations dataframe are not of the same index
    ValueError
        If high smoke year observations dataframe and low smoke year
        observations dataframe are not of the same NaN mask
    """
    if esacci_lakes_high_smoke_year_observations_df.shape != esacci_lakes_low_smoke_year_observations_df.shape:
        message = "expected high smoke year observations dataframe and low smoke year observations dataframe to be of the same shape"

        raise ValueError(message)

    if not esacci_lakes_high_smoke_year_observations_df.index.equals(esacci_lakes_low_smoke_year_observations_df.index):
        message = "expected high smoke year observations dataframe and low smoke year observations dataframe to be of the same index"

        raise ValueError(message)

    if not (esacci_lakes_high_smoke_year_observations_df.isna() == esacci_lakes_low_smoke_year_observations_df.isna()).all(axis=None):
        message = "expected high smoke year observations dataframe and low smoke year observations dataframe to be of the same NaN mask"

        raise ValueError(message)

    windowed_high_smoke_year_observations_df    = esacci_lakes_high_smoke_year_observations_df[column_names]
    windowed_low_smoke_year_observations_df     = esacci_lakes_low_smoke_year_observations_df[column_names]
    diff                                        = windowed_high_smoke_year_observations_df - windowed_low_smoke_year_observations_df

    delta       = (
                    diff
                    .mean(axis=1)
                )
    coverage    = (
                    diff
                    .notna()
                    .sum(axis=1)
                )

    df  = pd.DataFrame(
            {
                "delta":    delta,
                "coverage": coverage,
            },
            index = windowed_high_smoke_year_observations_df.index,
        )

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

    high_smoke_year_observations_anomaly_df = read_esacci_lakes_high_smoke_year_observations_anomaly_csv(
                                                args.esacci_lakes_high_smoke_year_observations_anomaly_csv_path,
                                            )
    low_smoke_year_observations_anomaly_df  = read_esacci_lakes_low_smoke_year_observations_anomaly_csv(
                                                args.esacci_lakes_low_smoke_year_observations_anomaly_csv_path,
                                            )

    column_names    = comprehend_column_names(
                        args.esacci_lakes_week_first,
                        args.esacci_lakes_week_last,
                    )

    deltas_df   = build_deltas_df(
                    high_smoke_year_observations_anomaly_df,
                    low_smoke_year_observations_anomaly_df,
                    column_names,
                )

    to_csv(
        deltas_df,
        args.output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
