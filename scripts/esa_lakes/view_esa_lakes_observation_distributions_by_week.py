"""
Filename:   view_esa_lakes_observation_distributions_by_week.py
Author:     William Chuter-Davies
Modified:   10/11/26
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

from matplotlib                     import cm
from matplotlib.axes                import Axes
from matplotlib.figure              import Figure
from mpl_toolkits.mplot3d.axes3d    import Axes3D

# Local Application/Library Specific Imports
from wfsel.arguments                        import add_argument_output
from wfsel.exit_codes                       import (
                                                EXIT_FAILURE,
                                                EXIT_SUCCESS,
                                            )
from wfsel.io.writers                       import to_svg
from wfsel.plot.arguments                   import (
                                                add_argument_azimuth,
                                                add_argument_dimension,
                                                add_argument_elevation,
                                            )
from wfsel.plot.literals                    import (
                                                FONTSIZE_AXIS_LABEL,
                                                FONTSIZE_TICK_LABEL,
                                                FONTSIZE_TITLE,
                                                GREY_M,
                                            )
from wfsel.plot.plotters                    import (
                                                plot_colorbar,
                                                plot_kde_2d,
                                                plot_kde_3d,
                                            )
from wfsel.sources.esa_lakes.arguments      import (
                                                add_argument_esa_lakes_high_smoke_year_observations_anomaly_csv_path,
                                                add_argument_esa_lakes_low_smoke_year_observations_anomaly_csv_path,
                                                add_argument_esa_lakes_week_first,
                                                add_argument_esa_lakes_week_last,
                                            )
from wfsel.sources.esa_lakes.comprehenders  import comprehend_column_names
from wfsel.sources.esa_lakes.readers        import (
                                                read_esa_lakes_high_smoke_year_observations_anomaly_csv,
                                                read_esa_lakes_low_smoke_year_observations_anomaly_csv,
                                            )
from wfsel.utils.argparse_utils             import (
                                                arguments_are_valid as _arguments_are_valid,
                                                build_parser        as _build_parser,
                                                argument_is_file,
                                            )

PROG    = "view_esa_lakes_observation_distributions_by_week.py"
DESC    = ""

FIGSIZE_2D  = (6.40, 4.80)
FIGSIZE_3D  = (19.2, 14.4)
ALPHA       = 0.75

HIGH_SMOKE_AX_CMAP          = cm.Reds_r
HIGH_SMOKE_AX_TITLE         = "Distributions of High Smoke Temperature Anomalies"
HIGH_SMOKE_AX_XAXIS_LABEL   = "Temperature Anomaly (°C)"
HIGH_SMOKE_AX_YAXIS_LABEL   = "Density"
HIGH_SMOKE_AX_ZAXIS_LABEL   = "Week Number"

LOW_SMOKE_AX_CMAP           = cm.Blues_r
LOW_SMOKE_AX_TITLE          = "Distributions of Low Smoke Temperature Anomalies"
LOW_SMOKE_AX_XAXIS_LABEL    = "Temperature Anomaly (°C)"
LOW_SMOKE_AX_YAXIS_LABEL    = "Density"
LOW_SMOKE_AX_ZAXIS_LABEL    = "Week Number"

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
                    add_argument_esa_lakes_high_smoke_year_observations_anomaly_csv_path,
                    add_argument_esa_lakes_low_smoke_year_observations_anomaly_csv_path,
                    add_argument_esa_lakes_week_first,
                    add_argument_esa_lakes_week_last,
                ],
                optional_arguments      = [
                    add_argument_dimension,
                    add_argument_elevation,
                    add_argument_azimuth,
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
    if (    arguments.dimension == 3
        and arguments.elevation is None
    ):
        message = "expected argument elevation to be set if --dimension=3 is true"

        raise ValueError(message)

    if (    arguments.dimension == 3
        and arguments.azimuth is None
    ):
        message = "expected argument azimuth to be set if --dimension=3 is true"

        raise ValueError(message)

    argument_name_to_validator  = {
                                    "esa_lakes_high_smoke_year_observations_anomaly_csv_path":  argument_is_file,
                                    "esa_lakes_low_smoke_year_observations_anomaly_csv_path":   argument_is_file,
                                }

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


# ----------------------------------------------------------------------
# builder functions
# ----------------------------------------------------------------------
def build_figure_2d(
    esa_lakes_high_smoke_year_observations_anomaly_df:  pd.DataFrame,
    esa_lakes_low_smoke_year_observations_anomaly_df:   pd.DataFrame,
    column_names:                                       list[str],
) -> Figure:
    """
    Build a 2D figure.

    Parameters
    ----------
    esa_lakes_high_smoke_year_observations_anomaly_df : pd.DataFrame
        The ESA Lakes high smoke year observations anomaly dataframe
    esa_lakes_low_smoke_year_observations_anomaly_df : pd.DataFrame
        The ESA Lakes low smoke year observations anomaly dataframe
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
            high_smoke_ax,
            low_smoke_ax,
        ),
    )   = plt.subplots(
            nrows   = 2,
            ncols   = 1,
            sharex  = True,
            sharey  = True,
            figsize = FIGSIZE_2D,
        )

    plot_high_smoke_ax_2d(
        high_smoke_ax,
        esa_lakes_high_smoke_year_observations_anomaly_df,
        column_names,
    )
    plot_low_smoke_ax_2d(
        low_smoke_ax,
        esa_lakes_low_smoke_year_observations_anomaly_df,
        column_names,
    )

    decorate_high_smoke_ax_2d(high_smoke_ax)
    decorate_low_smoke_ax_2d(low_smoke_ax)

    fig.subplots_adjust(hspace = 0.25)
    fig.align_xlabels()
    fig.align_ylabels()

    return fig


