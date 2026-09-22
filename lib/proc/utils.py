r"""
utils.py

Description:
    Provides definitions for proc-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse

from pathlib import Path
from typing  import TextIO


def add_argument_output(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds an `output` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `output` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "-o", "--output",
        type     = Path,
        required = True,
        help     = """path to some output destination"""
    )


def argument_output_is_a_file(
    output: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `output`.

    Parameters
    ----------
    output : :class:`pathlib.Path`
        The argument `output`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `output` does not exist, or exists as a file. `False`
    otherwise.
    """
    if not output.exists() or output.is_file():
        return True

    if loud:
        print(f"""error: argument output: not a file: {output}""")

    return False


def argument_output_is_a_directory(
    output: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `output`.

    Parameters
    ----------
    output : :class:`pathlib.Path`
        The argument `output`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `output` does not exist, or exists as a directory.
    `False` otherwise.
    """
    if not output.exists() or output.is_dir():
        return True

    if loud:
        print(f"""error: argument output: not a directory: {output}""")

    return False


def open_logstream(
    output: Path
) -> TextIO:
    """
    Opens a log file for appending.

    Parameters
    ----------
    output : :class:`pathlib.Path`
        The output directory path

    Returns
    -------
    A :class:`typing.TextIO`.

    Notes
    -----
    The returned file object is a context manager.
    """
    return open(
        output / "log.txt",
        "a"
    )
