"""
Filename:   view_esa_lakes_observation_distributions_by_week.py
Author:     William Chuter-Davies
Modified:   05/11/26
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

from matplotlib         import cm
from matplotlib.figure  import Figure

# Local Application/Library Specific Imports
from wfsel.exit_codes                       import (
                                                EXIT_FAILURE,
                                                EXIT_SUCCESS,
                                            )
from wfsel.io.arguments                     import add_argument_output
from wfsel.io.writers                       import to_svg
from wfsel.plot.arguments                   import (
                                                add_argument_azimuth,
                                                add_argument_dimension,
                                                add_argument_elevation,
                                            )
from wfsel.plot.literals                    import (
                                                AXIS_LABEL_FONTSIZE,
                                                MEDIUM_GREY,
                                                TICK_LABEL_FONTSIZE,
                                                TITLE_FONTSIZE,
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

HIGH_SMOKE_AX_TITLE = "Distributions of High Smoke Temperature Anomalies"
LOW_SMOKE_AX_TITLE  = "Distributions of Low Smoke Temperature Anomalies"

X_LABEL = "Temperature Anomaly (°C)"
Y_LABEL = "Density"
Z_LABEL = "Week Number"

HIGH_SMOKE_AX_CMAP  = cm.Reds_r
LOW_SMOKE_AX_CMAP   = cm.Blues_r

FIGSIZE_2D  = (
                6.4,    # x
                4.8,    # y
            )
FIGSIZE_3D  = (
                19.2,   # x
                14.4,   # y
            )

ALPHA   = 0.75
HSPACE  = 0.33

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
    Build a 2D distributions figure.

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
            high_smoke_year_ax,
            low_smoke_year_ax,
        ),
    )   = plt.subplots(
            nrows   = 2,
            ncols   = 1,
            sharex  = True,
            sharey  = True,
            figsize = FIGSIZE_2D,
        )

    fig.subplots_adjust(hspace = HSPACE)

    for i, column_name in reversed(list(enumerate(column_names))):
        ser     = esa_lakes_high_smoke_year_observations_anomaly_df[column_name]
        colour  = HIGH_SMOKE_AX_CMAP(i / max(len(column_names) - 1, 1))

        plot_kde_2d(
            high_smoke_year_ax,
            ser     = ser,
            color   = colour,
        )

    plot_colorbar(
        high_smoke_year_ax,
        cmap    = HIGH_SMOKE_AX_CMAP,
        vmin    = 1,
        vmax    = len(column_names),
        label   = Z_LABEL,
    )

    high_smoke_year_ax.set_title(
        HIGH_SMOKE_AX_TITLE,
        fontsize = TITLE_FONTSIZE,
    )
    high_smoke_year_ax.set_ylabel(
        Y_LABEL,
        fontsize = AXIS_LABEL_FONTSIZE,
    )
    high_smoke_year_ax.tick_params(
        labelsize = TICK_LABEL_FONTSIZE,
    )
    high_smoke_year_ax.set_facecolor(
        MEDIUM_GREY,
    )

    for i, column_name in reversed(list(enumerate(column_names))):
        ser     = esa_lakes_low_smoke_year_observations_anomaly_df[column_name]
        colour  = LOW_SMOKE_AX_CMAP(i / max(len(column_names) - 1, 1))

        plot_kde_2d(
            low_smoke_year_ax,
            ser     = ser,
            color   = colour,
        )

    plot_colorbar(
        low_smoke_year_ax,
        cmap    = LOW_SMOKE_AX_CMAP,
        vmin    = 1,
        vmax    = len(column_names),
        label   = Z_LABEL,
    )

    low_smoke_year_ax.set_title(
        LOW_SMOKE_AX_TITLE,
        fontsize = TITLE_FONTSIZE,
    )
    low_smoke_year_ax.set_xlabel(
        X_LABEL,
        fontsize = AXIS_LABEL_FONTSIZE,
    )
    low_smoke_year_ax.set_ylabel(
        Y_LABEL,
        fontsize = AXIS_LABEL_FONTSIZE,
    )
    low_smoke_year_ax.tick_params(
        labelsize = TICK_LABEL_FONTSIZE,
    )
    low_smoke_year_ax.set_facecolor(
        MEDIUM_GREY,
    )

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
    Build a 3D distributions figure.

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

    high_smoke_ax  = fig.add_subplot(
        211,
        projection="3d",
    )
    low_smoke_ax   = fig.add_subplot(
        212,
        projection="3d",
    )

    for i, column_name in reversed(list(enumerate(column_names))):
        ser     = esa_lakes_high_smoke_year_observations_anomaly_df[column_name]
        colour  = HIGH_SMOKE_AX_CMAP(i / max(len(column_names) - 1, 1))

        plot_kde_3d(
            high_smoke_ax,
            ser     = ser,
            zs      = i,
            color   = colour,
        )

    high_smoke_ax.set_title(
        HIGH_SMOKE_AX_TITLE,
        fontsize = TITLE_FONTSIZE,
    )
    high_smoke_ax.set_xlabel(
        X_LABEL,
        fontsize = AXIS_LABEL_FONTSIZE,
    )
    high_smoke_ax.set_ylabel(
        Z_LABEL,
        fontsize = AXIS_LABEL_FONTSIZE,
    )
    high_smoke_ax.set_zlabel(
        Y_LABEL,
        fontsize = AXIS_LABEL_FONTSIZE,
    )
    high_smoke_ax.set_yticks(
        range(len(column_names)),
        labels  = [
                    column_name.split("_")[1]
                    for column_name
                    in column_names
                ],
    )
    high_smoke_ax.tick_params(
        labelsize = TICK_LABEL_FONTSIZE,
    )
    high_smoke_ax.view_init(
        elev = elevation,
        azim = azimuth,
    )

    high_smoke_ax.zaxis.set_pane_color(MEDIUM_GREY)    # type: ignore[name-defined]
    high_smoke_ax.xaxis.set_pane_color(MEDIUM_GREY)    # type: ignore[name-defined]
    high_smoke_ax.yaxis.set_pane_color(MEDIUM_GREY)    # type: ignore[name-defined]

    for i, column_name in reversed(list(enumerate(column_names))):
        ser     = esa_lakes_low_smoke_year_observations_anomaly_df[column_name]
        colour  = LOW_SMOKE_AX_CMAP(i / max(len(column_names) - 1, 1))

        plot_kde_3d(
            low_smoke_ax,
            ser     = ser,
            zs      = i,
            color   = colour,
        )

    low_smoke_ax.set_title(
        LOW_SMOKE_AX_TITLE,
        fontsize = TITLE_FONTSIZE,
    )
    low_smoke_ax.set_xlabel(
        X_LABEL,
        fontsize = AXIS_LABEL_FONTSIZE,
    )
    low_smoke_ax.set_ylabel(
        Z_LABEL,
        fontsize = AXIS_LABEL_FONTSIZE,
    )
    low_smoke_ax.set_zlabel(
        Y_LABEL,
        fontsize = AXIS_LABEL_FONTSIZE,
    )
    low_smoke_ax.set_yticks(
        range(len(column_names)),
        labels  = [
                    column_name.split("_")[1]
                    for column_name
                    in column_names
                ],
    )
    low_smoke_ax.tick_params(
        labelsize = TICK_LABEL_FONTSIZE,
    )
    low_smoke_ax.view_init(
        elev = elevation,
        azim = azimuth,
    )

    low_smoke_ax.zaxis.set_pane_color(MEDIUM_GREY) # type: ignore[name-defined]
    low_smoke_ax.xaxis.set_pane_color(MEDIUM_GREY) # type: ignore[name-defined]
    low_smoke_ax.yaxis.set_pane_color(MEDIUM_GREY) # type: ignore[name-defined]

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
