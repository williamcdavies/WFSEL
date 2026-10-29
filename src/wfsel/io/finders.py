"""
Filename:   wfsel.io.finders.py
Author:     William Chuter-Davies
Modified:   29/10/26
"""

# Standard Library Imports
from pathlib import Path


def find_files_by_extension(
    dir_path:   Path,
    extension:  str,
) -> list[Path]:
    """
    Find files by extension.

    Parameters
    ----------
    dir_path : Path
        The directory path
    extension : str
        The extension

    Returns
    -------
    list[Path]
        A list of paths
    """
    paths = sorted(dir_path.glob(f"**/*.{extension}"))

    return paths
