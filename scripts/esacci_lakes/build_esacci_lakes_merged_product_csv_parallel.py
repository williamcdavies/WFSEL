"""
build_esacci_lakes_merged_product_csv_parallel.py.

Written by William Chuter-Davies
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
from pathlib            import Path
from subprocess         import run

# Related Third-party Imports
from tqdm import tqdm

# Local Application/Library Specific Imports
from wfsel.exit_codes                     import (
    EXIT_FAILURE,
    EXIT_SUCCESS,
)
from wfsel.io.arguments                   import add_argument_output
from wfsel.io.finders                     import find_files_by_extension
from wfsel.io.models                      import CompletedProcessLog
from wfsel.io.openers                     import open_logstream
from wfsel.io.writers                     import to_logstream
from wfsel.sources.esacci_lakes.arguments import (
    add_argument_esacci_lakes_merged_product_dir_path,
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_static_lake_mask_nc_path,
)
from wfsel.utils.argparse_utils           import (
    argument_is_directory,
    argument_is_file,
)
from wfsel.utils.argparse_utils           import (
    arguments_are_valid as _arguments_are_valid,
    build_parser        as _build_parser,
)

PROG = "build_esacci_lakes_merged_product_csv_parallel.py"
DESC = ""

DATE_STRING_FIELD_INDEX = 5
YEAR_STRING_SLICE       = slice(
    0,
    4,
)
MONTH_STRING_SLICE      = slice(
    4,
    6,
)

MAX_WORKERS = 8


# ----------------------------------------------------------------------
# setup functions
# ----------------------------------------------------------------------
def build_parser(
) -> ArgumentParser:
    """
    Wrap build_parser.

    Returns
    -------
    ArgumentParser

    """
    parser = ArgumentParser(
        prog        = PROG,
        description = DESC,
        usage       = "%(prog)s [options]",
    )

    parser = _build_parser(
        parser,
        positional_arguments = [
            add_argument_esacci_lakes_metadata_csv_path,
            add_argument_esacci_lakes_static_lake_mask_nc_path,
            add_argument_esacci_lakes_merged_product_dir_path,
        ],
        optional_arguments   = [
            add_argument_output,
        ],
    )

    return parser


def arguments_are_valid(
    arguments: Namespace,
) -> bool:
    """
    Wrap arguments_are_valid.

    Parameters
    ----------
    arguments : Namespace
        The arguments

    Returns
    -------
    bool

    """
    argument_name_to_validator = {
        "esacci_lakes_metadata_csv_path":        argument_is_file,
        "esacci_lakes_static_lake_mask_nc_path": argument_is_file,
        "esacci_lakes_merged_product_dir_path":  argument_is_directory,
        "output":                                argument_is_directory,
    }

    boolean = _arguments_are_valid(
        arguments,
        argument_name_to_validator,
    )

    return boolean


# ----------------------------------------------------------------------
# subprocess functions
# ----------------------------------------------------------------------
def run_build_esacci_lakes_merged_product_csv(
    *,
    esacci_lakes_metadata_csv_path:        Path,
    esacci_lakes_static_lake_mask_nc_path: Path,
    esacci_lakes_merged_product_nc_path:   Path,
    output_file_path:                      Path,
) -> CompletedProcessLog:
    """
    Run `build_esacci_lakes_merged_product_csv.py` as a subprocess.

    Parameters
    ----------
    esacci_lakes_metadata_csv_path : Path
        The ESA CCI Lakes metadata path
    esacci_lakes_static_lake_mask_nc_path : Path
        The ESA CCI Lakes static lake mask path
    esacci_lakes_merged_product_nc_path : Path
        The ESA CCI Lakes merged product path
    output_file_path : Path
        The output file path

    Returns
    -------
    CompletedProcessLog

    """
    completed_process = run(
        [
            sys.executable,
            f"{Path(__file__).resolve().parent / "build_esacci_lakes_merged_product_csv.py"}",
            str(esacci_lakes_metadata_csv_path),
            str(esacci_lakes_static_lake_mask_nc_path),
            str(esacci_lakes_merged_product_nc_path),
            "-o", str(output_file_path),
        ],
        capture_output = True,
        check          = False,
        text           = True,
    )

    completed_process_log = CompletedProcessLog(
        args       = completed_process.args,
        returncode = completed_process.returncode,
        stdout     = completed_process.stdout,
        stderr     = completed_process.stderr,
    )

    return completed_process_log


def submit_build_esacci_lakes_merged_product_csv(
    executor: ThreadPoolExecutor,
    *,
    esacci_lakes_metadata_csv_path:        Path,
    esacci_lakes_static_lake_mask_nc_path: Path,
    esacci_lakes_merged_product_nc_path:   Path,
    output_file_path:                      Path,
) -> Future:
    """
    Submit `build_esacci_lakes_merged_product_csv.py`.

    Parameters
    ----------
    executor : ThreadPoolExecutor
        The executor
    esacci_lakes_metadata_csv_path : Path
        The ESA CCI Lakes metadata path
    esacci_lakes_static_lake_mask_nc_path : Path
        The ESA CCI Lakes static lake mask path
    esacci_lakes_merged_product_nc_path : Path
        The ESA CCI Lakes merged product path
    output_file_path : Path
       The output file path

    Returns
    -------
    Future

    """
    future = executor.submit(
        run_build_esacci_lakes_merged_product_csv,
        esacci_lakes_metadata_csv_path        = esacci_lakes_metadata_csv_path,
        esacci_lakes_static_lake_mask_nc_path = esacci_lakes_static_lake_mask_nc_path,
        esacci_lakes_merged_product_nc_path   = esacci_lakes_merged_product_nc_path,
        output_file_path                      = output_file_path,
    )

    return future


def submit_build_esacci_lakes_merged_product_csvs(
    executor: ThreadPoolExecutor,
    *,
    esacci_lakes_metadata_csv_path:        Path,
    esacci_lakes_static_lake_mask_nc_path: Path,
    esacci_lakes_merged_product_nc_paths:  list[Path],
    output_file_paths:                     list[Path],
) -> list[Future]:
    """
    Submit `compute_esacci_lakes_merged_product_csv.py`s.

    Parameters
    ----------
    executor : ThreadPoolExecutor
        The executor
    esacci_lakes_metadata_csv_path : Path
        The ESA CCI Lakes metadata path
    esacci_lakes_static_lake_mask_nc_path : Path
        The ESA CCI Lakes static lake mask path
    esacci_lakes_merged_product_nc_paths : list[Path]
        The ESA CCI Lakes merged product paths
    output_file_paths : list[Path]
        The output file paths

    Returns
    -------
    list[Future]

    """
    futures = [
        submit_build_esacci_lakes_merged_product_csv(
            executor,
            esacci_lakes_metadata_csv_path        = esacci_lakes_metadata_csv_path,
            esacci_lakes_static_lake_mask_nc_path = esacci_lakes_static_lake_mask_nc_path,
            esacci_lakes_merged_product_nc_path   = esacci_lakes_merged_product_nc_path,
            output_file_path                      = output_file_path,
        )
        for (
            esacci_lakes_merged_product_nc_path,
            output_file_path,
        ) in zip(
            esacci_lakes_merged_product_nc_paths,
            output_file_paths,
            strict = True,
        )
    ]

    return futures


# ----------------------------------------------------------------------
# output file path functions
# ----------------------------------------------------------------------
def build_output_file_path(
    esacci_lakes_merged_product_nc_path: Path,
    directory_path:                      Path,
) -> Path:
    """
    Build an output file path.

    Parameters
    ----------
    esacci_lakes_merged_product_nc_path : Path
        The ESA CCI Lakes merged product path
    directory_path : Path
        The directory path

    Returns
    -------
    Path

    """
    stem             = esacci_lakes_merged_product_nc_path.stem
    date_string      = stem.split("-")[DATE_STRING_FIELD_INDEX]
    year_string      = date_string[YEAR_STRING_SLICE]
    month_string     = date_string[MONTH_STRING_SLICE]
    output_file_path = directory_path / year_string / month_string / f"{stem}.csv"

    return output_file_path


def build_output_file_paths(
    esacci_lakes_merged_product_nc_paths: list[Path],
    directory_path:                       Path,
) -> list[Path]:
    """
    Build output file paths.

    Parameters
    ----------
    esacci_lakes_merged_product_nc_paths : list[Path]
        The ESA CCI Lakes merged product paths
    directory_path : Path
        The directory path

    Returns
    -------
    list[Path]

    """
    output_file_paths = [
        build_output_file_path(
            esacci_lakes_merged_product_nc_path,
            directory_path,
        )
        for esacci_lakes_merged_product_nc_path
        in esacci_lakes_merged_product_nc_paths
    ]

    return output_file_paths


# ----------------------------------------------------------------------
# entry point
# ----------------------------------------------------------------------
def main(
) -> int:
    """
    Entry point.

    Returns
    -------
    int

    """
    args = build_parser().parse_args()

    if not arguments_are_valid(args):
        return EXIT_FAILURE

    merged_product_nc_paths = find_files_by_extension(
        args.esacci_lakes_merged_product_dir_path,
        "nc",
    )
    output_file_paths       = build_output_file_paths(
        merged_product_nc_paths,
        args.output,
    )

    with (
        ThreadPoolExecutor(max_workers = MAX_WORKERS) as executor,
        open_logstream(args.output)                   as logstream,
    ):
        futures = submit_build_esacci_lakes_merged_product_csvs(
            executor,
            esacci_lakes_metadata_csv_path        = args.esacci_lakes_metadata_csv_path,
            esacci_lakes_static_lake_mask_nc_path = args.esacci_lakes_static_lake_mask_nc_path,
            esacci_lakes_merged_product_nc_paths  = merged_product_nc_paths,
            output_file_paths                     = output_file_paths,
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
