"""
Filename:   compute_umn_lakes_naive_deltas.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
import logging
import os
import sys

from argparse   import (
                    ArgumentParser,
                    Namespace,
                )
from pathlib    import Path
from typing     import Any

# Related Third-party Imports
import numpy    as np
import pandas   as pd
import psycopg

from dotenv         import load_dotenv
from scipy.stats    import skew
from tqdm           import tqdm

# Local Application/Library Specific Imports
from wfsel.arguments                    import add_argument_output
from wfsel.exit_codes                   import (
                                            EXIT_FAILURE,
                                            EXIT_SUCCESS,
                                        )
from wfsel.io.writers                   import to_csv
from wfsel.sources.umn_lakes.arguments  import add_argument_umn_lakes_product_dir_path
from wfsel.sources.umn_lakes.literals   import (
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_DATE,
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_FIELD,
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_FRAC_VALID,
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_UNMLKNUM,
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_V50P,
                                            UMN_LAKES_PRODUCT_GLOB_PATTERN_A4,
                                            UMN_LAKES_PRODUCT_GLOB_PATTERN_CL,
                                            UMN_LAKES_PRODUCT_GLOB_PATTERN_SD,
                                        )
from wfsel.sources.umn_lakes.queries    import query_umn_lakes_distinct_start_days
from wfsel.sources.umn_lakes.readers    import read_umn_lakes_product_tsv
from wfsel.time.literals                import DATE_FORMAT_YYYYMMDD
from wfsel.utils.argparse_utils         import (
                                            arguments_are_valid as _arguments_are_valid,
                                            build_parser        as _build_parser,
                                            argument_is_dir,
                                        )

PROG    = "compute_umn_lakes_naive_deltas.py"
DESC    = ""

MINIMUM_N_FOR_POP   = 1
MINIMUM_N_FOR_FPC   = 3

logging.basicConfig(
    stream  = sys.stderr,
    level   = logging.INFO,
)


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
            )
    parser  = _build_parser(
                parser,
                positional_arguments    = [
                                            add_argument_umn_lakes_product_dir_path,
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
    argument_name_to_validator = {
                                    "output": argument_is_dir,
                                }

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


# ----------------------------------------------------------------------
# comprehender functions
# ----------------------------------------------------------------------
def comprehend_umn_lakes_product_df_list(
    umn_lakes_product_tsv_paths: list[Path],
) -> list[pd.DataFrame]:
    """
    Comprehend a list of UMN Lakes product dataframes.

    Parameters
    ----------
    umn_lakes_product_tsv_paths : list[Path]
        The list of UMN Lakes product tsv paths

    Returns
    -------
    list[pd.DataFrame]
        A list of UMN Lakes product dataframes
    """
    df_list = [
                read_umn_lakes_product_tsv(umn_lakes_product_tsv_path)
                for umn_lakes_product_tsv_path
                in umn_lakes_product_tsv_paths
            ]

    return df_list


# ----------------------------------------------------------------------
# expander functions
# ----------------------------------------------------------------------
def expand_umn_lakes_product_df(
    umn_lakes_product_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Expand a UMN Lakes product dataframe with columns "_timestamp",
    "_year", "_month", and "_day".

    Parameters
    ----------
    umn_lakes_product_df : pd.DataFrame
        The UMN Lakes product dataframe

    Returns
    -------
    pd.DataFrame
        A UMN Lakes product dataframe
    """
    df = umn_lakes_product_df.copy()

    df["_timestamp"]    = pd.to_datetime(df[UMN_LAKES_PRODUCT_COLUMN_NAME_DATE], format = DATE_FORMAT_YYYYMMDD)
    df["_year"]         = df["_timestamp"].dt.year
    df["_month"]        = df["_timestamp"].dt.month
    df["_day"]          = df["_timestamp"].dt.day

    return df


