r"""
main_parallel.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import subprocess
import sys

from argparse           import ArgumentParser
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)
from dataclasses        import dataclass
from datetime           import datetime
from pathlib            import Path

# Related Third-party Imports
from tqdm import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.argparse import (
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_static_lake_mask_nc_path,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_static_lake_mask_nc_path_exists
)
from lib.io.vars                     import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)

PROG = "main_parallel.py"


@dataclass
class CompletedProcessLog:
    args:       list
    returncode: int
    stdout:     str
    stderr:     str


def get_date_str_from_file(
    file: Path
) -> str:
    return file.stem.split("-")[5]


def get_year_from_date_str(
    date_str: str
) -> str:
    return date_str[0:4]


def get_year_from_file(
    file: Path
) -> str:
    return get_year_from_date_str(get_date_str_from_file(file))


def get_month_from_date_str(
    date_str: str
) -> str:
    return date_str[4:6]


def get_month_from_file(
    file: Path
) -> str:
    return get_month_from_date_str(get_date_str_from_file(file))


def get_output_csv_path_from_file(
    file:            Path,
    output_dir_path: Path
) -> Path:
    date_str = get_date_str_from_file(file)
    year     = get_year_from_date_str(date_str)
    month    = get_month_from_date_str(date_str)

    return Path(output_dir_path / year / month / (file.stem + ".csv"))


def __main_py(
    esacci_lakes_metadata_csv_path:        Path,
    esacci_lakes_static_lake_mask_nc_path: Path,
    esacci_lakes_merged_product_nc_path:   Path,
    output_csv_path:                       Path
) -> CompletedProcessLog:
    completed_process = subprocess.run(
        [
            sys.executable,
            "main.py",
            str(esacci_lakes_metadata_csv_path),
            str(esacci_lakes_static_lake_mask_nc_path),
            str(esacci_lakes_merged_product_nc_path),
            str(output_csv_path)
        ],
        capture_output=True,
        text=True,
    )
    
    return CompletedProcessLog(
        args=completed_process.args,
        returncode=completed_process.returncode,
        stdout=completed_process.stdout,
        stderr=completed_process.stderr
    )


def main_py(
    esacci_lakes_metadata_csv_path:        Path,
    esacci_lakes_static_lake_mask_nc_path: Path,
    esacci_lakes_merged_product_nc_path:   Path,
    output_dir_path:                       Path
) -> CompletedProcessLog: 
    output_csv_path = get_output_csv_path_from_file(
        esacci_lakes_merged_product_nc_path,
        output_dir_path
    )
    output_csv_path.parent.mkdir(
        parents=True, 
        exist_ok=True
    )

    return __main_py(
        esacci_lakes_metadata_csv_path,
        esacci_lakes_static_lake_mask_nc_path, 
        esacci_lakes_merged_product_nc_path,
        output_csv_path
    )


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = ArgumentParser(
        prog=PROG,
        usage="%(prog)s [options]",
        description=""""""
    )

    # Positional arguments
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_static_lake_mask_nc_path(parser)
    parser.add_argument(
        "input_dir_path",
        type=Path,
        help=f""""""
    )
    parser.add_argument(
        "output_dir_path",
        type=Path,
        help=f""""""
    )
    
    # Optional arguments
    parser.add_argument(
        "--workers",
        default=8,
        type=int,
        help=f""""""
    )

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not argument_esacci_lakes_metadata_csv_path_exists(
        args.esacci_lakes_metadata_csv_path,
        loud=True
    ):
        return RETURN_FAILURE

    if not argument_esacci_lakes_static_lake_mask_nc_path_exists(
        args.esacci_lakes_static_lake_mask_nc_path,
        loud=True
    ):
        return RETURN_FAILURE

    if not args.input_dir_path.exists():
        print(
            f"""error: argument input_dir_path: no such file or directory: {args.input_dir_path}"""
        )
        
        return RETURN_FAILURE

    if not args.output_dir_path.exists():
        print(
            f"""error: argument output_dir_path: no such file or directory: {args.output_dir_path}"""
        )
        
        return RETURN_FAILURE
    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    files = list(args.input_dir_path.glob('**/*.nc'))

    timestamp     = datetime.now().strftime("%Y%m%dT%H%M%S")
    log_file_path = args.output_dir_path / f"{timestamp}.log"

    with (
        ThreadPoolExecutor(max_workers=args.workers) as executor,
        open(log_file_path, "a")                     as log_file
    ):
        futures = []

        for file in files:
            if get_output_csv_path_from_file(
                file, 
                args.output_dir_path
            ).exists():
                continue

            futures.append(
                executor.submit(
                    main_py, 
                    args.esacci_lakes_metadata_csv_path, 
                    args.esacci_lakes_static_lake_mask_nc_path, 
                    file, 
                    args.output_dir_path
                )
            )

        for future in tqdm(
            as_completed(futures),
            total=len(futures)
        ):
            result = future.result()

            log_file.write(f"{datetime.now().isoformat()}\n")
            log_file.write(f"args:       {result.args}\n")
            log_file.write(f"returncode: {result.returncode}\n")
            log_file.write(f"stdout:     {result.stdout}\n")
            log_file.write(f"stderr:     {result.stderr}\n")
            log_file.write("-" * 100 + "\n")
            log_file.flush()

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == "__main__":
    sys.exit(main())
