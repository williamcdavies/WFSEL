r"""
utils.py

Description:
    Provides definitions for plot-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path

# Related Third-party Imports
import geopandas as gpd

from matplotlib.axes   import Axes
from matplotlib.figure import Figure


# Export functions
# ==================================================================================================
def save_figure(
    figure: Figure,
    output: Path
) -> None:
    """
    Saves `figure` to `output`.

    Parameters
    ----------
    figure : :class:`matplotlib.figure.Figure`
        The figure

    output : :class:`pathlib.Path`
        The output file path

    Returns
    -------
    None.

    Notes
    -----
    Creates the parent of `output` if it does not exist.
    """
    output.parent.mkdir(
        parents  = True,
        exist_ok = True
    )

    figure.savefig(
        output,
        dpi         = 300,
        bbox_inches = "tight"
    )


# ==================================================================================================


# Limit functions
# ==================================================================================================
def set_ax_xlim_to_gdf_total_bounds(
    ax:  Axes,
    gdf: gpd.GeoDataFrame
) -> None:
    """
    Sets `ax`'s x-axis limits to `gdf`'s total bounds, padded by 1.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes

    gdf : :class:`geopandas.GeoDataFrame`
        The geodataframe

    Returns
    -------
    None.

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
    ax:  Axes,
    gdf: gpd.GeoDataFrame
) -> None:
    """
    Sets `ax`'s y-axis limits to `gdf`'s total bounds, padded by 1.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes

    gdf : :class:`geopandas.GeoDataFrame`
        The geodataframe

    Returns
    -------
    None.

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


# ==================================================================================================


# Scale functions
# ==================================================================================================
def set_ax_xscale_to_linear(
    ax: Axes
) -> None:
    """
    Sets `ax`'s x-axis to a linear scale.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes

    Returns
    -------
    None.
    """
    ax.set_xscale("linear")


def set_ax_xscale_to_log(
    ax: Axes
) -> None:
    """
    Sets `ax`'s x-axis to a log scale.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes

    Returns
    -------
    None.
    """
    ax.set_xscale("log")


def set_ax_yscale_to_linear(
    ax: Axes
) -> None:
    """
    Sets `ax`'s y-axis to a linear scale.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes

    Returns
    -------
    None.
    """
    ax.set_yscale("linear")


def set_ax_yscale_to_log(
    ax: Axes
) -> None:
    """
    Sets `ax`'s y-axis to a log scale.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes

    Returns
    -------
    None.
    """
    ax.set_yscale("log")


# ==================================================================================================


# Tick functions
# ==================================================================================================
def force_ax_xtick_visibility(
    ax: Axes,
    *,
    on: bool = True
) -> None:
    """
    Forces the visibility of `ax`'s x-axis tick labels.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes

    on : :class:`bool`
        If `True`, shows `ax`'s x-axis tick labels. If `False`, hides `ax`'s
        x-axis tick labels. default=True

    Returns
    -------
    None.
    """
    ax.tick_params(labelbottom = on)


def force_ax_ytick_visibility(
    ax: Axes,
    *,
    on: bool = True
) -> None:
    """
    Forces the visibility of `ax`'s y-axis tick labels.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes

    on : :class:`bool`
        If `True`, shows `ax`'s y-axis tick labels. If `False`, hides `ax`'s
        y-axis tick labels. default=True

    Returns
    -------
    None.
    """
    ax.tick_params(labelleft = on)


def set_ax_xticks_to_empty_list(
    ax: Axes
) -> None:
    """
    Clears `ax`'s x-axis ticks.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes

    Returns
    -------
    None.
    """
    ax.set_xticks([])


def set_ax_yticks_to_empty_list(
    ax: Axes
) -> None:
    """
    Clears `ax`'s y-axis ticks.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes

    Returns
    -------
    None.
    """
    ax.set_yticks([])


# ==================================================================================================
