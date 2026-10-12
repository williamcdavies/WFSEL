r"""
utils.py

Description:
    Provides definitions for proc-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from datetime import datetime
from pathlib  import Path
from typing   import (
    Callable,
    Iterable,
    TextIO
)

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from lib.proc.objects import CompletedProcessLog


# Parser functions
# ==================================================================================================
def add_argument_output(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `output` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `output` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "-o", "--output",
        type     = Path,
        required = True,
        help     = "path to some output destination"
    )


def add_argument_workers(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `workers` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `workers` is of type :class:`int`. default=8.
    """
    parser.add_argument(
        "-w", "--workers",
        type    = int,
        default = 8,
        help    = "number of worker threads"
    )


def build_parser(
    prog:        str,
    description: str,
    *,
    positional_args: Iterable[Callable[[argparse.ArgumentParser], None]] = (),
    optional_args:   Iterable[Callable[[argparse.ArgumentParser], None]] = ()
) -> argparse.ArgumentParser:
    """
    Builds a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    prog : :class:`str`
        The program name

    description : :class:`str`
        The program description

    positional_args : Iterable[Callable[[:class:`argparse.ArgumentParser`], None]]
        The positional argument functions. default=()

    optional_args : Iterable[Callable[[:class:`argparse.ArgumentParser`], None]]
        The optional argument functions. default=()

    Returns
    -------
    A :class:`argparse.ArgumentParser`.
    """
    parser = argparse.ArgumentParser(
        prog        = prog,
        usage       = "%(prog)s [options]",
        description = description
    )

    for add in (
        *positional_args,
        *optional_args
    ):
        add(parser)

    return parser


# ==================================================================================================


# Validator functions
# ==================================================================================================
def argument_output_is_dir_or_missing(
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
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `output` does not exist or is a directory. `False`
    otherwise.
    """
    if (
        not output.exists() or
        output.is_dir()
    ):
        return True

    if loud:
        print(
            f"error: argument output: not a directory: {output}",
            file = sys.stderr
        )

    return False


def argument_output_is_file_or_missing(
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
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `output` does not exist or is a file. `False` otherwise.
    """
    if (
        not output.exists() or
        output.is_file()
    ):
        return True

    if loud:
        print(
            f"error: argument output: not a file: {output}",
            file = sys.stderr
        )

    return False


def arguments_are_valid(
    args:      argparse.Namespace,
    functions: Iterable[tuple[Callable[..., bool], str]]
) -> bool:
    """
    Validates `args`.

    Parameters
    ----------
    args : :class:`argparse.Namespace`
        The arguments

    functions : Iterable[tuple[Callable[..., bool], :class:`str`]]
        The functions

    Returns
    -------
    `True` if every argument passes its validator. `False` otherwise.
    """
    for (
        function,
        arg
    ) in functions:
        if not function(
            getattr(
                args,
                arg
            ),
            loud = True
        ):
            return False

    return True


# ==================================================================================================


# System functions
# ==================================================================================================
def get_file_paths_from_dir_path_by_extension(
    dir_path:  Path,
    extension: str
) -> list[Path]:
    """
    Returns the paths of all files in `dir_path` and its subdirectories
    with the extension `extension`.

    Parameters
    ----------
    dir_path : :class:`pathlib.Path`
        The directory

    extension : :class:`str`
        The extension

    Returns
    -------
    A sorted list of :class:`pathlib.Path`.
    """
    return sorted(dir_path.glob(f"**/*.{extension}"))


# ==================================================================================================


# Log functions
# ==================================================================================================
def open_logstream(
    dir_path: Path
) -> TextIO:
    """
    Opens the log file in `dir_path` in append mode.

    Parameters
    ----------
    dir_path : :class:`pathlib.Path`
        The directory

    Returns
    -------
    A :class:`typing.TextIO`.
    """
    return open(
        dir_path / "log.txt",
        "a"
    )


def write_completed_process_log_to_logstream(
    completed_process_log: CompletedProcessLog,
    logstream:             TextIO
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
    None.
    """
    logstream.write(f"{
        datetime
        .now()
        .isoformat()
    }\n")
    logstream.write(f"args:       {completed_process_log.args}\n")
    logstream.write(f"returncode: {completed_process_log.returncode}\n")
    logstream.write(f"stdout:     {completed_process_log.stdout}\n")
    logstream.write(f"stderr:     {completed_process_log.stderr}\n")
    logstream.write("-" * 100 + "\n")
    logstream.flush()


# ==================================================================================================


# Write functions
# ==================================================================================================
def write_df_to_csv(
    df:              pd.DataFrame,
    output_csv_path: Path
) -> None:
    """
    Writes `df` to `output_csv_path`.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The dataframe

    output_csv_path : :class:`pathlib.Path`
        The output csv path

    Returns
    -------
    None.

    Notes
    -----
    Creates the parent directories of `output_csv_path` if they do not
    exist.
    """
    output_csv_path.parent.mkdir(
        parents  = True,
        exist_ok = True
    )

    df.to_csv(output_csv_path)


# ==================================================================================================
