"""
Filename:   wfsel.io.writers.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from pathlib    import Path
from typing     import TextIO

# Related Third-party Imports
import pandas as pd

from matplotlib.figure import Figure

# Local Application/Library Specific Imports
from wfsel.io.models import CompletedProcessLog


def to_csv(
    df:                 pd.DataFrame,
    output_file_path:   Path,
) -> None:
    """
    Write a dataframe to a .csv file.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe
    output_file_path : Path
        The output file path
    """
    df.to_csv(output_file_path)


def to_svg(
    fig:                Figure,
    output_file_path:   Path,
) -> None:
    """
    Write a figure to a .svg file.

    Parameters
    ----------
    fig : Figure
        The figure
    output_file_path : Path
        The output file path
    """
    fig.savefig(
        output_file_path,
        format      = "svg",
        bbox_inches = "tight",
    )


def to_png(
    fig:                Figure,
    output_file_path:   Path,
) -> None:
    """
    Write a figure to a .png file.

    Parameters
    ----------
    fig : Figure
        The figure
    output_file_path : Path
        The output file path
    """
    fig.savefig(
        output_file_path,
        format      = "png",
        bbox_inches = "tight",
    )


def to_log(
    completed_process_log:  CompletedProcessLog,
    file_object:            TextIO,
) -> None:
    """
    Write a completed process log to a file.

    Parameters
    ----------
    completed_process_log : CompletedProcessLog
        The completed process log
    file_object : TextIO
        The file object
    """
    file_object.write(f"{completed_process_log}\n")
    file_object.flush()
