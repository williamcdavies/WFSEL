"""
view_distribution_of_esacci_lakes_over_hylak_field.py.

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse import (
    ArgumentParser,
    Namespace,
)

# Related Third-party Imports
import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd

from matplotlib.axes   import Axes
from matplotlib.figure import Figure

# Local Application/Library Specific Imports
from wfsel.exit_codes                     import (
    EXIT_FAILURE,
    EXIT_SUCCESS,
)
from wfsel.io.arguments                   import add_argument_output
from wfsel.io.writers                     import to_png
from wfsel.math.arguments                 import add_argument_scale
from wfsel.math.literals                  import SCALES
from wfsel.sources.esacci_lakes.arguments import add_argument_esacci_lakes_hylak_field_values_csv_path
from wfsel.sources.esacci_lakes.readers   import read_esacci_lakes_hylak_field_values_csv
from wfsel.sources.hydro_lakes.arguments  import add_argument_hylak_field
from wfsel.sources.hydro_lakes.models     import HYLAK_FIELDS
from wfsel.utils.argparse_utils           import (
    arguments_are_valid as _arguments_are_valid,
    build_parser        as _build_parser,
    argument_is_file,
    argument_is_member_of_set,
)
from wfsel.utils.pandas_utils             import compute_quantiles

PROG = "view_distribution_of_esacci_lakes_over_hylak_field.py"
DESC = ""


# ----------------------------------------------------------------------
# setup functions
# ----------------------------------------------------------------------
def build_parser(
) -> ArgumentParser:
    """
    Wrap build_parser.

    Returns
    -------
    ArgumentParser

    """
    parser = ArgumentParser(
        prog        = PROG,
        description = DESC,
        usage       = "%(prog)s [options]",
    )

    parser = _build_parser(
        parser,
        positional_arguments = [
            add_argument_hylak_field,
            add_argument_esacci_lakes_hylak_field_values_csv_path,
        ],
        optional_arguments   = [
            add_argument_scale,
            add_argument_output,
        ],
    )

    return parser


def arguments_are_valid(
    arguments: Namespace,
) -> bool:
    """
    Wrap arguments_are_valid.

    Parameters
    ----------
    arguments : Namespace
        The arguments

    Returns
    -------
    bool

    """
    argument_name_to_validator = {
        "hylak_field":                              argument_is_member_of_set(list(HYLAK_FIELDS.keys())),
        "esacci_lakes_hylak_field_values_csv_path": argument_is_file,
        "scale":                                    argument_is_member_of_set(SCALES),
    }

    boolean = _arguments_are_valid(
        arguments,
        argument_name_to_validator,
    )

    return boolean


# ----------------------------------------------------------------------
# plot functions
# ----------------------------------------------------------------------
def plot_quantiles(
    ax:        Axes,
    quantiles: list[float],
) -> None:
    """
    Plot quantiles on an Axes.

    Parameters
    ----------
    ax : Axes
        The Axes
    quantiles : list[float]
        The quantiles
    """
    cmap = plt.get_cmap("tab10")

    for (
        i,
        quantile,
    ) in enumerate(quantiles):
        ax.axvline(
            quantile,
            color     = cmap(i),
            label     = f"Q_{i + 1}: {quantile:.3e}",
            linestyle = ":",
        )


def plot_on_hist_ax(
    ax:        Axes,
    ser:       pd.Series,
    quantiles: list[float],
    scale:     str,
) -> None:
    """
    Plot on hist Axes.

    Parameters
    ----------
    ax : Axes
        The Axes
    ser : pd.Series
        The Series
    quantiles : list[float]
        The quantiles
    scale : str
        The scale

    Raises
    ------
    ValueError
        If scale is not in a list of valid scales
    """
    ser = ser.dropna()

    if scale == "linear":
        bins = 30
    elif scale == "log":
        bins = np.logspace(
            np.log10(ser.min()),
            np.log10(ser.max()),
            30,
        )
    else:
        message = f"expected scale to be in {SCALES}: got {scale}"

        raise ValueError(message)

    ax.hist(
        ser,
        bins      = bins,
        edgecolor = "#000000",
        facecolor = "#FFFFFF",
    )

    plot_quantiles(
        ax,
        quantiles,
    )


def plot_on_boxplot_ax(
    ax:        Axes,
    ser:       pd.Series,
    quantiles: list[float],
) -> None:
    """
    Plot on boxplot Axes.

    Parameters
    ----------
    ax : Axes
        The Axes
    ser : pd.Series
        The Series
    quantiles : list[float]
        The quantiles
    """
    ser = ser.dropna()

    ax.boxplot(
        ser,
        orientation = "horizontal",
    )

    plot_quantiles(
        ax,
        quantiles,
    )


# ----------------------------------------------------------------------
# set functions
# ----------------------------------------------------------------------
def set_ax_properties(
    ax:    Axes,
    scale: str,
) -> None:
    """
    Set Axes properties.

    Parameters
    ----------
    ax : Axes
        The Axes
    scale : str
        The scale

    Raises
    ------
    ValueError
        If scale is not in SCALES
    """
    if scale == "linear":
        ax.set_xscale("linear")
    elif scale == "log":
        ax.set_xscale("log")
    else:
        message = f"expected scale to be in {SCALES}: got {scale}"

        raise ValueError(message)


def set_hist_ax_properties(
    ax:    Axes,
    scale: str,
) -> None:
    """
    Set hist Axes properties.

    Parameters
    ----------
    ax : Axes
        The Axes
    scale : str
        The scale
    """
    set_ax_properties(
        ax,
        scale,
    )


def set_boxplot_ax_properties(
    ax:    Axes,
    scale: str,
) -> None:
    """
    Set boxplot Axes properties.

    Parameters
    ----------
    ax : Axes
        The Axes
    scale : str
        The scale
    """
    set_ax_properties(
        ax,
        scale,
    )


def set_fig_properties(
    fig:         Figure,
    hylak_field: str,
    scale:       str,
) -> None:
    """
    Set Figure properties.

    Parameters
    ----------
    fig : Figure
        The Figure
    hylak_field : str
        The HydroLAKES field
    scale : str
        The scale
    """
    fig.suptitle(f"{scale.capitalize()} Distribution of {HYLAK_FIELDS[hylak_field].long_name}")


# ----------------------------------------------------------------------
# entry point
# ----------------------------------------------------------------------
def main(
) -> int:
    """
    Entry point.

    Returns
    -------
    int

    """
    arguments = build_parser().parse_args()

    if not arguments_are_valid(arguments):
        return EXIT_FAILURE

    hylak_field_values_df  = read_esacci_lakes_hylak_field_values_csv(arguments.esacci_lakes_hylak_field_values_csv_path)
    hylak_field_values_ser = hylak_field_values_df[arguments.hylak_field]

    hylak_field_values_quantiles = compute_quantiles(
        hylak_field_values_ser,
        [
            0.25,
            0.5,
            0.75,
        ],
    )

    (
        fig,
        (
            hist_ax,
            boxplot_ax,
        ),
    ) = plt.subplots(
        nrows       = 2,
        ncols       = 1,
        sharex      = True,
        gridspec_kw = {"height_ratios": [
            3,
            1,
        ]},
    )

    plot_on_hist_ax(
        hist_ax,
        hylak_field_values_ser,
        hylak_field_values_quantiles,
        arguments.scale,
    )
    plot_on_boxplot_ax(
        boxplot_ax,
        hylak_field_values_ser,
        hylak_field_values_quantiles,
    )

    set_hist_ax_properties(
        hist_ax,
        arguments.scale,
    )
    set_boxplot_ax_properties(
        boxplot_ax,
        arguments.scale,
    )

    set_fig_properties(
        fig,
        arguments.hylak_field,
        arguments.scale,
    )

    hist_ax.legend()

    to_png(
        fig,
        arguments.output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
