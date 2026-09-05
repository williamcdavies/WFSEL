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

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.io import (
    add_argument_hylak_field,
    add_argument_esacci_lakes_hylak_fields_csv_path,
    argument_hylak_field_is_in_hylak_fields,
    argument_esacci_lakes_hylak_fields_csv_path_exists,
    read_esacci_lakes_hylak_fields_csv
)
from lib.io.vars               import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)
from lib.math.utils            import (
    get_ser_from_df,
    get_quantiles_from_ser
)
from lib.math.vars             import SPACES
from lib.plot.utils            import (
    set_ax_xscale_to_lin,
    set_ax_xscale_to_log,
    set_ax_title
)

PROG   = "view_distribution_of_esacci_lakes_hylak_field.py"


def add_argument_space(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `space` argument to a :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `space` is of type :class:`str`.
    """
    parser.add_argument(
        "--space",
        type=str,
        required=True,
        help=f"""one of {SPACES}"""
    )


def argument_space_is_in_spaces(
    space: str,
    *,
    loud:   bool = False
) -> bool:
    """
    Validates `space`.

    Parameters
    ----------
    space : :class:`str`
        The argument `space`

    loud : bool
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `space` is in `SPACES`. `False` otherwise.
    """
    if space in SPACES:
        return True

    if loud:
        print(f"""error: argument space: not in {SPACES}: {space}""")

    return False


def build_parser(
) -> argparse.ArgumentParser:
    """
    Builds a :class:`ArgumentParser`.

    Returns
    -------
    A :class:`ArgumentParser`.
    """
    parser = argparse.ArgumentParser(
        prog=PROG,
        usage="%(prog)s [options]",
        description=""""""
    )

    # Positional arguments
    add_argument_hylak_field(parser)
    add_argument_esacci_lakes_hylak_fields_csv_path(parser)

    # Optinal arguments
    add_argument_space(parser)

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
    if not argument_hylak_field_is_in_hylak_fields(args.hylak_field, loud=True): 
        return False

    if not argument_esacci_lakes_hylak_fields_csv_path_exists(args.esacci_lakes_hylak_fields_csv_path, loud=True):
        return False

    return True


def plot_hylak_field_lin_histogram(
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


def plot_hylak_field_log_histogram(
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


def plot_hylak_field_boxplot(
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


def plot_quartile_lines(
    ax:        plt.Axes, # type: ignore
    quartiles: list[float],
    labels:    list[str]
) -> None:
    """
    Plots vertical dotted lines on `ax` at each of `quartiles`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    quartiles : list[float]
        The values to draw lines at

    labels : list[str]
        The label for each of `quartiles`

    Returns
    -------
    None
    """
    cmap = plt.get_cmap("tab10")

    for i, (quartile, label) in enumerate(zip(quartiles, labels)):
        ax.axvline(
            x=quartile,
            color=cmap(i),
            linestyle=":",
            label=f"""{label}: {quartile:.3e}"""
        )


def main(
) -> int:
    """
    Orchestration layer.

    Returns
    -------
    0 if program completes successfully. 1 otherwise.
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

    _, (hist_ax, box_ax) = plt.subplots(
        nrows=2,
        ncols=1,
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1]}
    )

    if args.space == "log":
        plot_hylak_field_log_histogram(
            hist_ax,
            hylak_field_ser
        )

        set_ax_xscale_to_log(hist_ax)
        set_ax_xscale_to_log(box_ax)
        
        set_ax_title(
            hist_ax, 
            f"""Log Distribution of {args.hylak_field}"""
        )
    elif args.space == "lin":
        plot_hylak_field_lin_histogram(
            hist_ax,
            hylak_field_ser
        )

        set_ax_xscale_to_lin(hist_ax)
        set_ax_xscale_to_lin(box_ax)

        set_ax_title(
            hist_ax, 
            f"""Lin Distribution of {args.hylak_field}"""
        )
    else:
        return RETURN_FAILURE

    plot_hylak_field_boxplot(
        box_ax, 
        hylak_field_ser
    )

    plot_quartile_lines(
        hist_ax, 
        hylak_field_quantiles, 
        [
            "Q1", 
            "Q2", 
            "Q3"
        ]
    )
    plot_quartile_lines(
        box_ax, 
        hylak_field_quantiles, 
        [
            "Q1", 
            "Q2", 
            "Q3"
        ]
    )

    hist_ax.legend()
    plt.tight_layout()
    plt.show()

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
