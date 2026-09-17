r"""
view_distribution_of_esacci_lakes_hylak_field.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from datetime                  import datetime
from typing                    import Callable

# Related Third-party Imports
import matplotlib.pyplot       as plt
import numpy                   as np
import pandas                  as pd

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.io import (
    add_argument_hylak_field,
    add_argument_esacci_lakes_hylak_fields_csv_path,
    argument_hylak_field_is_in_hylak_fields,
    argument_esacci_lakes_hylak_fields_csv_path_exists,
    read_esacci_lakes_hylak_fields_csv
)
from lib.esacci_lakes.vars     import HYLAK_FIELDS
from lib.io.vars               import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)
from lib.math.utils            import (
    get_ser_from_df,
    get_quantiles_from_ser
)
from lib.math.vars             import SCALES
from lib.plot.utils            import (
    set_ax_xscale_to_lin,
    set_ax_xscale_to_log,
    save_figure
)

PROG = "view_distribution_of_esacci_lakes_hylak_field.py"
TIME = datetime.now()


# Argument functions
# ==================================================================================================
def add_argument_scale(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `scale` argument to a :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `scale` is of type :class:`str`.
    """
    parser.add_argument(
        "-s", "--scale",
        type=str,
        required=True,
        help=f"""one of {SCALES}"""
    )


def argument_scale_is_in_scales(
    scale: str,
    *,
    loud:   bool = False
) -> bool:
    """
    Validates `scale`.

    Parameters
    ----------
    scale : :class:`str`
        The argument `scale`

    loud : bool
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `scale` is in `SCALES`. `False` otherwise.
    """
    if scale in SCALES:
        return True

    if loud:
        print(f"""error: argument scale: not in {SCALES}: {scale}""")

    return False


def build_parser(
    prog: str
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG,
        usage="%(prog)s [options]",
        description="""Produces a distribution visualisation of a HydroLAKES field of all lakes in spatial.esacci_lakes (Same lakes as provided by ESA Lakes Climate Change Initiative (esacci_lakes): Lake products, Version 3.0)"""
    )

    # Positional arguments
    add_argument_hylak_field(parser)
    add_argument_esacci_lakes_hylak_fields_csv_path(parser)

    # Optinal arguments
    add_argument_scale(parser)

    return parser


def arguments_are_valid(
    args: argparse.Namespace
) -> bool:
    """
    Validates `args`.

    Returns
    -------
    `True` if all arguments are successfully validated. `False`
    otherwise.
    """
    if not argument_hylak_field_is_in_hylak_fields(
        args.hylak_field,
        loud=True
    ):
        return False

    if not argument_esacci_lakes_hylak_fields_csv_path_exists(
        args.esacci_lakes_hylak_fields_csv_path,
        loud=True
    ):
        return False

    if not argument_scale_is_in_scales(
        args.scale,
        loud=True
    ):
        return False

    return True


# ==================================================================================================


# Plot functions
# ==================================================================================================
def plot_ser_histogram_lin(
    ax:  plt.Axes, # type: ignore
    ser: pd.Series
) -> None:
    """
    Plots a histogram of `ser` onto `ax`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    ser : :class:`pandas.Series`
        The :class:`pandas.Series`

    Returns
    -------
    None
    """
    ser  = ser.dropna()
    bins = 30

    ax.hist(
        x=ser,
        bins=bins,
        facecolor="#FFFFFF",
        edgecolor="#000000"
    )


def plot_ser_histogram_log(
    ax:  plt.Axes, # type: ignore
    ser: pd.Series
) -> None:
    """
    Plots a histogram of `ser` onto `ax`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    ser : :class:`pandas.Series`
        The :class:`pandas.Series`

    Returns
    -------
    None
    """
    ser  = ser.dropna()
    bins = np.logspace(
        np.log10(ser.min()),
        np.log10(ser.max()),
        30
    )

    ax.hist(
        x=ser,
        bins=bins,
        facecolor="#FFFFFF",
        edgecolor="#000000"
    )


def plot_ser_boxplot(
    ax:  plt.Axes, # type: ignore
    ser: pd.Series
) -> None:
    """
    Plots a box and whisker plot of `ser` onto `ax`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    ser : :class:`pandas.Series`
        The :class:`pandas.Series`

    Returns
    -------
    None
    """
    ax.boxplot(
        x=ser.dropna(),
        orientation="horizontal"
    )


