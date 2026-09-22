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
from datetime           import datetime
from pathlib            import Path
from subprocess         import run
from typing             import TextIO

# Related Third-party Imports
from tqdm import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.proc import (
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_static_lake_mask_nc_path,
    add_argument_esacci_lakes_merged_product_dir_path,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_static_lake_mask_nc_path_exists,
    argument_esacci_lakes_merged_product_dir_path_exists,
    get_esacci_lakes_merged_product_nc_paths
)
from lib.proc.objects             import CompletedProcessLog
from lib.proc.utils               import (
    add_argument_output,
    argument_output_is_a_directory,
    open_logstream
)
from lib.proc.vars                import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)
from lib.time.utils               import (
    get_year_from_datetime,
    get_month_from_datetime
)

PROG = "main_parallel.py"


# Argument functions
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
    None

    Notes
    -----
    Argument `workers` is of type :class:`int`. default=8.
    """
    parser.add_argument(
        "--workers",
        type    = int,
        default = 8,
        help    = """number of worker threads"""
    )


def build_parser(
    prog: str
) -> argparse.ArgumentParser:
    """
    Builds a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    prog : :class:`str`
        The program name

    Returns
    -------
    A :class:`argparse.ArgumentParser`.
    """
    parser = argparse.ArgumentParser(
        prog        = prog,
        usage       = "%(prog)s [options]",
        description = """Runs `main.py` in parallel."""
    )

    # Positional arguments
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_static_lake_mask_nc_path(parser)
    add_argument_esacci_lakes_merged_product_dir_path(parser)
    add_argument_workers(parser)

    # Optional arguments
    add_argument_output(parser)

    return parser


def arguments_are_valid(
    args: argparse.Namespace
) -> bool:
    """
    Validates `args`.

    Returns
    -------
    `True` if all arguments are successfully validated. `False`
    otherwise.
    """
    if not argument_esacci_lakes_metadata_csv_path_exists(
        args.esacci_lakes_metadata_csv_path,
        loud = True
    ):
        return False

    if not argument_esacci_lakes_static_lake_mask_nc_path_exists(
        args.esacci_lakes_static_lake_mask_nc_path,
        loud = True
    ):
        return False

    if not argument_esacci_lakes_merged_product_dir_path_exists(
        args.esacci_lakes_merged_product_dir_path,
        loud = True
    ):
        return False

    if not argument_output_is_a_directory(
        args.output,
        loud = True
    ):
        return False

    return True


# ==================================================================================================
def get_esacci_lakes_merged_product_time(
    esacci_lakes_merged_product_nc_path: Path
) -> datetime:
    """
    Returns the time for `esacci_lakes_merged_product_nc_path` as a
    :class:`datetime.datetime`.

    Parameters
    ----------
    esacci_lakes_merged_product_nc_path : :class:`pathlib.Path`
        The path to some ESA CCI Lakes merged product netCDF file

    Returns
    -------
    A :class:`datetime.datetime`.
    """
    date_string = esacci_lakes_merged_product_nc_path.stem.split("-")[5]

    return datetime.strptime(
        date_string,
        "%Y%m%d"
    )


def get_esacci_lakes_merged_product_output_path(
    output:                               Path,
    esacci_lakes_merged_product_nc_path: Path
) -> Path:
    """
    Returns the output file path for
    `esacci_lakes_merged_product_nc_path`.

    Parameters
    ----------
    output : :class:`pathlib.Path`
        The output directory path

    esacci_lakes_merged_product_nc_path : :class:`pathlib.Path`
        The path to some ESA CCI Lakes merged product netCDF file

    Returns
    -------
    A :class:`pathlib.Path`.
    """
    time  = get_esacci_lakes_merged_product_time(esacci_lakes_merged_product_nc_path)
    year  = get_year_from_datetime(time)
    month = get_month_from_datetime(time)
    stem  = esacci_lakes_merged_product_nc_path.stem

    return output / year / month / f"{stem}.csv"


def get_esacci_lakes_merged_product_output_paths(
    output:                               Path,
    esacci_lakes_merged_product_nc_paths: list[Path]
) -> list[Path]:
    """
    Returns the output file paths for
    `esacci_lakes_merged_product_nc_paths`.

    Parameters
    ----------
    output : :class:`pathlib.Path`
        The output directory path

    esacci_lakes_merged_product_nc_paths : list[:class:`pathlib.Path`]
        Paths to some ESA CCI Lakes merged product netCDF files

    Returns
    -------
    A list of :class:`pathlib.Path`.
    """
    return [
        get_esacci_lakes_merged_product_output_path(
            output,
            esacci_lakes_merged_product_nc_path
        )
        for esacci_lakes_merged_product_nc_path
        in esacci_lakes_merged_product_nc_paths
    ]


def main_py(
    esacci_lakes_metadata_csv_path:        Path,
    esacci_lakes_static_lake_mask_nc_path: Path,
    esacci_lakes_merged_product_nc_path:   Path,
    output:                                Path
) -> CompletedProcessLog:
    """
    Runs a main.py subprocess and returns the completed process log.

    Parameters
    ----------
    esacci_lakes_metadata_csv_path : :class:`pathlib.Path`
        The path to the `lakescci_v2.1.0_metadata.csv` file as provided
        by ESA Lakes Climate Change Initiative (Lakes_cci): Lake
        products, Version 3.0

    esacci_lakes_static_lake_mask_nc_path : :class:`pathlib.Path`
        The path to the `ESA_CCI_static_lake_mask.nc` file as provided
        by ESA Lakes Climate Change Initiative (Lakes_cci): Lake
        products, Version 3.0

    esacci_lakes_merged_product_nc_path : :class:`pathlib.Path`
        The path to some
        `ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.nc` file
        as provided by ESA Lakes Climate Change Initiative (Lakes_cci):
        Lake products, Version 3.0

    output : :class:`pathlib.Path`
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
            "-o", str(output)
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


