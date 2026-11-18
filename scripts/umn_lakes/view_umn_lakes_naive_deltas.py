"""
Filename:   view_umn_lakes_naive_deltas.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
import logging
import sys

from argparse           import (
                            ArgumentParser,
                            Namespace,
                        )
from collections.abc    import Callable
from functools          import partial
from pathlib            import Path

# Related Third-party Imports
import pandas   as pd

from matplotlib.axes import Axes

from wfsel.arguments            import add_argument_output
from wfsel.exit_codes           import (
                                    EXIT_FAILURE,
                                    EXIT_SUCCESS,
                                )
from wfsel.io.writers           import to_png
from wfsel.plot.builders        import build_figure
from wfsel.plot.literals        import (
                                    FONTSIZE_AXIS_LABEL,
                                    FONTSIZE_TICK_LABEL,
                                    FONTSIZE_TITLE,
                                )
from wfsel.utils.argparse_utils import (
                                    arguments_are_valid as _arguments_are_valid,
                                    build_parser        as _build_parser,
                                    argument_is_file,
                                )

PROG    = "view_umn_lakes_naive_deltas.py"
DESC    = ""

logging.basicConfig(
    stream  = sys.stderr,
    level   = logging.INFO,
)


# ----------------------------------------------------------------------
# argument functions
# ----------------------------------------------------------------------
def add_argument_umn_lakes_a4_naive_deltas_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "umn_lakes_a4_naive_deltas_csv_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "umn_lakes_a4_naive_deltas_csv_path",
        type    = Path,
        metavar = "PATH",
        help    = "umn_lakes_a4_naive_deltas_csv_path",
    )


def add_argument_umn_lakes_cl_naive_deltas_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "umn_lakes_cl_naive_deltas_csv_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "umn_lakes_cl_naive_deltas_csv_path",
        type    = Path,
        metavar = "PATH",
        help    = "umn_lakes_cl_naive_deltas_csv_path",
    )


def add_argument_umn_lakes_sd_naive_deltas_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "umn_lakes_sd_naive_deltas_csv_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "umn_lakes_sd_naive_deltas_csv_path",
        type    = Path,
        metavar = "PATH",
        help    = "umn_lakes_sd_naive_deltas_csv_path",
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
                                            add_argument_umn_lakes_a4_naive_deltas_csv_path,
                                            add_argument_umn_lakes_cl_naive_deltas_csv_path,
                                            add_argument_umn_lakes_sd_naive_deltas_csv_path,
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
                                    "umn_lakes_a4_naive_deltas_csv_path":   argument_is_file,
                                    "umn_lakes_cl_naive_deltas_csv_path":   argument_is_file,
                                    "umn_lakes_sd_naive_deltas_csv_path":   argument_is_file,
                                }

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


# ----------------------------------------------------------------------
# reader functions
# ----------------------------------------------------------------------
def read_umn_lakes_naive_deltas_csv(
    umn_lakes_naive_deltas_csv_path: Path,
) -> pd.DataFrame:
    """
    Read "a4_naive_deltas" (or similar) into a dataframe.

    Parameters
    ----------
    umn_lakes_naive_deltas_csv_path : Path
        The path to "a4_naive_deltas" (or similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df  = pd.read_csv(
            umn_lakes_naive_deltas_csv_path,
            index_col   = "index_col",
            dtype       = {"unmlknum": str},
        )

    return df


# ----------------------------------------------------------------------
# comprehender functions
# ----------------------------------------------------------------------
def comprehend_plotter_fns(
    *,
    umn_lakes_a4_naive_deltas_df:   pd.DataFrame,
    umn_lakes_cl_naive_deltas_df:   pd.DataFrame,
    umn_lakes_sd_naive_deltas_df:   pd.DataFrame,
) -> list[Callable[[Axes], None]]:
    """
    Comprehend a list of plotter functions.

    Parameters
    ----------
    umn_lakes_a4_naive_deltas_df : pd.DataFrame
        The UMN Lakes A4 naive deltas dataframe
    umn_lakes_cl_naive_deltas_df : pd.DataFrame
        The UMN Lakes CL naive deltas dataframe
    umn_lakes_sd_naive_deltas_df : pd.DataFrame
        The UMN Lakes SD naive deltas dataframe

    Returns
    -------
    list[Callable[[Axes], None]]
        A list of plotter functions
    """
    fns = [
            partial(plot_ax, umn_lakes_naive_deltas_df = umn_lakes_a4_naive_deltas_df),
            partial(plot_ax, umn_lakes_naive_deltas_df = umn_lakes_cl_naive_deltas_df),
            partial(plot_ax, umn_lakes_naive_deltas_df = umn_lakes_sd_naive_deltas_df),
        ]

    return fns


def comprehend_decorator_fns(
    *,
    titles:     list[str],
    xlabels:    list[str],
    ylabels:    list[str],
) -> list[Callable[[Axes], None]]:
    """
    Comprehend a list of decorator functions.

    Parameters
    ----------
    fields : list[str]
        The list of field names

    Returns
    -------
    list[Callable[[Axes], None]]
        A list of decorator functions
    """
    fns = [
            partial(
                decorate_ax,
                title   = title,
                xlabel  = xlabel,
                ylabel  = ylabel,
            )
            for (
                title,
                xlabel,
                ylabel,
            )
            in zip(
                titles,
                xlabels,
                ylabels,
                strict = True,
            )
        ]

    return fns


# ----------------------------------------------------------------------
# plotter functions
# ----------------------------------------------------------------------
def plot_ax(
    ax: Axes,
    *,
    umn_lakes_naive_deltas_df: pd.DataFrame,
) -> None:
    """
    Plot onto an axes.

    Parameters
    ----------
    ax : Axes
        The axes
    umn_lakes_naive_deltas_df : pd.DataFrame
        The UMN Lakes naive deltas dataframe
    """
    plot_umn_lakes_naive_deltas_df(
        ax,
        umn_lakes_naive_deltas_df = umn_lakes_naive_deltas_df,
    )


def plot_umn_lakes_naive_deltas_df(
    ax: Axes,
    *,
    umn_lakes_naive_deltas_df: pd.DataFrame,
) -> None:
    """
    Plot a UMN Lakes naive deltas dataframe.

    Parameters
    ----------
    ax : Axes
        The axes
    umn_lakes_naive_deltas_df : pd.DataFrame
        The UMN Lakes naive deltas dataframe
    """
    x = umn_lakes_naive_deltas_df["N"]
    y = umn_lakes_naive_deltas_df["delta"]


    ax.scatter(
        x   = x,
        y   = y,
        s   = 1,
    )

    ax.set_ylim(
        -y.abs().max(),
         y.abs().max(),
    )

# ----------------------------------------------------------------------
# decorator functions
# ----------------------------------------------------------------------
def decorate_ax(
    ax: Axes,
    *,
    title:  str,
    xlabel: str,
    ylabel: str,
) -> None:
    """
    Decorate an axes.

    Parameters
    ----------
    ax : Axes
        The axes
    field : str
        The field name
    """
    ax.set_title(
        title,
        fontsize = FONTSIZE_TITLE,
    )
    ax.set_xlabel(
        xlabel,
        fontsize = FONTSIZE_AXIS_LABEL,
    )
    ax.set_ylabel(
        ylabel,
        fontsize = FONTSIZE_AXIS_LABEL,
    )
    ax.tick_params(
        labelsize = FONTSIZE_TICK_LABEL,
    )


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

    umn_lakes_a4_naive_deltas_csv_path  = args.umn_lakes_a4_naive_deltas_csv_path
    umn_lakes_cl_naive_deltas_csv_path  = args.umn_lakes_cl_naive_deltas_csv_path
    umn_lakes_sd_naive_deltas_csv_path  = args.umn_lakes_sd_naive_deltas_csv_path
    output                              = args.output

    a4_naive_deltas_df  = read_umn_lakes_naive_deltas_csv(umn_lakes_a4_naive_deltas_csv_path)
    cl_naive_deltas_df  = read_umn_lakes_naive_deltas_csv(umn_lakes_cl_naive_deltas_csv_path)
    sd_naive_deltas_df  = read_umn_lakes_naive_deltas_csv(umn_lakes_sd_naive_deltas_csv_path)

    plotter_fns     = comprehend_plotter_fns(
                        umn_lakes_a4_naive_deltas_df    = a4_naive_deltas_df,
                        umn_lakes_cl_naive_deltas_df    = cl_naive_deltas_df,
                        umn_lakes_sd_naive_deltas_df    = sd_naive_deltas_df,
                    )
    decorator_fns   = comprehend_decorator_fns(
                        titles  = [
                                    "A440 CDOM",
                                    "Chlorophyll-a",
                                    "Secchi Depth",
                                ],
                        xlabels = [
                                    "",
                                    "",
                                    "N",
                                ],
                        ylabels = [
                                    "Delta",
                                    "Delta",
                                    "Delta",
                                ],
                    )

    fig = build_figure(
            nrows           = 3,
            ncols           = 1,
            plotter_fns     = plotter_fns,
            decorator_fns   = decorator_fns,
            figsize         = (6.4, 4.8),
            sharex          = True,
            sharey          = False,
        )

    to_png(
        fig,
        output_file_path = output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
