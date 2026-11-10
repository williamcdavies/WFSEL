"""
Filename:   view_umn_lakes_observations.py
Author:     William Chuter-Davies
Modified:   10/11/26
"""

# Standard Library Imports
import sys

from argparse   import (
                    ArgumentParser,
                    Namespace,
                )
from pathlib    import Path

# Related Third-party Imports
import matplotlib.pyplot    as plt
import pandas               as pd

from matplotlib.axes    import Axes
from matplotlib.figure  import Figure

# Local Application/Library Specific Imports
from wfsel.arguments                    import add_argument_output
from wfsel.exit_codes                   import (
                                            EXIT_FAILURE,
                                            EXIT_SUCCESS,
                                        )
from wfsel.io.writers                   import to_svg
from wfsel.plot.literals                import (
                                            FONTSIZE_AXIS_LABEL,
                                            FONTSIZE_TICK_LABEL,
                                        )
from wfsel.sources.umn_lakes.arguments  import (
                                            add_argument_umn_lakes_id,
                                            add_argument_umn_lakes_product_dir_path,
                                        )
from wfsel.sources.umn_lakes.literals   import (
                                            UMN_LAKES_PRODUCT_GLOB_PATTERN_A4,
                                            UMN_LAKES_PRODUCT_GLOB_PATTERN_CL,
                                            UMN_LAKES_PRODUCT_GLOB_PATTERN_SD,
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_DATE,
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_UNMLKNUM,
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_V25P,
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_V50P,
                                            UMN_LAKES_PRODUCT_COLUMN_NAME_V75P,
                                        )
from wfsel.sources.umn_lakes.readers    import read_umn_lakes_product_tsv
from wfsel.time.literals                import DATE_FORMAT_YMD
from wfsel.utils.argparse_utils         import (
                                            arguments_are_valid as _arguments_are_valid,
                                            build_parser        as _build_parser,
                                            argument_is_dir,
                                            argument_is_valid_umn_lakes_id,
                                        )

PROG    = "view_umn_lakes_observations.py"
DESC    = ""

SD_PRODUCT_AX_XAXIS_LABEL   = ""
SD_PRODUCT_AX_YAXIS_LABEL   = "Secchi Depth ()"

CL_PRODUCT_AX_XAXIS_LABEL   = ""
CL_PRODUCT_AX_YAXIS_LABEL   = "Chlorophyll-a ()"

A4_PRODUCT_AX_XAXIS_LABEL   = "Date"
A4_PRODUCT_AX_YAXIS_LABEL   = "A440 CDOM ()"


