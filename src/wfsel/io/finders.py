"""
wfsel.io.finders.

Written by William Chuter-Davies
"""

# Standard Library Imports
from pathlib  import Path


def find_files_by_extension(
    directory_path: Path,
    extension:     str,
) -> list[Path]:
    """
    Find files by an extension.

    Parameters
    ----------
    directory_path : Path
        The directory path
    extension : str
        The extension

    Returns
    -------
    list[Path]

    """
    paths = sorted(directory_path.glob(f"**/*.{extension}"))

    return paths
