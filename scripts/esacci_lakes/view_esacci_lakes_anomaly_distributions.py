"""
Filename:   view_esacci_lakes_anomaly_distributions.py
Author:     William Chuter-Davies
Modified:   30/10/26
"""

# Standard Library Imports
import sys

from argparse   import (
                    ArgumentParser,
                    Namespace,
                )

# Related Third-party Imports
import matplotlib.pyplot    as plt
import pandas               as pd

from matplotlib.axes    import Axes
from matplotlib.figure  import Figure
from scipy.stats        import gaussian_kde

# Local Application/Library Specific Imports
from wfsel.exit_codes                           import (
                                                    EXIT_FAILURE,
                                                    EXIT_SUCCESS,
                                                )
from wfsel.io.arguments                         import add_argument_output
from wfsel.io.writers                           import to_svg
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

PROG    = "view_esacci_lakes_anomaly_distributions.py"
DESC    = ""

OPACITY = 0.25

HIGH_SMOKE_YEAR_AX_TITLE    = "Distributions of High Smoke Season Anomalies"
HIGH_SMOKE_YEAR_AX_COLOUR   = "red"
LOW_SMOKE_YEAR_AX_TITLE     = "Distributions of Low Smoke Season Anomalies"
LOW_SMOKE_YEAR_AX_COLOUR    = "blue"
X_LABEL                     = "Temperature anomaly (°C)"
Y_LABEL                     = "Density"

plt.rcParams["font.family"] = "Arial"

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
def compute_kde(
    ser: pd.Series[float],
) -> gaussian_kde:
    """
    Compute a KDE from a series.

    Parameters
    ----------
    ser : pd.Series[float]
        The series

    Returns
    -------
    gaussian_kde
        A KDE
    """
    return gaussian_kde(ser)


def plot_kde(
    ax:     Axes,
    ser:    pd.Series[float],
    colour: str,
) -> None:
    """
    Plot a KDE of a series onto an axes.

    Parameters
    ----------
    ax : Axes
        The axes
    ser : pd.Series[float]
        The series
    colour : str
        The colour
    """
    ser = ser.dropna()
    kde = compute_kde(ser)
    x   = ser.sort_values()
    y   = pd.Series(
            kde(x),
            index = x.index
        )

    ax.plot(
        x,
        y,
        alpha   = OPACITY,
        color   = colour,
    )


def build_figure(
    esacci_lakes_high_smoke_year_observations_anomaly_df:   pd.DataFrame,
    esacci_lakes_low_smoke_year_observations_anomaly_df:    pd.DataFrame,
    column_names:                                           list[str],
) -> Figure:
    """
    Build a distributions figure.

    Parameters
    ----------
    esacci_lakes_high_smoke_year_observations_anomaly_df : pd.DataFrame
        The ESA CCI Lakes high smoke year observations anomaly dataframe
    esacci_lakes_low_smoke_year_observations_anomaly_df : pd.DataFrame
        The ESA CCI Lakes low smoke year observations anomaly dataframe
    column_names : list[str]
        The list of column names

    Returns
    -------
    Figure
        A figure
    """
    (
        fig,
        (
            high_smoke_year_ax,
            low_smoke_year_ax,
        )
    )   = plt.subplots(
            nrows   = 2,
            ncols   = 1,
            sharex  = True,
            sharey  = True,
        )

    for column_name in column_names:
        ser = esacci_lakes_high_smoke_year_observations_anomaly_df[column_name]
    
        plot_kde(
            high_smoke_year_ax,
            ser,
            HIGH_SMOKE_YEAR_AX_COLOUR,
        )

    for column_name in column_names:
        ser = esacci_lakes_low_smoke_year_observations_anomaly_df[column_name]
    
        plot_kde(
            low_smoke_year_ax,
            ser,
            LOW_SMOKE_YEAR_AX_COLOUR,
        )
    
    high_smoke_year_ax.set_title(HIGH_SMOKE_YEAR_AX_TITLE)
    high_smoke_year_ax.set_ylabel(Y_LABEL)
    low_smoke_year_ax.set_title(LOW_SMOKE_YEAR_AX_TITLE)
    low_smoke_year_ax.set_ylabel(Y_LABEL)
    low_smoke_year_ax.set_xlabel(X_LABEL)

    return fig


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

    fig = build_figure(
            high_smoke_year_observations_anomaly_df,
            low_smoke_year_observations_anomaly_df,
            column_names,
        )

    to_svg(
        fig,
        args.output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
