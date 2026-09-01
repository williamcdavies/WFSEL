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
from lib.io.vars import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)

PROG = "view_lakes_within_states.py"


def get_gdf_from_postgis(
    query:       str,
    connection:  sqlalchemy.Connection
) -> gpd.GeoDataFrame:
    """
    Returns a `geopandas.GeoDataFrame` from a query and an `sqlachemy.Connection`.

    Parameters
    ----------
    query : :class:`str`
        The query

    connection : :class:`sqlachemy.Connection`
        The connection

    Notes
    -----
    Internal `geopandas.read_postgis` call assumes geom_col="geom".
    """
    return gpd.read_postgis(
        query,
        connection
    )


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(
        prog=PROG,
        usage="%(prog)s [options]",
        description="""Produces a map visualisation of all lakes within a set of states."""
    )
    
    # Valued arguments
    parser.add_argument(
        "--stusps",
        nargs="+",
        type=str,
        required=True,
        help="list of two–letter state and possession abbreviations as defined in Mailing Standards of the United States Postal Service Publication 28 - Postal Addressing Standards"
    )

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================

    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    with sqlalchemy.create_engine("postgresql+psycopg://localhost/spatial").connect() as conn:
            lakes_query = """
                SELECT
                    l.id,
                    l.geom
                FROM lakes_points AS l
                """
            lakes_gdf = get_gdf_from_postgis(lakes_query, conn)

            states_query = """
                SELECT
                    s.stusps,
                    s.geom
                FROM states AS s
                """
            states_gdf = get_gdf_from_postgis(states_query, conn)

    target_states_gdf = states_gdf[states_gdf["stusps"].isin(args.stusps)]
    target_lakes_gdf  = gpd.sjoin(
        lakes_gdf,
        target_states_gdf,
        how="inner",
        predicate="within"
    )

    fig, ax = plt.subplots()

    states_gdf.plot(
        ax=ax,
        facecolor="#FFFFFF",
        edgecolor="#000000"
    )
    target_states_gdf.plot(
        ax=ax,
        facecolor="#A9C8E9",
        edgecolor="#000000"
    )
    target_lakes_gdf.plot(
        ax=ax,
        color="#000000",
        markersize=2
    )

    minx, miny, maxx, maxy = target_states_gdf.total_bounds

    ax.set_aspect("equal")
    ax.set_xlim(minx - 1, maxx + 1)
    ax.set_ylim(miny - 1, maxy + 1)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout()
    plt.show()
    
    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == "__main__":
    sys.exit(main())
