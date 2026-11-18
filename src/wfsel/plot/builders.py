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
    nrows:  int,
    ncols:  int,
    *,
    plotter_fns:    list[Callable[[Axes], None]],
    decorator_fns:  list[Callable[[Axes], None]],
    figsize:        tuple[float, float] | None  = None,
    sharex:         bool                        = False,
    sharey:         bool                        = False,
    pad:            float                       = 1.08,
    h_pad:          float | None                = None,
    w_pad:          float | None                = None,
) -> Figure:
    """
    Build a figure.

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
    figsize : tuple[float, float]
        The figure size
    sharex : bool
        The sharex argument
    sharey : bool
        The sharey argument
    pad : float
        The padding between the figure edge and the axes
    h_pad : float or None
        The vertical padding between the axes
    w_pad : float or None
        The horizontal padding between the axes

    Returns
    -------
    Figure
        A figure
    """
    fig, axes = plt.subplots(
        nrows   = nrows,
        ncols   = ncols,
        squeeze = False,
        sharex  = sharex,
        sharey  = sharey,
        figsize = figsize,
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

    fig.tight_layout(
        pad     = pad,
        h_pad   = h_pad,
        w_pad   = w_pad,
    )

    return fig
