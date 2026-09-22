r"""
utils.py

Description:
    Provides definitions for plot-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
from datetime import datetime
from pathlib  import Path

# Related Third-party Imports
import geopandas as gpd

from matplotlib import pyplot as plt


def set_ax_xlim_to_gdf_total_bounds(
    ax:  plt.Axes, # type: ignore
    gdf: gpd.GeoDataFrame
) -> None:
    """
    Sets `ax`'s x-axis limits to `gdf`'s total bounds, padded by 1.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to set limits on

    gdf : :class:`geopandas.GeoDataFrame`
        The geodataframe

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If `gdf` is empty.
    """
    if gdf.empty:
        raise ValueError("expected `gdf` to be non-empty")

    ax.set_xlim(
        gdf.total_bounds[0] - 1, # minx
        gdf.total_bounds[2] + 1  # maxx
    )


def set_ax_ylim_to_gdf_total_bounds(
    ax:  plt.Axes, # type: ignore
    gdf: gpd.GeoDataFrame
) -> None:
    """
    Sets `ax`'s y-axis limits to `gdf`'s total bounds, padded by 1.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to set limits on

    gdf : :class:`geopandas.GeoDataFrame`
        The geodataframe

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If `gdf` is empty.
    """
    if gdf.empty:
        raise ValueError("expected `gdf` to be non-empty")

    ax.set_ylim(
        gdf.total_bounds[1] - 1, # miny
        gdf.total_bounds[3] + 1  # maxy
    )


def set_ax_xscale_to_lin(
    ax: plt.Axes # type: ignore
) -> None:
    """
    Sets `ax`'s x-axis to a linear scale.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to set the scale on

    Returns
    -------
    None
    """
    ax.set_xscale("linear")


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


def set_ax_xticks_to_empty_list(
    ax: plt.Axes # type: ignore
) -> None:
    """
    Clears `ax`'s x-axis ticks.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to clear ticks on

    Returns
    -------
    None
    """
    ax.set_xticks([])


def set_ax_yticks_to_empty_list(
    ax: plt.Axes # type: ignore
) -> None:
    """
    Clears `ax`'s y-axis ticks.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to clear ticks on

    Returns
    -------
    None
    """
    ax.set_yticks([])


def force_ax_xtick_visibility(
    ax: plt.Axes, # type: ignore
    *,
    on: bool = True
) -> None:
    """
    Forces `ax`'s x-axis tick labels to be shown or hidden.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to set x-axis tick label visibility on

    on : :class:`bool`
        If `True`, shows `ax`'s x-axis tick labels. If `False`, hides
        them. default=True

    Returns
    -------
    None
    """
    ax.tick_params(labelbottom = on)


def force_ax_ytick_visibility(
    ax: plt.Axes, # type: ignore
    *,
    on: bool = True
) -> None:
    """
    Forces `ax`'s y-axis tick labels to be shown or hidden.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to set y-axis tick label visibility on

    on : :class:`bool`
        If `True`, shows `ax`'s y-axis tick labels. If `False`, hides
        them. default=True

    Returns
    -------
    None
    """
    ax.tick_params(labelleft = on)


def save_figure(
    figure: plt.Figure, # type: ignore
    prog:   str,
    time:   str,
    name:   str
) -> None:
    """
    Saves `figure` to `{prog}/`.

    Parameters
    ----------
    figure : :class:`matplotlib.figure.Figure`
        The figure to save

    prog : :class:`str`
        The program name

    time : :class:`str`
        The program time

    name : :class:`str`
            The output file name

    Returns
    -------
    None
    """
    fdir  = Path(f"data/dv/{prog}_{time}")

    fdir.mkdir(
        parents  = True,
        exist_ok = True
    )

    figure.savefig(
        fdir / (name + ".png"),
        dpi         = 300,
        bbox_inches = "tight"
    )