def build_figure_3d(
    esa_lakes_high_smoke_year_observations_anomaly_df:  pd.DataFrame,
    esa_lakes_low_smoke_year_observations_anomaly_df:   pd.DataFrame,
    column_names:                                       list[str],
    *,
    elevation:  float,
    azimuth:    float,
) -> Figure:
    """
    Build a 3D figure.

    Parameters
    ----------
    esa_lakes_high_smoke_year_observations_anomaly_df : pd.DataFrame
        The ESA Lakes high smoke year observations anomaly dataframe
    esa_lakes_low_smoke_year_observations_anomaly_df : pd.DataFrame
        The ESA Lakes low smoke year observations anomaly dataframe
    column_names : list[str]
        The list of column names
    elevation : float
        The elevation
    azimuth : float
        The azimuth

    Returns
    -------
    Figure
        A figure
    """
    fig = plt.figure(figsize = FIGSIZE_3D)

    high_smoke_ax  = fig.add_subplot(211, projection="3d")
    low_smoke_ax   = fig.add_subplot(212, projection="3d")

    plot_high_smoke_ax_3d(
        high_smoke_ax,
        esa_lakes_high_smoke_year_observations_anomaly_df,
        column_names,
    )
    plot_low_smoke_ax_3d(
        low_smoke_ax,
        esa_lakes_low_smoke_year_observations_anomaly_df,
        column_names,
    )

    decorate_high_smoke_ax_3d(
        high_smoke_ax,
        column_names,
        elevation,
        azimuth,
    )
    decorate_low_smoke_ax_3d(
        low_smoke_ax,
        column_names,
        elevation,
        azimuth,
    )

    fig.align_xlabels()
    fig.align_ylabels()

    return fig


# ----------------------------------------------------------------------
# builder functions
# ----------------------------------------------------------------------
def plot_high_smoke_ax_2d(
    high_smoke_ax:                                      Axes,
    esa_lakes_high_smoke_year_observations_anomaly_df:  pd.DataFrame,
    column_names:                                       list[str],
) -> None:
    """
    Plot onto a high smoke axes.

    Parameters
    ----------
    high_smoke_ax : Axes
        The high smoke axes
    esa_lakes_high_smoke_year_observations_anomaly_df : pd.DataFrame
        The ESA Lakes high smoke year observations anomaly dataframe
    column_names : list[str]
        The list of column names
    """
    for i, column_name in reversed(list(enumerate(column_names))):
        ser     = esa_lakes_high_smoke_year_observations_anomaly_df[column_name]
        colour  = HIGH_SMOKE_AX_CMAP(i / max(len(column_names) - 1, 1))

        plot_kde_2d(
            high_smoke_ax,
            ser     = ser,
            color   = colour,
        )

    plot_colorbar(
        high_smoke_ax,
        cmap    = HIGH_SMOKE_AX_CMAP,
        vmin    = 1,
        vmax    = len(column_names),
        label   = HIGH_SMOKE_AX_ZAXIS_LABEL,
    )


