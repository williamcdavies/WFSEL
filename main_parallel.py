r"""
main_parallel.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from concurrent.futures import (
    Future,
    ThreadPoolExecutor,
    as_completed
)
from pathlib            import Path
from subprocess         import run

# Related Third-party Imports
from tqdm import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.proc import (
    add_argument_esacci_lakes_merged_product_dir_path,
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_static_lake_mask_nc_path,
    argument_esacci_lakes_merged_product_dir_path_is_dir,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_static_lake_mask_nc_path_exists,
    get_esacci_lakes_filename_time
)
from lib.proc.objects            import CompletedProcessLog
from lib.proc.utils              import (
    arguments_are_valid as _arguments_are_valid,
    build_parser        as _build_parser,

    add_argument_output,
    argument_output_is_dir_or_missing,
    get_file_paths_from_dir_by_extension,
    open_logstream,
    write_completed_process_log_to_logstream
)
from lib.proc.vars               import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)
from lib.time.utils              import (
    get_month_from_datetime,
    get_year_from_datetime
)


# Constants
# ==================================================================================================
PROG = "main_parallel.py"


# ==================================================================================================


# Parser functions
# ==================================================================================================
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
) -> argparse.ArgumentParser:
    """
    Builds a :class:`argparse.ArgumentParser`.

    Returns
    -------
    A :class:`argparse.ArgumentParser`.
    """
    return _build_parser(
        PROG,
        "Runs `main.py` in parallel.",
        positional_arguments = [
            add_argument_esacci_lakes_metadata_csv_path,
            add_argument_esacci_lakes_static_lake_mask_nc_path,
            add_argument_esacci_lakes_merged_product_dir_path
        ],
        optional_arguments   = [
            add_argument_workers,
            add_argument_output
        ]
    )


# ==================================================================================================


# System functions
# ==================================================================================================
def get_esacci_lakes_merged_product_output_file_path(
    output_dir_path:                     Path,
    esacci_lakes_merged_product_nc_path: Path
) -> Path:
    """
    Returns the output file path for an ESA CCI Lakes merged product netCDF
    file.

    Parameters
    ----------
    output_dir_path : :class:`pathlib.Path`
        The output directory path

    esacci_lakes_merged_product_nc_path : :class:`pathlib.Path`
        The path to some ESA CCI Lakes merged product netCDF file

    Returns
    -------
    A :class:`pathlib.Path`.
    """
    time  = get_esacci_lakes_filename_time(esacci_lakes_merged_product_nc_path)
    year  = get_year_from_datetime(time)
    month = get_month_from_datetime(time)
    stem  = esacci_lakes_merged_product_nc_path.stem

    return output_dir_path / year / month / f"{stem}.csv"


def get_esacci_lakes_merged_product_output_file_paths(
    output_dir_path:                      Path,
    esacci_lakes_merged_product_nc_paths: list[Path]
) -> list[Path]:
    """
    Returns the output file paths for all ESA CCI Lakes merged product netCDF
    files.

    Parameters
    ----------
    output_dir_path : :class:`pathlib.Path`
        The output directory path

    esacci_lakes_merged_product_nc_paths : list[:class:`pathlib.Path`]
        Paths to some ESA CCI Lakes merged product netCDF files

    Returns
    -------
    A list of :class:`pathlib.Path`.
    """
    return [
        get_esacci_lakes_merged_product_output_file_path(
            output_dir_path,
            esacci_lakes_merged_product_nc_path
        )
        for esacci_lakes_merged_product_nc_path
        in esacci_lakes_merged_product_nc_paths
    ]


def get_main_py_future(
    executor: ThreadPoolExecutor,
    *,
    esacci_lakes_metadata_csv_path:        Path,
    esacci_lakes_static_lake_mask_nc_path: Path,
    esacci_lakes_merged_product_nc_path:   Path,
    output_file_path:                      Path
) -> Future:
    """
    Submits a main.py subprocess and returns its future.

    Parameters
    ----------
    executor : :class:`concurrent.futures.ThreadPoolExecutor`
        The executor to submit to

    esacci_lakes_metadata_csv_path : :class:`pathlib.Path`
        The path to the `lakescci_v2.1.0_metadata.csv` file as provided by ESA
        Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0

    esacci_lakes_static_lake_mask_nc_path : :class:`pathlib.Path`
        The path to the `ESA_CCI_static_lake_mask.nc` file as provided by ESA
        Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0

    esacci_lakes_merged_product_nc_path : :class:`pathlib.Path`
        The path to some
        `ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.nc` file as
        provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake
        products, Version 3.0

    output_file_path : :class:`pathlib.Path`
        The output file path

    Returns
    -------
    A :class:`concurrent.futures.Future`.
    """
    return executor.submit(
        main_py,
        esacci_lakes_metadata_csv_path        = esacci_lakes_metadata_csv_path,
        esacci_lakes_static_lake_mask_nc_path = esacci_lakes_static_lake_mask_nc_path,
        esacci_lakes_merged_product_nc_path   = esacci_lakes_merged_product_nc_path,
        output_file_path                      = output_file_path
    )


def get_main_py_futures(
    executor:                              ThreadPoolExecutor,
    esacci_lakes_metadata_csv_path:        Path,
    esacci_lakes_static_lake_mask_nc_path: Path,
    esacci_lakes_merged_product_nc_paths:  list[Path],
    output_file_paths:                     list[Path]
) -> list[Future]:
    """
    Submits a main.py subprocess for all ESA CCI Lakes merged product netCDF
    files and returns their futures.

    Parameters
    ----------
    executor : :class:`concurrent.futures.ThreadPoolExecutor`
        The executor to submit to

    esacci_lakes_metadata_csv_path : :class:`pathlib.Path`
        The path to the `lakescci_v2.1.0_metadata.csv` file as provided by ESA
        Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0

    esacci_lakes_static_lake_mask_nc_path : :class:`pathlib.Path`
        The path to the `ESA_CCI_static_lake_mask.nc` file as provided by ESA
        Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0

    esacci_lakes_merged_product_nc_paths : list[:class:`pathlib.Path`]
        Paths to some `ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.nc`
        files as provided by ESA Lakes Climate Change Initiative (Lakes_cci):
        Lake products, Version 3.0

    output_file_paths : list[:class:`pathlib.Path`]
        The output file paths

    Returns
    -------
    A list of :class:`concurrent.futures.Future`.

    Raises
    ------
    ValueError
        If `output_file_paths` and `esacci_lakes_merged_product_nc_paths` are
        not of similar length.
    """
    if len(output_file_paths) != len(esacci_lakes_merged_product_nc_paths):
        raise ValueError("expected `output_file_paths` and `esacci_lakes_merged_product_nc_paths` to be of similar length")

    futures = []

    for (
        esacci_lakes_merged_product_nc_path,
        output_file_path
    ) in zip(
        esacci_lakes_merged_product_nc_paths,
        output_file_paths
    ):
        future = get_main_py_future(
            executor,
            esacci_lakes_metadata_csv_path        = esacci_lakes_metadata_csv_path,
            esacci_lakes_static_lake_mask_nc_path = esacci_lakes_static_lake_mask_nc_path,
            esacci_lakes_merged_product_nc_path   = esacci_lakes_merged_product_nc_path,
            output_file_path                      = output_file_path
        )

        futures.append(future)

    return futures


def main_py(
    *,
    esacci_lakes_metadata_csv_path:        Path,
    esacci_lakes_static_lake_mask_nc_path: Path,
    esacci_lakes_merged_product_nc_path:   Path,
    output_file_path:                      Path
) -> CompletedProcessLog:
    """
    Runs a main.py subprocess and returns its completed process log.

    Parameters
    ----------
    esacci_lakes_metadata_csv_path : :class:`pathlib.Path`
        The path to the `lakescci_v2.1.0_metadata.csv` file as provided by ESA
        Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0

    esacci_lakes_static_lake_mask_nc_path : :class:`pathlib.Path`
        The path to the `ESA_CCI_static_lake_mask.nc` file as provided by ESA
        Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0

    esacci_lakes_merged_product_nc_path : :class:`pathlib.Path`
        The path to some
        `ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.nc` file as
        provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake
        products, Version 3.0

    output_file_path : :class:`pathlib.Path`
        The output file path

    Returns
    -------
    A :class:`lib.proc.objects.CompletedProcessLog`.
    """
    completed_process = run(
        [
            sys.executable,
            "main.py",
            str(esacci_lakes_metadata_csv_path),
            str(esacci_lakes_static_lake_mask_nc_path),
            str(esacci_lakes_merged_product_nc_path),
            "-o", str(output_file_path)
        ],
        capture_output = True,
        text           = True
    )

    return CompletedProcessLog(
        args       = completed_process.args,
        returncode = completed_process.returncode,
        stdout     = completed_process.stdout,
        stderr     = completed_process.stderr
    )


# ==================================================================================================


# Validator functions
# ==================================================================================================
def arguments_are_valid(
    args: argparse.Namespace
) -> bool:
    """
    Validates `args`.

    Parameters
    ----------
    args : :class:`argparse.Namespace`
        The arguments

    Returns
    -------
    `True` if all arguments are successfully validated. `False` otherwise.
    """
    return _arguments_are_valid(
        args,
        [
            (
                argument_esacci_lakes_metadata_csv_path_exists,
                "esacci_lakes_metadata_csv_path"
            ),
            (
                argument_esacci_lakes_static_lake_mask_nc_path_exists,
                "esacci_lakes_static_lake_mask_nc_path"
            ),
            (
                argument_esacci_lakes_merged_product_dir_path_is_dir,
                "esacci_lakes_merged_product_dir_path"
            ),
            (
                argument_output_is_dir_or_missing,
                "output"
            )
        ]
    )


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser().parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    args.output.mkdir(
        parents  = True,
        exist_ok = True
    )

    merged_product_nc_paths = get_file_paths_from_dir_by_extension(
        args.esacci_lakes_merged_product_dir_path,
        "nc"
    )
    merged_product_outputs  = get_esacci_lakes_merged_product_output_file_paths(
        args.output,
        merged_product_nc_paths
    )

    with (
        ThreadPoolExecutor(max_workers = args.workers) as executor,
        open_logstream(args.output)                    as logstream
    ):
        futures = get_main_py_futures(
            executor,
            args.esacci_lakes_metadata_csv_path,
            args.esacci_lakes_static_lake_mask_nc_path,
            merged_product_nc_paths,
            merged_product_outputs
        )

        for future in tqdm(
            as_completed(futures),
            total = len(futures)
        ):
            completed_process_log = future.result()

            write_completed_process_log_to_logstream(
                completed_process_log,
                logstream
            )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
