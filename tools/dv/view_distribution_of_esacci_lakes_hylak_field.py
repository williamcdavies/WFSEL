r"""
view_distribution_of_esacci_lakes_hylak_field.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

# Related Third-party Imports
import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd

from matplotlib.axes   import Axes
from matplotlib.figure import Figure

# Local Application/Library Specific Imports
from lib.dataframe.utils         import (
    get_quantiles_from_ser,
    get_ser_from_df
)
from lib.esacci_lakes.utils.proc import (
    add_argument_esacci_lakes_hylak_fields_csv_path,
    add_argument_hylak_field,
    argument_esacci_lakes_hylak_fields_csv_path_exists,
    argument_hylak_field_is_in_hylak_fields,
    read_esacci_lakes_hylak_fields_csv
)
from lib.esacci_lakes.vars       import HYLAK_FIELDS
from lib.plot.utils              import (
    save_figure,
    set_ax_xscale_to_linear,
    set_ax_xscale_to_log
)
from lib.plot.vars               import AXIS_SCALES
from lib.proc.utils              import (
    arguments_are_valid as _arguments_are_valid,
    build_parser        as _build_parser,

    add_argument_output,
    argument_output_is_file_or_missing
)
from lib.proc.vars               import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)


# Constants
# ==================================================================================================
PROG = "view_distribution_of_esacci_lakes_hylak_field.py"


# ==================================================================================================


# Parser functions
# ==================================================================================================
def add_argument_scale(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `scale` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `scale` is of type :class:`str`.
    """
    parser.add_argument(
        "scale",
        type = str,
        help = f"one of {", ".join(AXIS_SCALES)}"
    )


def build_parser(
) -> argparse.ArgumentParser:
    """
    Builds a :class:`argparse.ArgumentParser`.

    Returns
    -------
    A :class:`argparse.ArgumentParser`.
    """
    return _build_parser(
        PROG,
        "Produces a distribution visualisation of a HydroLAKES field of all lakes in spatial.esacci_lakes (Same lakes as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0)",
        positional_arguments = [
            add_argument_hylak_field,
            add_argument_esacci_lakes_hylak_fields_csv_path,
            add_argument_scale
        ],
        optional_arguments   = [
            add_argument_output
        ]
    )


# ==================================================================================================


# Plot functions
# ==================================================================================================
def plot_on_box_ax(
    box_ax:                Axes,
    hylak_field_ser:       pd.Series,
    hylak_field_quantiles: list[float]
) -> None:
    """
    Plots a box and whisker plot and quantile lines of
    `hylak_field_ser` onto `box_ax`.

    Parameters
    ----------
    box_ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    hylak_field_ser : :class:`pandas.Series`
        The series

    hylak_field_quantiles : list[:class:`float`]
        The quantile values to draw lines at

    Returns
    -------
    None.
    """
    plot_ser_boxplot(
        box_ax,
        hylak_field_ser
    )
    plot_quantile_lines(
        box_ax,
        hylak_field_quantiles,
        [
            "Q1",
            "Q2",
            "Q3"
        ]
    )


def plot_on_hist_ax(
    hist_ax:               Axes,
    hylak_field_ser:       pd.Series,
    hylak_field_quantiles: list[float],
    scale:                 str
) -> None:
    """
    Plots a histogram and quantile lines of `hylak_field_ser` onto
    `hist_ax`, using `scale`.

    Parameters
    ----------
    hist_ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    hylak_field_ser : :class:`pandas.Series`
        The series

    hylak_field_quantiles : list[:class:`float`]
        The quantile values to draw lines at

    scale : :class:`str`
        One of `AXIS_SCALES`

    Returns
    -------
    None.

    Raises
    ------
    ValueError
        If `scale` is not in `AXIS_SCALES`.
    """
    if scale == "linear":
        plot_ser_histogram_linear(
            hist_ax,
            hylak_field_ser
        )
    elif scale == "log":
        plot_ser_histogram_log(
            hist_ax,
            hylak_field_ser
        )
    else:
        raise ValueError(f"expected `scale` to be one of {", ".join(AXIS_SCALES)}: {scale}")

    plot_quantile_lines(
        hist_ax,
        hylak_field_quantiles,
        [
            "Q1",
            "Q2",
            "Q3"
        ]
    )


def plot_quantile_lines(
    ax:        Axes,
    quantiles: list[float],
    labels:    list[str]
) -> None:
    """
    Plots vertical dotted lines on `ax` at each of `quantiles`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    quantiles : list[:class:`float`]
        The values to draw lines at

    labels : list[:class:`str`]
        The label for each of `quantiles`

    Returns
    -------
    None.
    """
    cmap = plt.get_cmap("tab10")

    for (
        i,
        (
            quantile,
            label
        )
    ) in enumerate(
        zip(
            quantiles,
            labels
        )
    ):
        ax.axvline(
            x         = quantile,
            color     = cmap(i),
            linestyle = ":",
            label     = f"{label}: {quantile:.3e}"
        )


def plot_ser_boxplot(
    ax:  Axes,
    ser: pd.Series
) -> None:
    """
    Plots a box and whisker plot of `ser` onto `ax`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    ser : :class:`pandas.Series`
        The series

    Returns
    -------
    None.
    """
    ax.boxplot(
        x           = ser.dropna(),
        orientation = "horizontal"
    )


