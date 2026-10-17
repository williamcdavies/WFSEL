"""
wfsel.core.logging.

Written by William Chuter-Davies
"""

# Standard Library Imports
from dataclasses import dataclass
from datetime    import (
    UTC,
    datetime,
)
from pathlib     import Path
from typing      import TextIO


@dataclass(kw_only = True)
class CompletedProcessLog:
    """Encapsualtes CompletedProcessLog."""

    args:       list[str]
    returncode: int
    stdout:     str
    stderr:     str


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
    return Path.open(
        directory_path / "log.txt",
        "a",
    )


def write_completed_process_log_to_logstream(
    completed_process_log: CompletedProcessLog,
    logstream:             TextIO,
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
