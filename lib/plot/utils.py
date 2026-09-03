r"""
utils.py

Description:
   Provides definitions for plot-utility functions.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import geopandas         as gpd
import matplotlib.pyplot as plt


def set_ax_lims_to_gdf_total_bounds(
    ax:     plt.Axes,
    gdf:    gpd.GeoDataFrame,
    *,
    buffer: float = 1
) -> None:
    """
    Sets `ax`'s x/y limits to `gdf`'s total bounds, padded by `buffer`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to set limits on

    gdf : :class:`geopandas.GeoDataFrame`
        The :class:`geopandas.GeoDataFrame`

    buffer : float
        Unit padding added to each side of total bounds. default=1

    Returns
    -------
    None
    """
    (
        minx, 
        miny, 
        maxx, 
        maxy
    ) = gdf.total_bounds

    ax.set_xlim(minx - buffer, maxx + buffer)
    ax.set_ylim(miny - buffer, maxy + buffer)


def set_ax_ticks_to_empty_lists(
    ax: plt.Axes
) -> None:
    """
    Clears `ax`'s x/y ticks.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to clear ticks on

    Returns
    -------
    None
    """
    ax.set_xticks([])
    ax.set_yticks([])