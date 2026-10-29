"""
view_map_of_hydro_lakes_in_united_states.py.

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse import (
    ArgumentParser,
    Namespace,
)

# Related Third-party Imports
import geopandas         as gpd
import matplotlib.pyplot as plt
import sqlalchemy

from matplotlib.axes import Axes

# Local Application/Library Specific Imports
from wfsel.utils.argparse_utils  import (
    arguments_are_valid as _arguments_are_valid,
    build_parser        as _build_parser,
    argument_is_subset_of_set,
)
from wfsel.io.arguments          import add_argument_output
from wfsel.exit_codes            import (
    EXIT_FAILURE,
    EXIT_SUCCESS,
)
from wfsel.geo.arguments         import add_argument_stusps
from wfsel.geo.literals          import TWO_LETTER_STATE_AND_POSSESSION_ABBREVIATIONS
from wfsel.plot.setters          import (
    set_ax_xlim_to_gdf_total_bounds,
    set_ax_ylim_to_gdf_total_bounds,
)
from wfsel.io.writers            import to_png
from wfsel.utils.geopandas_utils import filter_gdf_rows_by_values

PROG = "view_map_of_hydro_lakes_in_united_states.py"
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
            add_argument_stusps,
        ],
        optional_arguments   = [
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
        "stusps": argument_is_subset_of_set(list(TWO_LETTER_STATE_AND_POSSESSION_ABBREVIATIONS.keys())),
    }

    boolean = _arguments_are_valid(
        arguments,
        argument_name_to_validator,
    )

    return boolean


# ----------------------------------------------------------------------
# read functions
# ----------------------------------------------------------------------
def read_lakes_gdf(
    connection: sqlalchemy.Connection,
) -> gpd.GeoDataFrame:
    """
    Read PostGIS for lakes GeoDataFrame.

    Parameters
    ----------
    connection : sqlalchemy.Connection
        The connection

    Returns
    -------
    gpd.GeoDataFrame
    """
    query = """
        SELECT
            l.id, l.geom
        FROM lakes_points AS l
        """

    gdf = gpd.read_postgis(
        query,
        connection,
    )

    return gdf


def read_states_gdf(
    connection: sqlalchemy.Connection,
) -> gpd.GeoDataFrame:
    """
    Read PostGIS for states GeoDataFrame.

    Parameters
    ----------
    connection : sqlalchemy.Connection
        The connection

    Returns
    -------
    gpd.GeoDataFrame
    """
    query = """
        SELECT
            s.stusps, s.geom
        FROM states AS s
        """

    gdf = gpd.read_postgis(
        query,
        connection,
    )

    return gdf


# ----------------------------------------------------------------------
# plot functions
# ----------------------------------------------------------------------
def plot_states_gdf(
    ax:         Axes,
    states_gdf: gpd.GeoDataFrame,
) -> None:
    """
    Plot states GeoDataFrame.

    Parameters
    ----------
    ax : Axes
        The Axes
    states_gdf : gpd.GeoDataFrame
        The states
    """
    states_gdf.plot(
        ax        = ax,
        edgecolor = "#000000",
        facecolor = "#FFFFFF",
    )


def plot_target_states_gdf(
    ax:                Axes,
    target_states_gdf: gpd.GeoDataFrame,
) -> None:
    """
    Plot target states GeoDataFrame.

    Parameters
    ----------
    ax : Axes
        The Axes
    target_states_gdf : gpd.GeoDataFrame
        The target states
    """
    target_states_gdf.plot(
        ax        = ax,
        edgecolor = "#000000",
        facecolor = "#A9C8E9",
    )


def plot_target_lakes_gdf(
    ax:               Axes,
    target_lakes_gdf: gpd.GeoDataFrame,
) -> None:
    """
    Plot target lakes GeoDataFrame.

    Parameters
    ----------
    ax : Axes
        The Axes
    target_lakes_gdf : gpd.GeoDataFrame
        The target lakes
    """
    target_lakes_gdf.plot(
        ax         = ax,
        color      = "#000000",
        markersize = 2,
    )


def plot_on_ax(
    ax: Axes,
    *,
    states_gdf:        gpd.GeoDataFrame,
    target_states_gdf: gpd.GeoDataFrame,
    target_lakes_gdf:  gpd.GeoDataFrame,
) -> None:
    """
    Plot on Axes.

    Parameters
    ----------
    ax : Axes
        The axes
    states_gdf : gpd.GeoDataFrame
        The states
    target_states_gdf : gpd.GeoDataFrame
        The target states
    target_lakes_gdf : gpd.GeoDataFrame
        The target lakes
    """
    plot_states_gdf(
        ax,
        states_gdf,
    )
    plot_target_states_gdf(
        ax,
        target_states_gdf,
    )
    plot_target_lakes_gdf(
        ax,
        target_lakes_gdf,
    )


# ----------------------------------------------------------------------
# set functions
# ----------------------------------------------------------------------
def set_ax_properties(
    ax:                Axes,
    target_states_gdf: gpd.GeoDataFrame,
) -> None:
    """
    Set Axes properties.

    Parameters
    ----------
    ax : Axes
        The Axes
    target_states_gdf : gpd.GeoDataFrame
        The target states
    """
    set_ax_xlim_to_gdf_total_bounds(
        ax,
        target_states_gdf,
    )
    set_ax_ylim_to_gdf_total_bounds(
        ax,
        target_states_gdf,
    )
    ax.set_xticks([])
    ax.set_yticks([])


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

    with sqlalchemy.create_engine("postgresql+psycopg://localhost/spatial").connect() as connection:
        states_gdf = read_states_gdf(connection)
        lakes_gdf  = read_lakes_gdf(connection)

    lakes_states_gdf  = gpd.sjoin(
        lakes_gdf,
        states_gdf,
        predicate = "within",
    )
    target_states_gdf = filter_gdf_rows_by_values(
        states_gdf,
        "stusps",
        arguments.stusps,
    )
    target_lakes_gdf  = filter_gdf_rows_by_values(
        lakes_states_gdf,
        "stusps",
        arguments.stusps,
    )

    (
        fig,
        ax,
    ) = plt.subplots()

    plot_on_ax(
        ax,
        states_gdf        = states_gdf,
        target_states_gdf = target_states_gdf,
        target_lakes_gdf  = target_lakes_gdf,
    )

    set_ax_properties(
        ax,
        target_states_gdf,
    )

    to_png(
        fig,
        arguments.output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
