"""
Filename:   wfsel.plot.builders.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from collections.abc import Callable

# Related Third-party Imports
import matplotlib.pyplot as plt

from matplotlib.axes    import Axes
from matplotlib.figure  import Figure


def build_figure(
    nrows: int,
    ncols: int,
    *,
    plotter_fns:    list[Callable[[Axes], None]],
    decorator_fns:  list[Callable[[Axes], None]],
) -> Figure:
    """
    Build a figure

    Parameters
    ----------
    nrows : int
        The number of rows
    ncols : int
        The number of columns
    plotter_fns : list[Callable[[Axes], None]]
        The list of plotter functions
    decorator_fns : list[Callable[[Axes], None]]
        The list of decorator functions

    Returns
    -------
    Figure
        A figure
    """
    fig, axes = plt.subplots(
        nrows   = nrows,
        ncols   = ncols,
        squeeze = False,
    )

    for (
        ax,
        plotter_fn,
        decorator_fn,
    ) in zip(
        axes.flatten(),
        plotter_fns,
        decorator_fns,
        strict = True,
    ):
        plotter_fn(ax)
        decorator_fn(ax)

    return fig
