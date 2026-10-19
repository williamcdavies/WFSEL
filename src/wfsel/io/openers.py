"""
wfsel.io.openers.

Written by William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path
from typing  import TextIO


def open_logstream(
    directory_path: Path,
) -> TextIO:
    """
    Open a log file in append mode.

    Parameters
    ----------
    directory_path : Path
        The directory path

    Returns
    -------
    TextIO
    """
    directory_path.mkdir(
        parents  = True,
        exist_ok = True,
    )

    logstream = Path.open(
        directory_path / "log.txt",
        "a",
    )

    return logstream
