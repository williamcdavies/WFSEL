"""
Filename:   view_umn_lakes_product.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
import logging
import os
import sys

from argparse           import (
                            ArgumentParser,
                            Namespace,
                        )
from collections.abc    import Callable
from functools          import partial
from pathlib            import Path
from typing             import Any

# Related Third-party Imports
import pandas as pd
import psycopg

from dotenv             import load_dotenv
from matplotlib.axes    import Axes
from matplotlib.dates   import date2num
from matplotlib.typing  import ColorType

# Local Application/Library Specific Imports
from wfsel.arguments                    import add_argument_output
from wfsel.exit_codes                   import (
                                            EXIT_FAILURE,
                                            EXIT_SUCCESS,
                                        )
from wfsel.io.writers                   import to_svg
from wfsel.plot.literals                import (
                                            FONTSIZE_AXIS_LABEL,
                                            GREY_DARK,
                                        )
from wfsel.plot.builders                import build_figure
from wfsel.sources.umn_lakes.arguments  import (
                                            add_argument_umn_lakes_id,
                                            add_argument_umn_lakes_product_dir_path,
                                        )
from wfsel.sources.umn_lakes.literals   import (
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_DATE,
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_UNMLKNUM,
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_V50P,
                                            UMN_LAKES_PRODUCT_GLOB_PATTERN_A4,
                                            UMN_LAKES_PRODUCT_GLOB_PATTERN_CL,
                                            UMN_LAKES_PRODUCT_GLOB_PATTERN_SD,
                                            UMN_LAKES_PRODUCT_STEM_INDEX_YEAR,
                                        )
from wfsel.sources.umn_lakes.queries    import query_umn_lakes_distinct_start_days
from wfsel.sources.umn_lakes.readers    import read_umn_lakes_product_tsv
from wfsel.sources.umn_lakes.validators import argument_is_valid_umn_lakes_id
from wfsel.utils.argparse_utils         import (
                                            arguments_are_valid as _arguments_are_valid,
                                            build_parser        as _build_parser,
                                            argument_is_dir,
                                        )
from wfsel.utils.pandas_utils           import filter_df_by_index
from wfsel.time.literals                import DATE_FORMAT_YYYYMMDD, DATE_FORMAT_YYYYJJJ

PROG    = "view_umn_lakes_product.py"
DESC    = ""

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
                                            add_argument_umn_lakes_id,
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
    argument_name_to_validator  = {
                                    "umn_lakes_id":                 argument_is_valid_umn_lakes_id,
                                    "umn_lakes_product_dir_path":   argument_is_dir,
                                }

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


# ----------------------------------------------------------------------
# filter functions
# ----------------------------------------------------------------------
def filter_year_to_umn_lakes_product_df_by_index(
    year_to_umn_lakes_product_df:   dict[int, pd.DataFrame],
    index_name:                     str,
    index_values:                   list[Any],
) -> dict[int, pd.DataFrame]:
    """
    Filter a mapping of year to UMN Lakes product dataframe by a list of
    index values.

    Parameters
    ----------
    year_to_umn_lakes_product_df : dict[int, pd.DataFrame]
        The mapping of year to UMN Lakes product dataframe
    index_name : str
        The index name
    index_values : list[Any]
        The list of index values

    Returns
    -------
    dict[int, pd.DataFrame]
        A mapping of year to UMN Lakes product dataframe
    """
    for year, umn_lakes_product_df in year_to_umn_lakes_product_df.items():
        year_to_umn_lakes_product_df[year]  = filter_df_by_index(
                                                umn_lakes_product_df,
                                                index_name,
                                                index_values,
                                            )

    return year_to_umn_lakes_product_df


# ----------------------------------------------------------------------
# builder functions
# ----------------------------------------------------------------------
def build_year_to_umn_lakes_product_df(
    umn_lakes_product_tsv_paths: list[Path],
) -> dict[int, pd.DataFrame]:
    """
    Build a mapping of year to UMN Lakes product dataframe.

    Parameters
    ----------
    umn_lakes_product_tsv_paths : list[Path]
        The UMN Lakes product tsv paths

    Returns
    -------
    dict[int, pd.DataFrame]
        A mapping of year to UMN Lakes product dataframe
    """
    year_to_df = {}

    for path in umn_lakes_product_tsv_paths:
        year    = int(
                    path
                    .stem
                    .split("_")
                    [UMN_LAKES_PRODUCT_STEM_INDEX_YEAR],
                )
        df      = read_umn_lakes_product_tsv(path)

        year_to_df[year] = df

    return year_to_df


def build_year_to_distinct_start_days_ser(
    umn_lakes_id:   str,
    years:          list[int],
    connection:     psycopg.Connection,
) -> dict[int, pd.Series[int]]:
    """
    Build a mapping of year to distinct start days series.

    Parameters
    ----------
    umn_lakes_id : str
        The UMN Lakes id
    years : list[int]
        The list of years
    connection : psycopg.Connection
        The connection

    Returns
    -------
    dict[int, pd.Series[int]]
        A mapping of year to distinct start days series
    """
    year_to_ser = {}

    for year in years:
        ser = query_umn_lakes_distinct_start_days(
                umn_lakes_id,
                year,
                connection,
            )

        year_to_ser[year] = ser

    return year_to_ser


# ----------------------------------------------------------------------
# comprehender functions
# ----------------------------------------------------------------------
def comprehend_plotter_fns(
    *,
    years:                              list[int],
    year_to_umn_lakes_a4_product_df:    dict[int, pd.DataFrame],
    year_to_umn_lakes_cl_product_df:    dict[int, pd.DataFrame],
    year_to_umn_lakes_sd_product_df:    dict[int, pd.DataFrame],
    year_to_distinct_start_days_ser:    dict[int, pd.Series[int]],
) -> list[Callable[[Axes], None]]:
    """
    Comprehend a list of plotter functions.

    Parameters
    ----------
    years : list[int]
        The list of years
    year_to_umn_lakes_a4_product_df : dict[int, pd.DataFrame]
        The mapping of year to UMN Lakes A4 product dataframe.
    year_to_umn_lakes_cl_product_df : dict[int, pd.DataFrame]
        The mapping of year to UMN Lakes CL product dataframe.
    year_to_umn_lakes_sd_product_df : dict[int, pd.DataFrame]
        The mapping of year to UMN Lakes SD product dataframe.
    year_to_distinct_start_days_ser : dict[int, pd.Series[int]]
        The mapping of year to distinct label series.

    Returns
    -------
    list[Callable[[Axes], None]]
        A list of plotter functions
    """
    fns = [
            partial(
                plot_ax,
                umn_lakes_a4_product_df = year_to_umn_lakes_a4_product_df[year],
                umn_lakes_cl_product_df = year_to_umn_lakes_cl_product_df[year],
                umn_lakes_sd_product_df = year_to_umn_lakes_sd_product_df[year],
                distinct_start_days_ser = year_to_distinct_start_days_ser[year],
                year                    = year,
            )
            for year
            in years
        ]

    return fns


def comprehend_decorator_fns(
    *,
    years: list[int],
) -> list[Callable[[Axes], None]]:
    """
    Comprehend a list of decorator functions.

    Parameters
    ----------
    years : list[int]
        The list of years

    Returns
    -------
    list[Callable[[Axes], None]]
        A list of decorator functions
    """
    fns = [
            partial(
                decorate_ax,
                year = year,
            )
            for year
            in years
        ]

    return fns


# ----------------------------------------------------------------------
# plotter functions
# ----------------------------------------------------------------------
def plot_ax(
    ax: Axes,
    *,
    umn_lakes_a4_product_df:    pd.DataFrame,
    umn_lakes_cl_product_df:    pd.DataFrame,
    umn_lakes_sd_product_df:    pd.DataFrame,
    distinct_start_days_ser:    pd.Series[int],
    year:                       int,
) -> None:
    """
    Plot onto an axes.

    Parameters
    ----------
    ax : Axes
        The axes
    umn_lakes_a4_product_df : pd.DataFrame
        The UMN Lakes A4 product dataframe
    umn_lakes_cl_product_df : pd.DataFrame
        The UMN Lakes CL product dataframe
    umn_lakes_sd_product_df : pd.DataFrame
        The UMN Lakes SD product dataframe
    distinct_start_days_ser : pd.Series[int]
        The distinct start days series
    """
    plot_umn_lakes_product_df(
        ax,
        umn_lakes_product_df    = umn_lakes_a4_product_df,
        color                   = "red",
    )
    plot_umn_lakes_product_df(
        ax,
        umn_lakes_product_df    = umn_lakes_cl_product_df,
        color                   =  "green",
    )
    plot_umn_lakes_product_df(
        ax,
        umn_lakes_product_df    = umn_lakes_sd_product_df,
        color                   = "blue",
    )
    plot_distinct_start_days_ser(
        ax,
        distinct_start_days_ser = distinct_start_days_ser,
        year                    = year,
        color                   = GREY_DARK,
    )


def plot_umn_lakes_product_df(
    ax: Axes,
    *,
    umn_lakes_product_df:   pd.DataFrame,
    color:                  ColorType,
) -> None:
    """
    Plot a UMN Lakes product dataframe.

    Parameters
    ----------
    ax : Axes
        The axes
    umn_lakes_product_df : pd.DataFrame
        The UMN Lakes product dataframe
    color : ColorType
        The color
    """
    x   = pd.to_datetime(
            (
                umn_lakes_product_df
                .index
                .get_level_values(UMN_LAKES_PRODUCT_COLUMN_NAME_DATE)
                .astype(str)
            ),
            format = DATE_FORMAT_YYYYMMDD,
        )
    y   = umn_lakes_product_df[UMN_LAKES_PRODUCT_COLUMN_NAME_V50P]

    ax.scatter(
        x       = x,
        y       = y,
        color   = color,
    )


def plot_distinct_start_days_ser(
    ax: Axes,
    *,
    distinct_start_days_ser:    pd.Series[int],
    year:                       int,
    color:                      ColorType,
) -> None:
    """
    Plot a distinct start days series.

    Parameters
    ----------
    ax : Axes
        The axes
    distinct_start_days_ser : pd.Series[int]
        The distinct start days series
    color : ColorType
        The color
    """
    for distinct_start_day in distinct_start_days_ser:
        x   = pd.to_datetime(
                f"{year}{distinct_start_day:03d}",
                format = DATE_FORMAT_YYYYJJJ,
            )

        ax.axvline(
            x       = date2num(x),  # type: ignore[arg-type]
            color   = color,
        )


# ----------------------------------------------------------------------
# decorator functions
# ----------------------------------------------------------------------
def decorate_ax(
    ax: Axes,
    *,
    year: int,
) -> None:
    """
    Decorate an axes.

    Parameters
    ----------
    ax : Axes
        The axes
    year : int
        The year
    """
    ax.set_xlim(
        date2num(pd.Timestamp(year,  1,  1)),   # type: ignore[arg-type]
        date2num(pd.Timestamp(year, 12, 31)),   # type: ignore[arg-type]
    )

    ax.set_ylabel(
        str(year),
        fontsize = FONTSIZE_AXIS_LABEL,
    )
    ax.set_xlabel(
        "",
        fontsize = FONTSIZE_AXIS_LABEL,
    )

    ax.set_xticks([])
    ax.set_yticks([])


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

    umn_lakes_id                = args.umn_lakes_id
    umn_lakes_product_dir_path  = args.umn_lakes_product_dir_path
    output                      = args.output

    a4_product_tsv_paths    = list(umn_lakes_product_dir_path.glob(UMN_LAKES_PRODUCT_GLOB_PATTERN_A4))
    cl_product_tsv_paths    = list(umn_lakes_product_dir_path.glob(UMN_LAKES_PRODUCT_GLOB_PATTERN_CL))
    sd_product_tsv_paths    = list(umn_lakes_product_dir_path.glob(UMN_LAKES_PRODUCT_GLOB_PATTERN_SD))

    year_to_a4_product_df   = build_year_to_umn_lakes_product_df(a4_product_tsv_paths)
    year_to_cl_product_df   = build_year_to_umn_lakes_product_df(cl_product_tsv_paths)
    year_to_sd_product_df   = build_year_to_umn_lakes_product_df(sd_product_tsv_paths)

    year_to_a4_product_df   = filter_year_to_umn_lakes_product_df_by_index(
                                year_to_a4_product_df,
                                UMN_LAKES_PRODUCT_COLUMN_NAME_UNMLKNUM,
                                [umn_lakes_id],
                            )
    year_to_cl_product_df   = filter_year_to_umn_lakes_product_df_by_index(
                                year_to_cl_product_df,
                                UMN_LAKES_PRODUCT_COLUMN_NAME_UNMLKNUM,
                                [umn_lakes_id],
                            )
    year_to_sd_product_df   = filter_year_to_umn_lakes_product_df_by_index(
                                year_to_sd_product_df,
                                UMN_LAKES_PRODUCT_COLUMN_NAME_UNMLKNUM,
                                [umn_lakes_id],
                            )

    years   = sorted(
                    year_to_a4_product_df.keys()
                &   year_to_cl_product_df.keys()
                &   year_to_sd_product_df.keys(),
            )

    with psycopg.connect(os.environ["POSTGRESQL_URL"]) as connection:
        year_to_distinct_start_days_ser = build_year_to_distinct_start_days_ser(
                                            umn_lakes_id,
                                            years,
                                            connection,
                                        )

    plotter_fns     = comprehend_plotter_fns(
                        years                           = years,
                        year_to_umn_lakes_a4_product_df = year_to_a4_product_df,
                        year_to_umn_lakes_cl_product_df = year_to_cl_product_df,
                        year_to_umn_lakes_sd_product_df = year_to_sd_product_df,
                        year_to_distinct_start_days_ser = year_to_distinct_start_days_ser,
                    )
    decorator_fns   = comprehend_decorator_fns(
                        years = years,
                    )

    fig = build_figure(
            nrows           = len(years),
            ncols           = 1,
            plotter_fns     = plotter_fns,
            decorator_fns   = decorator_fns,
        )

    to_svg(
        fig,
        output_file_path = output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
