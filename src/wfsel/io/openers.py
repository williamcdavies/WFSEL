"""
wfsel.io.openers.

Written by William Chuter-Davies
"""

# Standard Library Imports
from pathlib    import Path
from typing     import TextIO


def open_logstream(
    dir_path: Path,
) -> TextIO:
    """
    Open a logstream.

    Parameters
    ----------
    dir_path : Path
        The directory path

    Returns
    -------
    TextIO
        A logstream
    """
    dir_path.mkdir(
        parents     = True,
        exist_ok    = True,
    )

    logstream   = Path.open(
                    dir_path / "log.txt",
                    "a",
                )

    return logstream
