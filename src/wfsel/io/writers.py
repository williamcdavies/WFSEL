"""
wfsel.io.writers.

Written by William Chuter-Davies
"""

# Standard Library Imports
from datetime   import (
    UTC,
    datetime,
)
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
    output_file_path.parent.mkdir(
        parents     = True,
        exist_ok    = True,
    )

    df.to_csv(output_file_path)


def to_svg(
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
    output_file_path.parent.mkdir(
        parents     = True,
        exist_ok    = True,
    )

    fig.savefig(
        output_file_path,
        format      = "svg",
        bbox_inches = "tight",
    )


def to_logstream(
    completed_process_log:  CompletedProcessLog,
    logstream:              TextIO,
) -> None:
    """
    Write a completed process log to a logstream.

    Parameters
    ----------
    completed_process_log : CompletedProcessLog
        The completed process log
    logstream : TextIO
        The logstream
    """
    logstream.write(f"{
        datetime
        .now(tz = UTC)
        .isoformat()
    }\n")
    logstream.write(f"args:       {completed_process_log.args      }\n")
    logstream.write(f"returncode: {completed_process_log.returncode}\n")
    logstream.write(f"stdout:     {completed_process_log.stdout    }\n")
    logstream.write(f"stderr:     {completed_process_log.stderr    }\n")
    logstream.write("\n")
    logstream.flush()
