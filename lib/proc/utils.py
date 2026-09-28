r"""
utils.py

Description:
    Provides definitions for proc-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse

from datetime import datetime
from pathlib  import Path
from typing   import TextIO

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from lib.proc.objects import CompletedProcessLog


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


def write_completed_process_log_to_logstream(
    completed_process_log: CompletedProcessLog,
    *,
    logstream: TextIO
) -> None:
    """
    Writes `completed_process_log` to `logstream`.

    Parameters
    ----------
    completed_process_log : :class:`lib.proc.objects.CompletedProcessLog`
        The completed process log

    logstream : :class:`typing.TextIO`
        The writable file object

    Returns
    -------
    None
    """
    logstream.write(f"{datetime.now().isoformat()}\n")
    logstream.write(f"args:       {completed_process_log.args}\n")
    logstream.write(f"returncode: {completed_process_log.returncode}\n")
    logstream.write(f"stdout:     {completed_process_log.stdout}\n")
    logstream.write(f"stderr:     {completed_process_log.stderr}\n")
    logstream.write("-" * 100 + "\n")
    logstream.flush()


def write_df_to_csv(
    df:     pd.DataFrame,
    output: Path
) -> None:
    """
    Writes `df` to `output`.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The dataframe

    output : :class:`pathlib.Path`
        The output file path

    Returns
    -------
    None
    """
    output.parent.mkdir(
        parents  = True,
        exist_ok = True
    )

    df.to_csv(output)


def get_dir_paths_by_extension(
    dir_path: Path,
    *,
    extension: str
) -> list[Path]:
    """
    Returns each `extension` file's path in `dir_path`.

    Parameters
    ----------
    dir_path : :class:`pathlib.Path`
        The directory

    extension : :class:`str`
        The file extension to match, without a leading period

    Returns
    -------
    A sorted list of :class:`pathlib.Path`.
    """
    return sorted(dir_path.glob(f"**/*.{extension}"))