def plot_low_smoke_ax_2d(
    low_smoke_ax:                                       Axes,
    esa_lakes_low_smoke_year_observations_anomaly_df:   pd.DataFrame,
    column_names:                                       list[str],
) -> None:
    """
    Plot onto a low smoke axes.

    Parameters
    ----------
    low_smoke_ax : Axes
        The low smoke axes
    esa_lakes_low_smoke_year_observations_anomaly_df : pd.DataFrame
        The ESA Lakes low smoke year observations anomaly dataframe
    column_names : list[str]
        The list of column names
    """
    for i, column_name in reversed(list(enumerate(column_names))):
        ser     = esa_lakes_low_smoke_year_observations_anomaly_df[column_name]
        colour  = LOW_SMOKE_AX_CMAP(i / max(len(column_names) - 1, 1))

        plot_kde_2d(
            low_smoke_ax,
            ser     = ser,
            color   = colour,
        )

    plot_colorbar(
        low_smoke_ax,
        cmap    = LOW_SMOKE_AX_CMAP,
        vmin    = 1,
        vmax    = len(column_names),
        label   = LOW_SMOKE_AX_ZAXIS_LABEL,
    )


def plot_high_smoke_ax_3d(
    high_smoke_ax:                                      Axes,
    esa_lakes_high_smoke_year_observations_anomaly_df:  pd.DataFrame,
    column_names:                                       list[str],
) -> None:
    """
    Plot onto a high smoke axes.

    Parameters
    ----------
    high_smoke_ax : Axes
        The high smoke axes
    esa_lakes_high_smoke_year_observations_anomaly_df : pd.DataFrame
        The ESA Lakes high smoke year observations anomaly dataframe
    column_names : list[str]
        The list of column names
    """
    for i, column_name in reversed(list(enumerate(column_names))):
        ser     = esa_lakes_high_smoke_year_observations_anomaly_df[column_name]
        colour  = HIGH_SMOKE_AX_CMAP(i / max(len(column_names) - 1, 1))

        plot_kde_3d(
            high_smoke_ax,
            ser     = ser,
            zs      = i,
            color   = colour,
        )


def plot_low_smoke_ax_3d(
    low_smoke_ax:                                       Axes,
    esa_lakes_low_smoke_year_observations_anomaly_df:   pd.DataFrame,
    column_names:                                       list[str],
) -> None:
    """
    Plot onto a low smoke axes.

    Parameters
    ----------
    low_smoke_ax : Axes
        The low smoke axes
    esa_lakes_low_smoke_year_observations_anomaly_df : pd.DataFrame
        The ESA Lakes low smoke year observations anomaly dataframe
    column_names : list[str]
        The list of column names
    """
    for i, column_name in reversed(list(enumerate(column_names))):
        ser     = esa_lakes_low_smoke_year_observations_anomaly_df[column_name]
        colour  = LOW_SMOKE_AX_CMAP(i / max(len(column_names) - 1, 1))

        plot_kde_3d(
            low_smoke_ax,
            ser     = ser,
            zs      = i,
            color   = colour,
        )

