r"""
view_lakes_within_states.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

# Related Third-party Imports
import geopandas         as gpd
import matplotlib.pyplot as plt
import sqlalchemy

# Local Application/Library Specific Imports
from lib.geo.vars   import TWO_LETTER_STATE_AND_POSSESSION_ABBREVIATIONS
from lib.geo.utils  import (
    get_gdf_from_postgis,
    join_gdfs_on_within
)
from lib.io.vars    import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)
from lib.plot.utils import (
    set_ax_lims_to_gdf_total_bounds,
    set_ax_ticks_to_empty_lists
)

PROG = "view_lakes_within_states.py"


def add_argument_stusps(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `stusps` argument to a :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `stusps` is of type list[str].
    """
    parser.add_argument(
        "--stusps",
        nargs="+",
        type=str,
        required=True,
        help="""list of two-letter state and possession abbreviations as defined in Mailing Standards of the United States Postal Service Publication 28 - Postal Addressing Standards"""
    )


def argument_stusps_is_subset_of_two_letter_state_and_possession_abbreviations(
    stusps: list[str],
    *,
    loud:   bool = False
) -> bool:
    """
    Validates `stusps`.

    Parameters
    ----------
    stusps : list[str]
        The argument `stusps`

    loud : bool
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if every element in `stusps` is in
    `TWO_LETTER_STATE_AND_POSSESSION_ABBREVIATIONS`. `False` otherwise.
    """
    for element in stusps:
        if element not in TWO_LETTER_STATE_AND_POSSESSION_ABBREVIATIONS:
            if loud:
                print(f"""error: argument stusps: element not in `TWO_LETTER_STATE_AND_POSSESSION_ABBREVIATIONS`: {element}""")

            return False

    return True


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
        description="""Produces a map visualisation of all lakes within a set of states."""
    )

    # Optional arguments
    add_argument_stusps(parser)

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
    if not argument_stusps_is_subset_of_two_letter_state_and_possession_abbreviations(args.stusps, loud=True): 
        return False

    return True


def get_lakes_gdf(
    connection: sqlalchemy.Connection
) -> gpd.GeoDataFrame:
    """
    Returns a :class:`geopandas.GeoDataFrame` of all lakes.

    Parameters
    ----------
    connection : :class:`sqlalchemy.Connection`
        The connection

    Returns
    -------
    A :class:`geopandas.GeoDataFrame`.

    Notes
    -----
    Internal `geopandas.read_postgis` call assumes "lakes_points" is an
    existing table and that "id" and "geom" are existing columns in
    "lakes_points".
    """
    query = """
        SELECT
            l.id,
            l.geom
        FROM lakes_points AS l
        """

    return get_gdf_from_postgis(query, connection)


def get_states_gdf(
    connection: sqlalchemy.Connection
) -> gpd.GeoDataFrame:
    """
    Returns a :class:`geopandas.GeoDataFrame` of all states.

    Parameters
    ----------
    connection : :class:`sqlalchemy.Connection`
        The connection

    Returns
    -------
    A :class:`geopandas.GeoDataFrame`.

    Notes
    -----
    Internal `geopandas.read_postgis` call assumes "states" is an
    existing table and that "stusps" and "geom" are existing columns in
    "states".
    """
    query = """
        SELECT
            s.stusps,
            s.geom
        FROM states AS s
        """

    return get_gdf_from_postgis(query, connection)


def filter_gdf_by_stusps(
    gdf:    gpd.GeoDataFrame,
    stusps: list[str]
) -> gpd.GeoDataFrame:
    """
    Filters a :class:`geopandas.GeoDataFrame` to rows whose `stusps`
    column is in `stusps`.

    Parameters
    ----------
    gdf : :class:`geopandas.GeoDataFrame`
        The :class:`geopandas.GeoDataFrame`

    stusps : list[str]
        The target list of two-letter state and possession abbreviations

    Returns
    -------
    A :class:`geopandas.GeoDataFrame`.

    Notes
    -----
    Internal indexing call assumes "stusps" is an existing column in
    `gdf`.
    """
    return gdf[gdf["stusps"].isin(stusps)]


def plot_states_gdf(
    ax:         plt.Axes, # type: ignore
    states_gdf: gpd.GeoDataFrame
) -> None:
    """
    Plots `states_gdf` onto `ax`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    states_gdf : :class:`geopandas.GeoDataFrame`
        All states

    Returns
    -------
    None
    """
    states_gdf.plot(
        ax=ax,
        facecolor="#FFFFFF",
        edgecolor="#000000"
    )


def plot_target_states_gdf(
    ax:                plt.Axes, # type: ignore
    target_states_gdf: gpd.GeoDataFrame
) -> None:
    """
    Plots `target_states_gdf` onto `ax`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    target_states_gdf : :class:`geopandas.GeoDataFrame`
        The target states

    Returns
    -------
    None
    """
    target_states_gdf.plot(
        ax=ax,
        facecolor="#A9C8E9",
        edgecolor="#000000"
    )


def plot_target_lakes_gdf(
    ax:               plt.Axes, # type: ignore
    target_lakes_gdf: gpd.GeoDataFrame
) -> None:
    """
    Plots `target_lakes_gdf` onto `ax`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    target_lakes_gdf : :class:`geopandas.GeoDataFrame`
        The target lakes

    Returns
    -------
    None
    """
    target_lakes_gdf.plot(
        ax=ax,
        color="#000000",
        markersize=2
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

    with sqlalchemy.create_engine("postgresql+psycopg://localhost/spatial").connect() as connection:
        states_gdf = get_states_gdf(connection)
        lakes_gdf  = get_lakes_gdf(connection)

    lakes_states_gdf  = join_gdfs_on_within(
        lakes_gdf, 
        states_gdf
    )
    target_states_gdf = filter_gdf_by_stusps(
        states_gdf, 
        args.stusps
    )
    target_lakes_gdf  = filter_gdf_by_stusps(
        lakes_states_gdf, 
        args.stusps
    )

    _, ax = plt.subplots()

    plot_states_gdf(
        ax, 
        states_gdf
    )
    plot_target_states_gdf(
        ax, 
        target_states_gdf
    )
    plot_target_lakes_gdf(
        ax, 
        target_lakes_gdf
    )

    ax.set_aspect("equal")
    set_ax_lims_to_gdf_total_bounds(
        ax, 
        target_states_gdf
    )
    set_ax_ticks_to_empty_lists(ax)

    plt.tight_layout()
    plt.show()
    
    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