# ----------------------------------------------------------------------
# argument functions
# ----------------------------------------------------------------------
def add_argument_stacked(
    parser: ArgumentParser,
) -> None:
    """
    Add a "stacked" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "-s", "--stacked",
        action = "store_true",
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
                    add_argument_stacked,
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
# builder functions
# ----------------------------------------------------------------------
def build_umn_lakes_product_df(
    umn_lakes_id:                   int,
    umn_lakes_product_tsv_paths:    list[Path],
) -> pd.DataFrame | None:
    """
    Build a UMN Lakes product dataframe.

    Parameters
    ----------
    umn_lakes_id : int
        The UMN Lakes ID
    umn_lakes_product_tsv_paths : list[Path]
        The list of UMN Lakes product tsv paths

    Returns
    -------
    pd.DataFrame | None
        A dataframe, or None if build fails
    """
    dfs = []

    for path in umn_lakes_product_tsv_paths:
        df = read_umn_lakes_product_tsv(path)

        if str(umn_lakes_id) not in (
                                        df
                                        .index
                                        .get_level_values(UMN_LAKES_PRODUCT_COLUMN_NAME_UNMLKNUM)
                                    ):
            continue

        df = df.xs(
            str(umn_lakes_id),
            level = UMN_LAKES_PRODUCT_COLUMN_NAME_UNMLKNUM,
        )

        dfs.append(df)

    if not dfs:
        return None

    df = pd.concat(dfs)

    return df


def build_figure_stacked(
    *,
    umn_lakes_sd_product_df:    pd.DataFrame | None,
    umn_lakes_cl_product_df:    pd.DataFrame | None,
    umn_lakes_a4_product_df:    pd.DataFrame | None,
) -> Figure:
    """
    Build a figure (stacked).

    Parameters
    ----------
    umn_lakes_sd_product_df : pd.DataFrame | None
        The UMN Lakes SD product dataframe
    umn_lakes_cl_product_df : pd.DataFrame | None
        The UMN Lakes CL product dataframe
    umn_lakes_a4_product_df : pd.DataFrame | None
        The UMN Lakes A4 product dataframe

    Returns
    -------
    Figure
        A figure
    """
    (
        fig,
        (
            sd_product_ax,
            cl_product_ax,
            a4_product_ax,
        ),
    )   = plt.subplots(
            nrows   = 3,
            ncols   = 1,
            sharex  = True,
            sharey  = False,
        )

    if umn_lakes_sd_product_df is not None:
        plot_umn_lakes_sd_product_ax_stacked(sd_product_ax, umn_lakes_sd_product_df)

    if umn_lakes_cl_product_df is not None:
        plot_umn_lakes_cl_product_ax_stacked(cl_product_ax, umn_lakes_cl_product_df)

    if umn_lakes_a4_product_df is not None:
        plot_umn_lakes_a4_product_ax_stacked(a4_product_ax, umn_lakes_a4_product_df)

    decorate_umn_lakes_sd_product_ax(sd_product_ax)
    decorate_umn_lakes_cl_product_ax(cl_product_ax)
    decorate_umn_lakes_a4_product_ax(a4_product_ax)

    fig.subplots_adjust(hspace = 0.25)
    fig.align_xlabels()
    fig.align_ylabels()

    return fig


def build_figure_unstacked(
    *,
    umn_lakes_sd_product_df:    pd.DataFrame | None,
    umn_lakes_cl_product_df:    pd.DataFrame | None,
    umn_lakes_a4_product_df:    pd.DataFrame | None,
) -> Figure:
    """
    Build a figure (unstacked).

    Parameters
    ----------
    umn_lakes_sd_product_df : pd.DataFrame | None
        The UMN Lakes SD product dataframe
    umn_lakes_cl_product_df : pd.DataFrame | None
        The UMN Lakes CL product dataframe
    umn_lakes_a4_product_df : pd.DataFrame | None
        The UMN Lakes A4 product dataframe

    Returns
    -------
    Figure
        A figure
    """
    (
        fig,
        (
            sd_product_ax,
            cl_product_ax,
            a4_product_ax,
        ),
    )   = plt.subplots(
            nrows   = 3,
            ncols   = 1,
            sharex  = True,
            sharey  = False,
        )

    if umn_lakes_sd_product_df is not None:
        plot_umn_lakes_sd_product_ax_unstacked(sd_product_ax, umn_lakes_sd_product_df)

    if umn_lakes_cl_product_df is not None:
        plot_umn_lakes_cl_product_ax_unstacked(cl_product_ax, umn_lakes_cl_product_df)

    if umn_lakes_a4_product_df is not None:
        plot_umn_lakes_a4_product_ax_unstacked(a4_product_ax, umn_lakes_a4_product_df)

    decorate_umn_lakes_sd_product_ax(sd_product_ax)
    decorate_umn_lakes_cl_product_ax(cl_product_ax)
    decorate_umn_lakes_a4_product_ax(a4_product_ax)

    fig.subplots_adjust(hspace = 0.25)
    fig.align_xlabels()
    fig.align_ylabels()

    return fig


# ----------------------------------------------------------------------
# plotter functions
# ----------------------------------------------------------------------
def plot_umn_lakes_product_scatter_stacked(
    umn_lakes_product_ax:   Axes,
    umn_lakes_product_df:   pd.DataFrame,
) -> None:
    """
    Plot a UMN Lakes product scatter (stacked).

    Parameters
    ----------
    umn_lakes_product_ax : Axes
        The UMN Lakes product axes
    umn_lakes_product_df : pd.DataFrame
        The UMN Lakes product dataframe
    """
    x   = pd.to_datetime(
            (
                umn_lakes_product_df
                .index
                .get_level_values(UMN_LAKES_PRODUCT_COLUMN_NAME_DATE)
                .astype(str)
            ),
            format = DATE_FORMAT_YMD,
        )
    x   = pd.to_datetime("9999" + x.strftime(r"%m%d"))

    y_v25p  = umn_lakes_product_df[UMN_LAKES_PRODUCT_COLUMN_NAME_V25P]
    y_v50p  = umn_lakes_product_df[UMN_LAKES_PRODUCT_COLUMN_NAME_V50P]
    y_v75p  = umn_lakes_product_df[UMN_LAKES_PRODUCT_COLUMN_NAME_V75P]

    umn_lakes_product_ax.scatter(x, y_v25p, color = "blue")
    umn_lakes_product_ax.scatter(x, y_v50p, color = "green")
    umn_lakes_product_ax.scatter(x, y_v75p, color = "red")


def plot_umn_lakes_product_scatter_unstacked(
    umn_lakes_product_ax:   Axes,
    umn_lakes_product_df:   pd.DataFrame,
) -> None:
    """
    Plot a UMN Lakes product scatter (unstacked).

    Parameters
    ----------
    umn_lakes_product_ax : Axes
        The UMN Lakes product axes
    umn_lakes_product_df : pd.DataFrame
        The UMN Lakes product dataframe
    """
    x   = pd.to_datetime(
            (
                umn_lakes_product_df
                .index
                .get_level_values(UMN_LAKES_PRODUCT_COLUMN_NAME_DATE)
                .astype(str)
            ),
            format = DATE_FORMAT_YMD,
        )

    y_v25p  = umn_lakes_product_df[UMN_LAKES_PRODUCT_COLUMN_NAME_V25P]
    y_v50p  = umn_lakes_product_df[UMN_LAKES_PRODUCT_COLUMN_NAME_V50P]
    y_v75p  = umn_lakes_product_df[UMN_LAKES_PRODUCT_COLUMN_NAME_V75P]

    umn_lakes_product_ax.scatter(x, y_v25p, color = "blue")
    umn_lakes_product_ax.scatter(x, y_v50p, color = "green")
    umn_lakes_product_ax.scatter(x, y_v75p, color = "red")


def plot_umn_lakes_sd_product_ax_stacked(
    umn_lakes_sd_product_ax:    Axes,
    umn_lakes_sd_product_df:    pd.DataFrame,
) -> None:
    """
    Plot onto an UMN Lakes SD product axes (stacked).

    Parameters
    ----------
    umn_lakes_sd_product_ax : Axes
        The UMN Lakes SD product axes
    umn_lakes_sd_product_df : pd.DataFrame
        The UMN Lakes SD product dataframe
    """
    plot_umn_lakes_product_scatter_stacked(
        umn_lakes_sd_product_ax,
        umn_lakes_sd_product_df,
    )


def plot_umn_lakes_cl_product_ax_stacked(
    umn_lakes_cl_product_ax:    Axes,
    umn_lakes_cl_product_df:    pd.DataFrame,
) -> None:
    """
    Plot onto an UMN Lakes CL product axes (stacked).

    Parameters
    ----------
    umn_lakes_cl_product_ax : Axes
        The UMN Lakes CL product axes
    umn_lakes_cl_product_df : pd.DataFrame
        The UMN Lakes CL product dataframe
    """
    plot_umn_lakes_product_scatter_stacked(
        umn_lakes_cl_product_ax,
        umn_lakes_cl_product_df,
    )


def plot_umn_lakes_a4_product_ax_stacked(
    umn_lakes_a4_product_ax:    Axes,
    umn_lakes_a4_product_df:    pd.DataFrame,
) -> None:
    """
    Plot onto an UMN Lakes A4 product axes (stacked).

    Parameters
    ----------
    umn_lakes_a4_product_ax : Axes
        The UMN Lakes A4 product axes
    umn_lakes_a4_product_df : pd.DataFrame
        The UMN Lakes A4 product dataframe
    """
    plot_umn_lakes_product_scatter_stacked(
        umn_lakes_a4_product_ax,
        umn_lakes_a4_product_df,
    )


def plot_umn_lakes_sd_product_ax_unstacked(
    umn_lakes_sd_product_ax:    Axes,
    umn_lakes_sd_product_df:    pd.DataFrame,
) -> None:
    """
    Plot onto an UMN Lakes SD product axes (unstacked).

    Parameters
    ----------
    umn_lakes_sd_product_ax : Axes
        The UMN Lakes SD product axes
    umn_lakes_sd_product_df : pd.DataFrame
        The UMN Lakes SD product dataframe
    """
    plot_umn_lakes_product_scatter_unstacked(
        umn_lakes_sd_product_ax,
        umn_lakes_sd_product_df,
    )


def plot_umn_lakes_cl_product_ax_unstacked(
    umn_lakes_cl_product_ax:    Axes,
    umn_lakes_cl_product_df:    pd.DataFrame,
) -> None:
    """
    Plot onto an UMN Lakes CL product axes (unstacked).

    Parameters
    ----------
    umn_lakes_cl_product_ax : Axes
        The UMN Lakes CL product axes
    umn_lakes_cl_product_df : pd.DataFrame
        The UMN Lakes CL product dataframe
    """
    plot_umn_lakes_product_scatter_unstacked(
        umn_lakes_cl_product_ax,
        umn_lakes_cl_product_df,
    )


def plot_umn_lakes_a4_product_ax_unstacked(
    umn_lakes_a4_product_ax:    Axes,
    umn_lakes_a4_product_df:    pd.DataFrame,
) -> None:
    """
    Plot onto an UMN Lakes A4 product axes (unstacked).

    Parameters
    ----------
    umn_lakes_a4_product_ax : Axes
        The UMN Lakes A4 product axes
    umn_lakes_a4_product_df : pd.DataFrame
        The UMN Lakes A4 product dataframe
    """
    plot_umn_lakes_product_scatter_unstacked(
        umn_lakes_a4_product_ax,
        umn_lakes_a4_product_df,
    )


# ----------------------------------------------------------------------
# decorator functions
# ----------------------------------------------------------------------
def decorate_umn_lakes_sd_product_ax(
    umn_lakes_sd_product_ax: Axes,
) -> None:
    """
    Decorate an UMN Lakes SD product axes.

    Parameters
    ----------
    umn_lakes_sd_product_ax : Axes
        The UMN Lakes SD product axes
    """
    umn_lakes_sd_product_ax.set_xlabel(SD_PRODUCT_AX_XAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    umn_lakes_sd_product_ax.set_ylabel(SD_PRODUCT_AX_YAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    umn_lakes_sd_product_ax.tick_params(labelsize = FONTSIZE_TICK_LABEL)


def decorate_umn_lakes_cl_product_ax(
    umn_lakes_cl_product_ax: Axes,
) -> None:
    """
    Decorate an UMN Lakes CL product axes.

    Parameters
    ----------
    umn_lakes_cl_product_ax : Axes
        The UMN Lakes CL product axes
    """
    umn_lakes_cl_product_ax.set_xlabel(CL_PRODUCT_AX_XAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    umn_lakes_cl_product_ax.set_ylabel(CL_PRODUCT_AX_YAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    umn_lakes_cl_product_ax.tick_params(labelsize = FONTSIZE_TICK_LABEL)


def decorate_umn_lakes_a4_product_ax(
    umn_lakes_a4_product_ax: Axes,
) -> None:
    """
    Decorate an UMN Lakes A4 product axes.

    Parameters
    ----------
    umn_lakes_a4_product_ax : Axes
        The UMN Lakes A4 product axes
    """
    umn_lakes_a4_product_ax.set_xlabel(A4_PRODUCT_AX_XAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    umn_lakes_a4_product_ax.set_ylabel(A4_PRODUCT_AX_YAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    umn_lakes_a4_product_ax.tick_params(labelsize = FONTSIZE_TICK_LABEL)


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

    sd_product_tsv_paths    = args.umn_lakes_product_dir_path.glob(UMN_LAKES_PRODUCT_GLOB_PATTERN_SD)
    cl_product_tsv_paths    = args.umn_lakes_product_dir_path.glob(UMN_LAKES_PRODUCT_GLOB_PATTERN_CL)
    a4_product_tsv_paths    = args.umn_lakes_product_dir_path.glob(UMN_LAKES_PRODUCT_GLOB_PATTERN_A4)

    sd_product_df   = build_umn_lakes_product_df(
                        args.umn_lakes_id,
                        sd_product_tsv_paths,
                    )
    cl_product_df   = build_umn_lakes_product_df(
                        args.umn_lakes_id,
                        cl_product_tsv_paths,
                    )
    a4_product_df   = build_umn_lakes_product_df(
                        args.umn_lakes_id,
                        a4_product_tsv_paths,
                    )

    if args.stacked:
        fig = build_figure_stacked(
                umn_lakes_sd_product_df = sd_product_df,
                umn_lakes_cl_product_df = cl_product_df,
                umn_lakes_a4_product_df = a4_product_df,
            )
    else:
        fig = build_figure_unstacked(
                umn_lakes_sd_product_df = sd_product_df,
                umn_lakes_cl_product_df = cl_product_df,
                umn_lakes_a4_product_df = a4_product_df,
            )

    to_svg(
        fig,
        args.output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
