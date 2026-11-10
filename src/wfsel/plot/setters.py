"""
Filename:   wfsel.plot.setters.py
Author:     William Chuter-Davies
"""

# Related Third-party Imports
import geopandas as gpd

from matplotlib.axes import Axes


def set_ax_xlim_to_gdf_total_bounds(
    ax:         Axes,
    gdf:        gpd.GeoDataFrame,
    padding:    float = 1,
) -> None:
    """
    Set xlim to the bounds of a geodataframe.

    Parameters
    ----------
    ax : Axes
        The axes
    gdf : gpd.GeoDataFrame
        The geodataframe
    padding : float
        The padding
    """
    minx, _, maxx, _ = gdf.total_bounds

    ax.set_xlim(
        minx - padding,
        maxx + padding,
    )


def set_ax_ylim_to_gdf_total_bounds(
    ax:         Axes,
    gdf:        gpd.GeoDataFrame,
    padding:    float = 1,
) -> None:
    """
    Set ylim to the bounds of a geodataframe.

    Parameters
    ----------
    ax : Axes
        The axes
    gdf : gpd.GeoDataFrame
        The geodataframe
    padding : float
        The padding
    """
    _, miny, _, maxy = gdf.total_bounds

    ax.set_ylim(
        miny - padding,
        maxy + padding,
    )
