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
from lib.dataframe.utils         import get_ser_from_df
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
from lib.plot.vars               import SCALES
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

PROG = "view_distribution_of_esacci_lakes_hylak_field.py"

plt.rcParams["font.family"] = "Arial"

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
        help = f"one of {", ".join(SCALES)}"
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
        "Produces a distribution visualisation of a HydroLAKES field of all lakes in spatial.esacci_lakes (Same lakes as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0).",
        positional_args = [
            add_argument_hylak_field,
            add_argument_esacci_lakes_hylak_fields_csv_path,
            add_argument_scale
        ],
        optional_args   = [
            add_argument_output
        ]
    )


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
    `True` if `scale` is in `SCALES`. `False` otherwise.
    """
    if scale in SCALES:
        return True

    if loud:
        print(
            f"error: argument scale: not in {", ".join(SCALES)}: {scale}",
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
    `True` if all arguments are successfully validated. `False`
    otherwise.
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


# Plot functions
# ==================================================================================================
def plot_on_box_ax(
    box_ax:          Axes,
    hylak_field_ser: pd.Series,
    scale:           str
) -> None:
    if scale == "linear":
        plot_ser_boxplot_linear(
            box_ax,
            hylak_field_ser
        )
    elif scale == "log":
        plot_ser_boxplot_log(
            box_ax,
            hylak_field_ser
        )
    else:
        raise ValueError(f"expected `scale` to be one of {", ".join(SCALES)}: {scale}")


def plot_on_hist_ax(
    hist_ax:         Axes,
    hylak_field_ser: pd.Series,
    scale:           str
) -> None:
    """
    Plots onto `hist_ax`.

    Parameters
    ----------
    hist_ax : :class:`matplotlib.axes.Axes`
        The axes

    hylak_field_ser : :class:`pandas.Series`
        The series

    scale : :class:`str`
        One of `SCALES`

    Returns
    -------
    None.

    Raises
    ------
    ValueError
        If `scale` is not in `SCALES`.
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
        raise ValueError(f"expected `scale` to be one of {", ".join(SCALES)}: {scale}")


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
        The axes

    quantiles : list[:class:`float`]
        The quantile values

    labels : list[:class:`str`]
        The quantile labels

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
        if label is not None and quantile is not None:
            ax.axvline(
                x         = quantile,
                color     = cmap(i),
                linestyle = ":",
                label     = f"{label}: {quantile:.1f}"
            )


def plot_ser_boxplot_linear(
    ax:  Axes,
    ser: pd.Series
):
    ax.boxplot(
        x           = ser.dropna(),
        orientation = "horizontal",
    )


def plot_ser_boxplot_log(
    ax:  Axes,
    ser: pd.Series
):
    q1 = np.quantile(ser.dropna(), 0.25)
    q3 = np.quantile(ser.dropna(), 0.75)

    IQR = q3 / q1
    OUT = IQR ** 1.5

    UPPER_LIMIT = q3 * OUT
    LOWER_LIMIT = q1 / OUT

    count_less_q1    = sum(1 for x in ser.dropna() if x < LOWER_LIMIT)
    count_greater_q3 = sum(1 for x in ser.dropna() if x > UPPER_LIMIT)

    percent_less_q1    = (count_less_q1 / len(ser.dropna())) 
    percent_greater_q3 = (count_greater_q3 / len(ser.dropna())) 

    ax.boxplot(
        x           = ser.dropna(),
        whis        = [percent_less_q1 * 100, (1 - percent_greater_q3) * 100],
        orientation = "horizontal",
    )


