"""
wfsel.core.plotting.

Written by William Chuter-Davies
"""

# Standard Library Imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

# Related Third-party Imports
if TYPE_CHECKING:
    from matplotlib.figure import Figure


def to_png(
    fig:              Figure,
    output_file_path: Path,
) -> None:
    """
    Write a Figure to a .png file.

    Parameters
    ----------
    fig : Figure
        The Figure
    output_file_path : Path
        The output file path
    """
    output_file_path.parent.mkdir(
        parents  = True,
        exist_ok = True,
    )

    fig.savefig(
        output_file_path,
        dpi         = 300,
        bbox_inches = "tight",
    )
