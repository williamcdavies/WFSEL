"""
wfsel.plot.setters.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import geopandas as gpd

from matplotlib.axes import Axes


def set_ax_xlim_to_gdf_total_bounds(
    ax:  Axes,
    gdf: gpd.GeoDataFrame,
) -> None:
    """
    Set xlim to the bounds of a geodataframe.

    Parameters
    ----------
    ax : Axes
        The axes
    gdf : gpd.GeoDataFrame
        The geodataframe
    """
    ax.set_xlim(
        gdf.total_bounds[0] - 1,    # minx
        gdf.total_bounds[2] + 1,    # maxx
    )


def set_ax_ylim_to_gdf_total_bounds(
    ax:  Axes,
    gdf: gpd.GeoDataFrame,
) -> None:
    """
    Set ylim to the bounds of a geodataframe.

    Parameters
    ----------
    ax : Axes
        The axes
    gdf : gpd.GeoDataFrame
        The geodataframe
    """
    ax.set_ylim(
        gdf.total_bounds[1] - 1,    # miny
        gdf.total_bounds[3] + 1,    # maxy
    )
