"""
Filename:   etl_noaa_hms_parallel.py
Author:     William Chuter-Davies
Modified:   10/11/26
"""

# Standard Library Imports
import sys

from argparse           import (
                            ArgumentParser,
                            Namespace,
                        )
from concurrent.futures import (
                            Future,
                            ThreadPoolExecutor,
                            as_completed,
                        )
from datetime           import (
                            date,
                            timedelta,
                        )
from pathlib            import Path
from subprocess         import run

# Related Third-party Imports
from tqdm import tqdm

# Local Application/Library Specific Imports
from wfsel.arguments            import (
                                    add_argument_force,
                                    add_argument_output,
                                )
from wfsel.exit_codes           import (
                                    EXIT_FAILURE,
                                    EXIT_SUCCESS,
                                )
from wfsel.io.models            import CompletedProcessLog
from wfsel.io.openers           import open_logstream
from wfsel.io.writers           import to_logstream
from wfsel.utils.argparse_utils import (
                                    arguments_are_valid as _arguments_are_valid,
                                    build_parser        as _build_parser,
                                    argument_is_dir,
                                )

PROG    = "etl_noaa_hms_parallel.py"
DESC    = ""

MAX_WORKERS = 8


# ----------------------------------------------------------------------
# argument functions
# ----------------------------------------------------------------------
def add_argument_start_date(
    parser: ArgumentParser,
) -> None:
    """
    Add a "start_date" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "start_date",
        type = date.fromisoformat,
    )


def add_argument_end_date(
    parser: ArgumentParser,
) -> None:
    """
    Add a "end_date" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "end_date",
        type = date.fromisoformat,
    )


# ----------------------------------------------------------------------
# setup functions
# ----------------------------------------------------------------------
def build_parser(
) -> ArgumentParser:
    """
    Wrap _build_parser.

    Returns
    -------
    ArgumentParser
        A parser
    """
    parser  = ArgumentParser(
                prog        = PROG,
                description = DESC,
            )
    parser  = _build_parser(
                parser,
                positional_arguments    = [
                    add_argument_start_date,
                    add_argument_end_date,
                ],
                optional_arguments      = [
                    add_argument_force,
                    add_argument_output,
                ],
            )

    return parser


def arguments_are_valid(
    arguments: Namespace,
) -> bool:
    """
    Wrap _arguments_are_valid.

    Parameters
    ----------
    arguments : Namespace
        The arguments

    Returns
    -------
    bool
        True if all arguments are valid, False otherwise
    """
    argument_name_to_validator  = {
                                    "output": argument_is_dir,
                                }

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


# ----------------------------------------------------------------------
# subprocess functions
# ----------------------------------------------------------------------
def run_etl_noaa_hms(
    *,
    target_date:    date,
    force:          bool,
) -> CompletedProcessLog:
    """
    Run `etl_noaa_hms.py` as a subprocess.

    Parameters
    ----------
    target_date : date
        The target date
    force : bool
        The force argument

    Returns
    -------
    CompletedProcessLog
        A completed process log
    """
    cmd = [
            sys.executable,
            f"{Path(__file__).resolve().parent / "etl_noaa_hms.py"}",
            "ingest",
            str(target_date),
        ]

    if force:
        cmd.append("-f")

    completed_process   = run(
                            cmd,
                            capture_output  = True,
                            check           = False,
                            text            = True,
                        )

    completed_process_log   = CompletedProcessLog(
                                args        = completed_process.args,
                                returncode  = completed_process.returncode,
                                stdout      = completed_process.stdout,
                                stderr      = completed_process.stderr,
                            )

    return completed_process_log


def submit_etl_noaa_hms(
    executor: ThreadPoolExecutor,
    *,
    target_date:    date,
    force:          bool,
) -> Future:
    """
    Submit `etl_noaa_hms.py`.

    Parameters
    ----------
    executor : ThreadPoolExecutor
        The executor
    target_date : date
        The target date
    force : bool
        The force argument

    Returns
    -------
    Future
        A future
    """
    future  = executor.submit(
                run_etl_noaa_hms,
                target_date = target_date,
                force       = force,
            )

    return future


def submit_etl_noaa_hmss(
    executor: ThreadPoolExecutor,
    *,
    target_dates:   list[date],
    force:          bool,
) -> list[Future]:
    """
    Submit `etl_noaa_hms.py`s.

    Parameters
    ----------
    executor : ThreadPoolExecutor
        The executor
    target_dates : list[date]
        The list of target dates
    force : bool
        The force argument

    Returns
    -------
    list[Future]
        A list of futures
    """
    futures = [
                submit_etl_noaa_hms(
                    executor,
                    target_date = target_date,
                    force       = force,
                )
                for target_date
                in target_dates
            ]

    return futures


# ----------------------------------------------------------------------
# builder functions
# ----------------------------------------------------------------------
def build_target_dates(
    start_date: date,
    end_date:   date,
) -> list[date]:
    """
    Build a list of dates.

    Parameters
    ----------
    start_date : date
        The start date
    end_date : date
        The end date

    Returns
    -------
    list[date]
        A list of dates
    """
    delta   = end_date - start_date
    dates   = [
                start_date + timedelta(days = i)
                for i
                in range(delta.days + 1)
            ]

    return dates


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main(
) -> int:
    """
    Run program.

    Returns
    -------
    int
        0 if program runs successfully, 1 otherwise
    """
    args = build_parser().parse_args()

    if not arguments_are_valid(args):
        return EXIT_FAILURE

    target_dates    = build_target_dates(
                        args.start_date,
                        args.end_date,
                    )

    with (
        ThreadPoolExecutor(max_workers = MAX_WORKERS)   as executor,
        open_logstream(args.output)                     as logstream,
    ):
        futures = submit_etl_noaa_hmss(
                    executor,
                    target_dates    = target_dates,
                    force           = args.force,
                )

        for future in tqdm(
            as_completed(futures),
            total = len(futures),
        ):
            completed_process_log = future.result()

            to_logstream(
                completed_process_log,
                logstream,
            )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