def plot_quantile_lines(
    ax:        plt.Axes, # type: ignore
    quantiles: list[float],
    labels:    list[str]
) -> None:
    """
    Plots vertical dotted lines on `ax` at each of `quantiles`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    quantiles : list[float]
        The values to draw lines at

    labels : list[str]
        The label for each of `quantiles`

    Returns
    -------
    None
    """
    cmap = plt.get_cmap("tab10")

    for i, (quantile, label) in enumerate(zip(quantiles, labels)):
        ax.axvline(
            x=quantile,
            color=cmap(i),
            linestyle=":",
            label=f"""{label}: {quantile:.3e}"""
        )


def plot_on_hist_ax(
    hist_ax:               plt.Axes, # type: ignore
    hylak_field_ser:       pd.Series,
    hylak_field_quantiles: list[float],
    plot_ser_histogram:    Callable[[plt.Axes, pd.Series], None] # type: ignore
) -> None:
    """
    Plots a histogram (via `plot_ser_histogram`) and quantile lines of
    `hylak_field_ser` onto `hist_ax`.

    Parameters
    ----------
    hist_ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    hylak_field_ser : :class:`pandas.Series`
        The :class:`pandas.Series`

    hylak_field_quantiles : list[float]
        The quantile values to draw lines at

    plot_ser_histogram : Callable[[:class:`matplotlib.axes.Axes`, :class:`pandas.Series`], None]
        The histogram-plotting function to use, e.g.
        `plot_ser_histogram_log` or `plot_ser_histogram_lin`

    Returns
    -------
    None
    """
    plot_ser_histogram(
        hist_ax,
        hylak_field_ser
    )
    plot_quantile_lines(
        hist_ax,
        hylak_field_quantiles,
        [
            "Q1",
            "Q2",
            "Q3"
        ]
    )


def plot_on_box_ax(
    box_ax:                plt.Axes, # type: ignore
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
        The :class:`pandas.Series`

    hylak_field_quantiles : list[float]
        The quantile values to draw lines at

    Returns
    -------
    None
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


def set_hist_ax_properties(
    hist_ax:       plt.Axes, # type: ignore
    set_ax_xscale: Callable[[plt.Axes], None] # type: ignore
) -> None:
    """
    Sets `hist_ax`'s properties, including its x-axis scale (via
    `set_ax_xscale`).

    Parameters
    ----------
    hist_ax : :class:`matplotlib.axes.Axes`
        The axes to set properties on

    set_ax_xscale : Callable[[:class:`matplotlib.axes.Axes`], None]
        The scale-setting function to use, e.g. `set_ax_xscale_to_log`
        or `set_ax_xscale_to_lin`

    Returns
    -------
    None
    """
    set_ax_xscale(hist_ax)


def set_box_ax_properties(
    box_ax:        plt.Axes, # type: ignore
    set_ax_xscale: Callable[[plt.Axes], None] # type: ignore
) -> None:
    """
    Sets `box_ax`'s properties, including its x-axis scale (via
    `set_ax_xscale`).

    Parameters
    ----------
    box_ax : :class:`matplotlib.axes.Axes`
        The axes to set properties on

    set_ax_xscale : Callable[[:class:`matplotlib.axes.Axes`], None]
        The scale-setting function to use, e.g. `set_ax_xscale_to_log`
        or `set_ax_xscale_to_lin`

    Returns
    -------
    None
    """
    set_ax_xscale(box_ax)


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()

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
        nrows=2,
        ncols=1,
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1]}
    )

    if args.scale == "log":
        plot_hylak_field_histogram = plot_ser_histogram_log
        set_ax_xscale              = set_ax_xscale_to_log
        title                      = f"""Log Distribution of {HYLAK_FIELDS[args.hylak_field].long_name}"""
    elif args.scale == "lin":
        plot_hylak_field_histogram = plot_ser_histogram_lin
        set_ax_xscale              = set_ax_xscale_to_lin
        title                      = f"""Lin Distribution of {HYLAK_FIELDS[args.hylak_field].long_name}"""
    else:
        return RETURN_FAILURE

    plot_on_hist_ax(
        hist_ax,
        hylak_field_ser,
        hylak_field_quantiles,
        plot_hylak_field_histogram
    )
    plot_on_box_ax(
        box_ax,
        hylak_field_ser,
        hylak_field_quantiles
    )

    set_hist_ax_properties(
        hist_ax,
        set_ax_xscale
    )
    set_box_ax_properties(
        box_ax,
        set_ax_xscale
    )

    fig.suptitle(title)

    hist_ax.legend()

    save_figure(
        fig,
        PROG,
        TIME
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
