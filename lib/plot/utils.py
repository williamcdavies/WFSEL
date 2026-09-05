r"""
utils.py

Description:
   Provides definitions for plot-utility functions.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import geopandas as gpd

from matplotlib import pyplot as plt


def set_ax_xscale_to_lin(
    ax: plt.Axes # type: ignore
) -> None:
    """
    Sets `ax`'s x-axis to a lin scale.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to set the scale on

    Returns
    -------
    None
    """
    ax.set_xscale("lin")


def set_ax_xscale_to_log(
    ax: plt.Axes # type: ignore
) -> None:
    """
    Sets `ax`'s x-axis to a log scale.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to set the scale on

    Returns
    -------
    None
    """
    ax.set_xscale("log")


def set_ax_title(
    ax:    plt.Axes, # type: ignore
    title: str
) -> None:
    """
    Sets `ax`'s title to `title`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to set the title on

    title : :class:`str`
        The title

    Returns
    -------
    None
    """
    ax.set_title(title)


def set_ax_xlim_to_gdf_total_bounds(
    ax:  plt.Axes, # type: ignore
    gdf: gpd.GeoDataFrame
) -> None:
    ax.set_xlim(
        gdf.total_bounds[0] - 1, # minx
        gdf.total_bounds[2] + 1  # maxx
    )


def set_ax_ylim_to_gdf_total_bounds(
    ax:  plt.Axes, # type: ignore
    gdf: gpd.GeoDataFrame
) -> None:
    ax.set_ylim(
        gdf.total_bounds[1] - 1, # miny
        gdf.total_bounds[3] + 1  # maxy
    )


def set_ax_xticks_to_empty_list(
    ax:  plt.Axes, # type: ignore
) -> None:
    ax.set_xticks([])


def set_ax_yticks_to_empty_list(
    ax:  plt.Axes, # type: ignore
) -> None:
    ax.set_yticks([])