# ----------------------------------------------------------------------
# decorator functions
# ----------------------------------------------------------------------
def decorate_high_smoke_ax_2d(
    high_smoke_ax: Axes,
) -> None:
    """
    Decorate a high smoke axes.

    Parameters
    ----------
    high_smoke_ax : Axes
        The high smoke axes
    """
    high_smoke_ax.set_title(HIGH_SMOKE_AX_TITLE, fontsize = FONTSIZE_TITLE)
    high_smoke_ax.set_xlabel(HIGH_SMOKE_AX_XAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    high_smoke_ax.set_ylabel(HIGH_SMOKE_AX_YAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    high_smoke_ax.tick_params(labelsize = FONTSIZE_TICK_LABEL)
    high_smoke_ax.set_facecolor(GREY_M)


def decorate_low_smoke_ax_2d(
    low_smoke_ax: Axes,
) -> None:
    """
    Decorate a low smoke axes.

    Parameters
    ----------
    low_smoke_ax : Axes
        The low smoke axes
    """
    low_smoke_ax.set_title(LOW_SMOKE_AX_TITLE, fontsize = FONTSIZE_TITLE)
    low_smoke_ax.set_xlabel(LOW_SMOKE_AX_XAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    low_smoke_ax.set_ylabel(LOW_SMOKE_AX_YAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    low_smoke_ax.tick_params(labelsize = FONTSIZE_TICK_LABEL)
    low_smoke_ax.set_facecolor(GREY_M)


def decorate_high_smoke_ax_3d(
    high_smoke_ax:  Axes3D,
    column_names:   list[str],
    elevation:      float,
    azimuth:        float,
) -> None:
    """
    Decorate a high smoke axes.

    Parameters
    ----------
    high_smoke_ax : Axes3D
        The high smoke axes
    column_names : list[str]
        The list of column names
    elevation : float
        The elevation
    azimuth : float
        The azimuth
    """
    high_smoke_ax.set_title(HIGH_SMOKE_AX_TITLE, fontsize = FONTSIZE_TITLE)
    high_smoke_ax.set_xlabel(HIGH_SMOKE_AX_XAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    high_smoke_ax.set_ylabel(HIGH_SMOKE_AX_ZAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    high_smoke_ax.set_zlabel(HIGH_SMOKE_AX_YAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    high_smoke_ax.set_yticks(
        range(len(column_names)),
        labels  = [
                    column_name.split("_")[1]
                    for column_name
                    in column_names
                ],
    )
    high_smoke_ax.tick_params(labelsize = FONTSIZE_TICK_LABEL)
    high_smoke_ax.view_init(elev = elevation, azim = azimuth)

    high_smoke_ax.zaxis.set_pane_color(GREY_M)    # type: ignore[name-defined]
    high_smoke_ax.xaxis.set_pane_color(GREY_M)    # type: ignore[name-defined]
    high_smoke_ax.yaxis.set_pane_color(GREY_M)    # type: ignore[name-defined]


def decorate_low_smoke_ax_3d(
    low_smoke_ax:   Axes3D,
    column_names:   list[str],
    elevation:      float,
    azimuth:        float,
) -> None:
    """
    Decorate a low smoke axes.

    Parameters
    ----------
    low_smoke_ax : Axes3D
        The low smoke axes
    column_names : list[str]
        The list of column names
    elevation : float
        The elevation
    azimuth : float
        The azimuth
    """
    low_smoke_ax.set_title(LOW_SMOKE_AX_TITLE, fontsize = FONTSIZE_TITLE)
    low_smoke_ax.set_xlabel(LOW_SMOKE_AX_XAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    low_smoke_ax.set_ylabel(LOW_SMOKE_AX_ZAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    low_smoke_ax.set_zlabel(LOW_SMOKE_AX_YAXIS_LABEL, fontsize = FONTSIZE_AXIS_LABEL)
    low_smoke_ax.set_yticks(
        range(len(column_names)),
        labels  = [
                    column_name.split("_")[1]
                    for column_name
                    in column_names
                ],
    )
    low_smoke_ax.tick_params(labelsize = FONTSIZE_TICK_LABEL)
    low_smoke_ax.view_init(elev = elevation, azim = azimuth)

    low_smoke_ax.zaxis.set_pane_color(GREY_M)    # type: ignore[name-defined]
    low_smoke_ax.xaxis.set_pane_color(GREY_M)    # type: ignore[name-defined]
    low_smoke_ax.yaxis.set_pane_color(GREY_M)    # type: ignore[name-defined]


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

    high_smoke_year_observations_anomaly_df = read_esa_lakes_high_smoke_year_observations_anomaly_csv(
                                                args.esa_lakes_high_smoke_year_observations_anomaly_csv_path,
                                            )
    low_smoke_year_observations_anomaly_df  = read_esa_lakes_low_smoke_year_observations_anomaly_csv(
                                                args.esa_lakes_low_smoke_year_observations_anomaly_csv_path,
                                            )

    column_names    = comprehend_column_names(
                        args.esa_lakes_week_first,
                        args.esa_lakes_week_last,
                    )

    if args.dimension == 2:
        fig = build_figure_2d(
                high_smoke_year_observations_anomaly_df,
                low_smoke_year_observations_anomaly_df,
                column_names,
            )
    else:
        fig = build_figure_3d(
                high_smoke_year_observations_anomaly_df,
                low_smoke_year_observations_anomaly_df,
                column_names,
                elevation   = args.elevation,
                azimuth     = args.azimuth,
            )

    to_svg(
        fig,
        args.output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