# ----------------------------------------------------------------------
# builder functions
# ----------------------------------------------------------------------
def build_umn_lakes_naive_deltas_row(
    o_0:                                pd.Series[Any],
    o_1:                                pd.Series[Any],
    umn_lakes_distinct_start_days_ser:  pd.Series[int],
) -> dict[str, Any]:
    """
    Build a UMN Lakes naive deltas row.

    Parameters
    ----------
    o_0 : pd.Series[Any]
        The leftmost observation series
    o_1 : pd.Series[Any]
        The rightmost observation series
    umn_lakes_distinct_start_days_ser : pd.Series[int]
        The UMN Lakes distinct start days series

    Returns
    -------
    dict[str, Any]
        A UMN Lakes naive deltas row

    Raises
    ------
    ValueError
        If o_0 and o_1 are not of the same field
    ValueError
        If o_0 and o_1 are not of the same unmlknum
    ValueError
        If o_0 and o_1 are not of the same year
    """
    field_0 = o_0[UMN_LAKES_PRODUCT_COLUMN_NAME_FIELD]
    field_1 = o_1[UMN_LAKES_PRODUCT_COLUMN_NAME_FIELD]

    if field_0 != field_1:
        message = f"expected observation 0 to be of the same field as observation 1: got {field_0} and {field_1}"

        raise ValueError(message)

    umnlknum_0 = o_0[UMN_LAKES_PRODUCT_COLUMN_NAME_UNMLKNUM]
    umnlknum_1 = o_1[UMN_LAKES_PRODUCT_COLUMN_NAME_UNMLKNUM]

    if umnlknum_0 != umnlknum_1:
        message = f"expected observation 0 to be of the same unmlknum as observation 1: got {umnlknum_0} and {umnlknum_1}"

        raise ValueError(message)

    year_0 = o_0["_timestamp"].year
    year_1 = o_1["_timestamp"].year

    if year_0 != year_1:
        message = f"expected observation 0 to be of the same year as observation 1: got {year_0} and {year_1}"

        raise ValueError(message)

    m_0     = o_0[UMN_LAKES_PRODUCT_COLUMN_NAME_V50P]
    m_1     = o_1[UMN_LAKES_PRODUCT_COLUMN_NAME_V50P]
    delta   = m_1 - m_0

    j_0     = o_0["_timestamp"].day_of_year
    j_1     = o_1["_timestamp"].day_of_year
    E       = umn_lakes_distinct_start_days_ser[
                        (umn_lakes_distinct_start_days_ser > j_0)
                    &   (umn_lakes_distinct_start_days_ser < j_1)
                ]
    N       = len(E)

    if N >= MINIMUM_N_FOR_POP:
        X       = (
                        (E   - j_0)
                    /   (j_1 - j_0)
                )
        mu      = np.mean(X)
        sigma   = np.std(X)

        if N >= MINIMUM_N_FOR_FPC:
            g_1 = skew(X)
        else:
            g_1 = np.nan
    else:
        mu      = np.nan
        sigma   = np.nan
        g_1     = np.nan

    row = {
        "field":            field_0,
        "unmlknum":         umnlknum_0,
        "o_0_date":         o_0[UMN_LAKES_PRODUCT_COLUMN_NAME_DATE],
        "o_0_v50p":         o_0[UMN_LAKES_PRODUCT_COLUMN_NAME_V50P],
        "o_0_frac_valid":   o_0[UMN_LAKES_PRODUCT_COLUMN_NAME_FRAC_VALID],
        "o_1_date":         o_1[UMN_LAKES_PRODUCT_COLUMN_NAME_DATE],
        "o_1_v50p":         o_1[UMN_LAKES_PRODUCT_COLUMN_NAME_V50P],
        "o_1_frac_valid":   o_1[UMN_LAKES_PRODUCT_COLUMN_NAME_FRAC_VALID],
        "delta":            delta,
        "N":                N,
        "mu":               mu,
        "sigma":            sigma,
        "g_1":              g_1,
    }

    return row


def build_umn_lakes_naive_deltas_df(
    umn_lakes_product_df:   pd.DataFrame,
    connection:             psycopg.Connection,
) -> pd.DataFrame:
    """
    Build a UMN Lakes naive deltas dataframe.

    Parameters
    ----------
    umn_lakes_product_df : pd.DataFrame
        The UMN Lakes product dataframe
    connection : psycopg.Connection
        The connection

    Returns
    -------
    pd.DataFrame
        A UMN Lakes naive deltas dataframe
    """
    expanded_df = expand_umn_lakes_product_df(umn_lakes_product_df)
    df_group_by = (
                    expanded_df
                    .sort_values("_timestamp")
                    .groupby(
                        [
                            UMN_LAKES_PRODUCT_COLUMN_NAME_UNMLKNUM,
                            "_year",
                        ],
                    )
                )

    rows = []

    for (umn_lakes_id, year), df in tqdm(df_group_by):
        distinct_start_days_ser = query_umn_lakes_distinct_start_days(
                                    umn_lakes_id,   # type: ignore[arg-type]
                                    year,           # type: ignore[arg-type]
                                    connection,
                                )

        for i in range(1, len(df)):
            o_0 = df.iloc[i - 1]
            o_1 = df.iloc[i]

            row = build_umn_lakes_naive_deltas_row(
                    o_0,
                    o_1,
                    distinct_start_days_ser,
                )

            rows.append(row)

    df = pd.DataFrame(rows)

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

    load_dotenv()

    umn_lakes_product_dir_path  = args.umn_lakes_product_dir_path
    output                      = args.output

    a4_product_tsv_paths    = list(umn_lakes_product_dir_path.glob(UMN_LAKES_PRODUCT_GLOB_PATTERN_A4))
    cl_product_tsv_paths    = list(umn_lakes_product_dir_path.glob(UMN_LAKES_PRODUCT_GLOB_PATTERN_CL))
    sd_product_tsv_paths    = list(umn_lakes_product_dir_path.glob(UMN_LAKES_PRODUCT_GLOB_PATTERN_SD))

    a4_product_df_list  = comprehend_umn_lakes_product_df_list(a4_product_tsv_paths)
    cl_product_df_list  = comprehend_umn_lakes_product_df_list(cl_product_tsv_paths)
    sd_product_df_list  = comprehend_umn_lakes_product_df_list(sd_product_tsv_paths)

    a4_product_df   = pd.concat(a4_product_df_list)
    cl_product_df   = pd.concat(cl_product_df_list)
    sd_product_df   = pd.concat(sd_product_df_list)

    with psycopg.connect(os.environ["POSTGRESQL_URL"]) as connection:
        a4_product_naive_deltas_df  = build_umn_lakes_naive_deltas_df(a4_product_df, connection)
        cl_product_naive_deltas_df  = build_umn_lakes_naive_deltas_df(cl_product_df, connection)
        sd_product_naive_deltas_df  = build_umn_lakes_naive_deltas_df(sd_product_df, connection)

    to_csv(a4_product_naive_deltas_df, output_file_path = output / "a4_product_naive_deltas.csv")
    to_csv(cl_product_naive_deltas_df, output_file_path = output / "cl_product_naive_deltas.csv")
    to_csv(sd_product_naive_deltas_df, output_file_path = output / "sd_product_naive_deltas.csv")

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