def plot_ser_histogram_linear(
    ax:  Axes,
    ser: pd.Series
) -> None:
    """
    Plots a histogram of `ser` onto `ax` with linearlyß spaced bins.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes

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
    Plots a histogram of `ser` onto `ax` with logarithmically spaced
    bins.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes

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
    box_ax:    Axes,
    scale:     str,
    xlabel:    str
) -> None:
    """
    Sets `box_ax`'s properties.

    Parameters
    ----------
    box_ax : :class:`matplotlib.axes.Axes`
        The axes

    scale : :class:`str`
        One of `SCALES`

    xlabel : :class:`str`
        The x-axis label

    Returns
    -------
    None.

    Raises
    ------
    ValueError
        If `scale` is not in `SCALES`.
    """
    if scale == "linear":
        set_ax_xscale_to_linear(box_ax)
    elif scale == "log":
        set_ax_xscale_to_log(box_ax)
    else:
        raise ValueError(f"expected `scale` to be one of {", ".join(SCALES)}: {scale}")

    box_ax.set_xlabel(
        xlabel,
        fontsize = 12
    )
    box_ax.tick_params(labelsize = 9)
    box_ax.set_yticks([])


def set_hist_ax_properties(
    hist_ax: Axes,
    scale:   str,
    ylabel:  str
) -> None:
    """
    Sets `hist_ax`'s properties.

    Parameters
    ----------
    hist_ax : :class:`matplotlib.axes.Axes`
        The axes

    scale : :class:`str`
        One of `SCALES`

    xlabel : :class:`str`
        The y-axis label

    Returns
    -------
    None.

    Raises
    ------
    ValueError
        If `scale` is not in `SCALES`.
    """
    if scale == "linear":
        set_ax_xscale_to_linear(hist_ax)
    elif scale == "log":
        set_ax_xscale_to_log(hist_ax)
    else:
        raise ValueError(f"expected `scale` to be one of {", ".join(SCALES)}: {scale}")

    hist_ax.set_ylabel(
        ylabel,
        fontsize = 12
    )
    hist_ax.tick_params(labelsize = 9)
    hist_ax.set_ylim(
        0,
        130
    )
    hist_ax.legend(fontsize = 12)


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser().parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    hylak_fields_df = read_esacci_lakes_hylak_fields_csv(args.esacci_lakes_hylak_fields_csv_path)
    hylak_field_ser = get_ser_from_df(
        hylak_fields_df,
        args.hylak_field
    )

    hylak_field   = HYLAK_FIELDS[args.hylak_field]
    display_scale = hylak_field.display_scale
    lower_bound   = hylak_field.lower_bound
    upper_bound   = hylak_field.upper_bound

    hylak_field_ser     = hylak_field_ser / display_scale
    lower_bound_display = lower_bound / display_scale if lower_bound is not None else None
    upper_bound_display = upper_bound / display_scale if upper_bound is not None else None

    fig_width  = 8.27 / 2
    fig_height = 11.69 / 3

    (
        fig,
        (
            hist_ax,
            box_ax
        )
    ) = plt.subplots(
        nrows       = 2,
        ncols       = 1,
        sharex      = True,
        gridspec_kw = {"height_ratios": [
            4,
            1
        ]},
        figsize = (
            fig_width,
            fig_height
        )
    )

    plot_on_hist_ax(
        hist_ax,
        hylak_field_ser,
        args.scale
    )
    plot_on_box_ax(
        box_ax,
        hylak_field_ser,
        args.scale
    )

    plot_quantile_lines(
        hist_ax,
        [
            upper_bound_display,
            lower_bound_display,
        ],
        [
            "Upper Bound",
            "Lower Bound",
        ]
    )

    plot_quantile_lines(
        box_ax,
        [
            upper_bound_display,
            lower_bound_display,
        ],
        [
            "Upper Bound",
            "Lower Bound",
        ]
    )

    set_hist_ax_properties(
        hist_ax,
        args.scale,
        ylabel = "Number of Lakes"
    )
    set_box_ax_properties(
        box_ax,
        args.scale,
        xlabel = (
            hylak_field.long_name
            + " "
            + "("
            + hylak_field.display_units
            + ")"
        )
    )

    fig.tight_layout()

    save_figure(
        fig,
        args.output
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
