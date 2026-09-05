r"""
utils.py

Description:
   Provides definitions for plot-utility functions.

Written by William Chuter-Davies
"""

# Related Third-party Imports
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
