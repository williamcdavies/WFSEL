"""
Filename:   wfsel.plot.plotters.py
Author:     William Chuter-Davies
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
from wfsel.plot.computers import compute_kde


def plot_kde_2d(
    ax: Axes,
    *,
    ser: pd.Series,
    **kwargs: Any,
) -> None:
    """
    Plot a KDE onto a 2D axes.

    Parameters
    ----------
    ax : Axes
        The axes
    ser : pd.Series[float]
        The series
    """
    x_values, y_values = compute_kde(ser)

    ax.plot(
        x_values,
        y_values,
        **kwargs,
    )


def plot_kde_3d(
    ax: Axes,
    *,
    ser:        pd.Series,
    z_value:    int,
    **kwargs: Any,
) -> None:
    """
    Plot a KDE onto a 3D axes.

    Parameters
    ----------
    ax : Axes
        The axes
    ser : pd.Series[float]
        The series
    z_value : int
        The z-value
    """
    x_values, y_values = compute_kde(ser)

    ax.plot(
        x_values,
        y_values,
        zs      = z_value,
        zdir    = "y",
        **kwargs,
    )


def plot_colorbar(
    ax: Axes,
    *,
    cmap:   mcolors.Colormap,
    vmin:   int,
    vmax:   int,
    **kwargs: Any,
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

    scalar_mappable = cm.ScalarMappable(
                        cmap    = cmap,
                        norm    = norm,
                    )

    plt.colorbar(
        scalar_mappable,
        ax      = ax,
        ticks   = range(
                    vmin,
                    vmax + 1,
                    vmax - 1,
                ),
        **kwargs,
    )
