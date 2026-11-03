"""
Filename:   wfsel.plot.plotters.py
Author:     William Chuter-Davies
Modified:   03/11/26
"""

# Standard Library Imports
from typing import Any

# Related Third-party Imports
import matplotlib.colors    as mcolors
import matplotlib.pyplot    as plt
import pandas               as pd

from matplotlib         import cm
from matplotlib.axes    import Axes

# Local Application/Library Specific Imports
from wfsel.math.computers import compute_kde


def plot_kde_2d(
    ax: Axes,
    *,
    ser:        pd.Series[float],
    **kwargs:   Any,
) -> None:
    """
    Plot a KDE of a series onto a 2D axes.

    Parameters
    ----------
    ax : Axes
        The axes
    ser : pd.Series[float]
        The series
    """
    ser = ser.dropna()
    kde = compute_kde(ser)
    xs  = ser.sort_values()
    ys  = pd.Series(kde(xs))

    ax.plot(
        xs,
        ys,
        **kwargs,
    )


def plot_kde_3d(
    ax: Axes,
    *,
    ser:        pd.Series[float],
    zs:         int,
    **kwargs:   Any,
) -> None:
    """
    Plot a KDE of a series onto a 3D axes.

    Parameters
    ----------
    ax : Axes
        The axes
    ser : pd.Series[float]
        The series
    zs : int
        The zs
    """
    ser = ser.dropna()
    kde = compute_kde(ser)
    xs  = ser.sort_values()
    ys  = pd.Series(kde(xs))

    ax.plot(
        xs,
        ys,
        zs      = zs,
        zdir    = "y",
        **kwargs,
    )


def plot_colorbar(
    ax: Axes,
    *,
    cmap:       mcolors.Colormap,
    vmin:       int,
    vmax:       int,
    **kwargs:   Any,
) -> None:
    """
    Plot a colorbar onto an axes.

    Parameters
    ----------
    ax : Axes
        The axes
    cmap : mcolors.Colormap
        The colormap
    vmin : int
        The value minimum
    vmax : int
        The value maximum
    """
    norm    = mcolors.Normalize(
        vmin    = vmin,
        vmax    = vmax,
    )
    sm      = cm.ScalarMappable(
        cmap    = cmap,
        norm    = norm,
    )

    plt.colorbar(
        sm,
        ax      = ax,
        ticks   = range(
            vmin,
            vmax + 1,
            vmax - 1,
        ),
        **kwargs,
    )