def plot_ser_histogram_linear(
    ax:  Axes,
    ser: pd.Series
) -> None:
    """
    Plots a histogram of `ser` onto `ax` with linearly spaced bins.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    ser : :class:`pandas.Series`
        The series

    Returns
    -------
    None.
    """
    ser  = ser.dropna()
    bins = 30

    ax.hist(
        x         = ser,
        bins      = bins,
        facecolor = "#FFFFFF",
        edgecolor = "#000000"
    )


def plot_ser_histogram_log(
    ax:  Axes,
    ser: pd.Series
) -> None:
    """
    Plots a histogram of `ser` onto `ax` with logarithmically spaced bins.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    ser : :class:`pandas.Series`
        The series

    Returns
    -------
    None.
    """
    ser  = ser.dropna()
    bins = np.logspace(
        np.log10(ser.min()),
        np.log10(ser.max()),
        30
    )

    ax.hist(
        x         = ser,
        bins      = bins,
        facecolor = "#FFFFFF",
        edgecolor = "#000000"
    )


def set_box_ax_properties(
    box_ax: Axes,
    scale:  str
) -> None:
    """
    Sets `box_ax`'s x-axis scale to `scale`.

    Parameters
    ----------
    box_ax : :class:`matplotlib.axes.Axes`
        The axes to set properties on

    scale : :class:`str`
        One of `AXIS_SCALES`

    Returns
    -------
    None.

    Raises
    ------
    ValueError
        If `scale` is not in `AXIS_SCALES`.
    """
    if scale == "linear":
        set_ax_xscale_to_linear(box_ax)
    elif scale == "log":
        set_ax_xscale_to_log(box_ax)
    else:
        raise ValueError(f"expected `scale` to be one of {", ".join(AXIS_SCALES)}: {scale}")


def set_fig_properties(
    fig:         Figure,
    hylak_field: str,
    scale:       str
) -> None:
    """
    Sets `fig`'s title from `hylak_field` and `scale`.

    Parameters
    ----------
    fig : :class:`matplotlib.figure.Figure`
        The figure to set properties on

    hylak_field : :class:`str`
        The HydroLAKES field id

    scale : :class:`str`
        One of `AXIS_SCALES`

    Returns
    -------
    None.
    """
    fig.suptitle(f"{scale.capitalize()} Distribution of {HYLAK_FIELDS[hylak_field].long_name}")


def set_hist_ax_properties(
    hist_ax: Axes,
    scale:   str
) -> None:
    """
    Sets `hist_ax`'s x-axis scale to `scale`.

    Parameters
    ----------
    hist_ax : :class:`matplotlib.axes.Axes`
        The axes to set properties on

    scale : :class:`str`
        One of `AXIS_SCALES`

    Returns
    -------
    None.

    Raises
    ------
    ValueError
        If `scale` is not in `AXIS_SCALES`.
    """
    if scale == "linear":
        set_ax_xscale_to_linear(hist_ax)
    elif scale == "log":
        set_ax_xscale_to_log(hist_ax)
    else:
        raise ValueError(f"expected `scale` to be one of {", ".join(AXIS_SCALES)}: {scale}")


# ==================================================================================================


# Validator functions
# ==================================================================================================
def argument_scale_is_in_axis_scales(
    scale: str,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `scale`.

    Parameters
    ----------
    scale : :class:`str`
        The argument `scale`

    loud : :class:`bool`
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `scale` is in `AXIS_SCALES`. `False` otherwise.
    """
    if scale in AXIS_SCALES:
        return True

    if loud:
        print(
            f"error: argument scale: not in {", ".join(AXIS_SCALES)}: {scale}",
            file = sys.stderr
        )

    return False


def arguments_are_valid(
    args: argparse.Namespace
) -> bool:
    """
    Validates `args`.

    Parameters
    ----------
    args : :class:`argparse.Namespace`
        The arguments

    Returns
    -------
    `True` if all arguments are successfully validated. `False` otherwise.
    """
    return _arguments_are_valid(
        args,
        [
            (
                argument_hylak_field_is_in_hylak_fields,
                "hylak_field"
            ),
            (
                argument_esacci_lakes_hylak_fields_csv_path_exists,
                "esacci_lakes_hylak_fields_csv_path"
            ),
            (
                argument_scale_is_in_axis_scales,
                "scale"
            ),
            (
                argument_output_is_file_or_missing,
                "output"
            )
        ]
    )


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser().parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    hylak_fields_df       = read_esacci_lakes_hylak_fields_csv(args.esacci_lakes_hylak_fields_csv_path)
    hylak_field_ser       = get_ser_from_df(
        hylak_fields_df,
        args.hylak_field
    )
    hylak_field_quantiles = get_quantiles_from_ser(
        hylak_field_ser,
        [
            0.25,
            0.5,
            0.75
        ]
    )

    fig, (hist_ax, box_ax) = plt.subplots(
        nrows       = 2,
        ncols       = 1,
        sharex      = True,
        gridspec_kw = {"height_ratios": [3, 1]}
    )

    plot_on_hist_ax(
        hist_ax,
        hylak_field_ser,
        hylak_field_quantiles,
        args.scale
    )
    plot_on_box_ax(
        box_ax,
        hylak_field_ser,
        hylak_field_quantiles
    )

    set_hist_ax_properties(
        hist_ax,
        args.scale
    )
    set_box_ax_properties(
        box_ax,
        args.scale
    )

    set_fig_properties(
        fig,
        args.hylak_field,
        args.scale
    )

    hist_ax.legend()

    save_figure(
        fig,
        args.output
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
