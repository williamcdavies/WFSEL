"""
Filename:   wfsel.io.openers.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from pathlib    import Path
from typing     import TextIO


def open_file_in_append(
    file_path: Path,
) -> TextIO:
    """
    Open a file in append mode.

    Parameters
    ----------
    file_path : Path
        The file path

    Returns
    -------
    TextIO
        A file object
    """
    file_object = file_path.open("a")

    return file_object
