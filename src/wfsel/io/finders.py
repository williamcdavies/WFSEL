"""
Filename:   wfsel.io.finders.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path


def find_file_paths_by_extension(
    dir_path:       Path,
    file_extension: str,
) -> list[Path]:
    """
    Find file paths by extension.

    Parameters
    ----------
    dir_path : Path
        The directory path
    file_extension : str
        The file extension

    Returns
    -------
    list[Path]
        A list of file paths

    Raises
    ------
    FileNotFoundError
        If the directory path does not exist
    """
    if not dir_path.exists():
        message = f"directory not found: {dir_path}"

        raise FileNotFoundError(message)

    file_paths = list(dir_path.glob(f"**/*.{file_extension}"))

    return file_paths