def get_main_py_future(
    executor: ThreadPoolExecutor,
    *,
    esacci_lakes_metadata_csv_path:        Path,
    esacci_lakes_static_lake_mask_nc_path: Path,
    esacci_lakes_merged_product_nc_path:   Path,
    output:                                Path
) -> Future:
    """
    Submits a main.py subprocess and returns its future.

    Parameters
    ----------
    executor : :class:`concurrent.futures.ThreadPoolExecutor`
        The executor to submit to

    esacci_lakes_metadata_csv_path : :class:`pathlib.Path`
        The path to the `lakescci_v2.1.0_metadata.csv` file as provided
        by ESA Lakes Climate Change Initiative (Lakes_cci): Lake
        products, Version 3.0

    esacci_lakes_static_lake_mask_nc_path : :class:`pathlib.Path`
        The path to the `ESA_CCI_static_lake_mask.nc` file as provided
        by ESA Lakes Climate Change Initiative (Lakes_cci): Lake
        products, Version 3.0

    esacci_lakes_merged_product_nc_path : :class:`pathlib.Path`
        The path to some
        `ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.nc` file
        as provided by ESA Lakes Climate Change Initiative (Lakes_cci):
        Lake products, Version 3.0

    output : :class:`pathlib.Path`
        The output file path

    Returns
    -------
    A :class:`concurrent.futures.Future`.
    """
    return executor.submit(
        main_py,
        esacci_lakes_metadata_csv_path,
        esacci_lakes_static_lake_mask_nc_path,
        esacci_lakes_merged_product_nc_path,
        output
    )


def get_main_py_futures(
    executor: ThreadPoolExecutor,
    *,
    esacci_lakes_metadata_csv_path:        Path,
    esacci_lakes_static_lake_mask_nc_path: Path,
    esacci_lakes_merged_product_nc_paths:  list[Path],
    outputs:                               list[Path]
) -> list[Future]:
    """
    Submits a main.py subprocess for each of
    `esacci_lakes_merged_product_nc_paths`.

    Parameters
    ----------
    executor : :class:`concurrent.futures.ThreadPoolExecutor`
        The executor to submit to

    esacci_lakes_metadata_csv_path : :class:`pathlib.Path`
        The path to the `lakescci_v2.1.0_metadata.csv` file as provided
        by ESA Lakes Climate Change Initiative (Lakes_cci): Lake
        products, Version 3.0

    esacci_lakes_static_lake_mask_nc_path : :class:`pathlib.Path`
        The path to the `ESA_CCI_static_lake_mask.nc` file as provided
        by ESA Lakes Climate Change Initiative (Lakes_cci): Lake
        products, Version 3.0

    esacci_lakes_merged_product_nc_paths : list[:class:`pathlib.Path`]
        Paths to some
        `ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.nc` files
        as provided by ESA Lakes Climate Change Initiative (Lakes_cci):
        Lake products, Version 3.0

    outputs : list[:class:`pathlib.Path`]
        The output file paths

    Returns
    -------
    A list of :class:`concurrent.futures.Future`.

    Raises
    ------
    ValueError
        If `outputs` and `esacci_lakes_merged_product_nc_paths` are not
        of similar length.
    """
    if len(outputs) != len(esacci_lakes_merged_product_nc_paths):
        raise ValueError("expected `outputs` and `esacci_lakes_merged_product_nc_paths` to be of similar length")

    futures = []

    for (
        esacci_lakes_merged_product_nc_path,
        output
    ) in zip(
        esacci_lakes_merged_product_nc_paths,
        outputs
    ):
        future = get_main_py_future(
            executor,
            esacci_lakes_metadata_csv_path        = esacci_lakes_metadata_csv_path,
            esacci_lakes_static_lake_mask_nc_path = esacci_lakes_static_lake_mask_nc_path,
            esacci_lakes_merged_product_nc_path   = esacci_lakes_merged_product_nc_path,
            output                                = output
        )

        futures.append(future)

    return futures


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


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    args.output.mkdir(
        parents  = True,
        exist_ok = True
    )

    merged_product_nc_paths = get_esacci_lakes_merged_product_nc_paths(args.esacci_lakes_merged_product_dir_path)
    merged_product_outputs  = get_esacci_lakes_merged_product_output_paths(
        args.output,
        merged_product_nc_paths
    )

    with (
        ThreadPoolExecutor(max_workers = args.workers) as executor,
        open_logstream(args.output)                    as logstream
    ):
        futures = get_main_py_futures(
            executor,
            esacci_lakes_metadata_csv_path        = args.esacci_lakes_metadata_csv_path,
            esacci_lakes_static_lake_mask_nc_path = args.esacci_lakes_static_lake_mask_nc_path,
            esacci_lakes_merged_product_nc_paths  = merged_product_nc_paths,
            outputs                               = merged_product_outputs
        )

        for future in tqdm(
            as_completed(futures),
            total = len(futures)
        ):
            completed_process_log = future.result()

            write_completed_process_log_to_logstream(
                completed_process_log,
                logstream = logstream
            )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
