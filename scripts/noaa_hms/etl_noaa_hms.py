"""
Filename:   etl_noaa_hms.py
Author:     William Chuter-Davies
Modified:   10/11/26
"""

# Standard Library Imports
import logging
import os
import sys


from argparse   import (
                    ArgumentParser,
                    Namespace,
                )
from datetime   import date
from io         import BytesIO

# Related Third-party Imports
import geopandas as gpd
import pandas    as pd
import psycopg

from dotenv import load_dotenv

# Local Application/Library Specific Imports
from wfsel.arguments                    import add_argument_force
from wfsel.exit_codes                   import (
                                            EXIT_FAILURE,
                                            EXIT_SUCCESS,
                                        )
from wfsel.io.interfacers               import download
from wfsel.sources.noaa_hms.literals    import (
                                            NOAA_HMS_DENSITY_NAME_TO_DENSITY_VALUE,
                                            NOAA_HMS_URL_TEMPLATE,
                                        )
from wfsel.sources.noaa_hms.queries     import (
                                            query_delete_from_hms_smokes_record,
                                            query_hms_smokes_record_exists,
                                            query_insert_into_hms_smokes_record,
                                        )
from wfsel.time.arguments               import add_argument_date
from wfsel.time.literals                import DATE_FORMAT_YJ_HM
from wfsel.utils.argparse_utils         import (
                                            arguments_are_valid as _arguments_are_valid,
                                            build_parser        as _build_parser,
                                            build_subparser     as _build_subparser,
                                        )

PROG    = "etl_noaa_hms.py"
DESC    = ""

load_dotenv()
POSTGRESQL_URL = os.environ["POSTGRESQL_URL"]

logger = logging.getLogger(__name__)


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
                positional_arguments    = None,
                optional_arguments      = None,
            )

    subparsers = parser.add_subparsers(dest = "subcommand")

    _ = _build_subparser(
        subparsers,
        name                    = "inspect",
        positional_arguments    = [
                                    add_argument_date,
                                ],
        optional_arguments      = None,
    )

    _ = _build_subparser(
        subparsers,
        name                    = "ingest",
        positional_arguments    = [
                                    add_argument_date,
                                ],
        optional_arguments      = [
                                    add_argument_force,
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
    argument_name_to_validator = {}

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


# ----------------------------------------------------------------------
# builder functions
# ----------------------------------------------------------------------
def build_noaa_hms_url(
    date: date,
) -> str:
    """
    Build a NOAA HMS URL.

    Parameters
    ----------
    date : date
        The date

    Returns
    -------
    str
        A NOAA HMS URL
    """
    noaa_hms_url = date.strftime(NOAA_HMS_URL_TEMPLATE)

    return noaa_hms_url


def build_hms_smokes_gdf(
    data: bytes,
) -> gpd.GeoDataFrame:
    """
    Build a hms_smokes geodataframe.

    Parameters
    ----------
    data : bytes
        The bytes

    Returns
    -------
    gpd.GeoDataFrame
        A hms_smokes geodataframe

    Raises
    ------
    ValueError
        If the CRS of the hms_smokes geodataframe is not of EPSG:4326
    """
    gdf = gpd.read_file(BytesIO(data))

    if gdf.crs != "EPSG:4326":
        message = f"expected geodataframe to be of CRS EPSG:4326: got {gdf.crs}"

        raise ValueError(message)

    gdf = gdf.rename(
            columns = {
                        "Start":    "start_datetime",
                        "End":      "end_datetime",
                        "Density":  "density",
                        "geometry": "geom",
                    },
        )

    gdf["start_datetime"]   = pd.to_datetime(gdf["start_datetime"], format = DATE_FORMAT_YJ_HM)
    gdf["end_datetime"]     = pd.to_datetime(gdf["end_datetime"], format = DATE_FORMAT_YJ_HM)

    gdf["start_year"]   = gdf["start_datetime"].dt.year
    gdf["start_day"]    = gdf["start_datetime"].dt.day_of_year
    gdf["start_time"]   = (
                                gdf["start_datetime"].dt.hour * 100
                            +   gdf["start_datetime"].dt.minute
                        )
    gdf["end_year"]     = gdf["end_datetime"].dt.year
    gdf["end_day"]      = gdf["end_datetime"].dt.day_of_year
    gdf["end_time"]     = (
                                gdf["end_datetime"].dt.hour * 100
                            +   gdf["end_datetime"].dt.minute
                        )
    gdf["density"]      = gdf["density"].map(NOAA_HMS_DENSITY_NAME_TO_DENSITY_VALUE)

    gdf = gdf.drop(
            columns = [
                        "Satellite",
                        "start_datetime",
                        "end_datetime",
                    ],
        )

    return gdf


# ----------------------------------------------------------------------
# printer functions
# ----------------------------------------------------------------------
def print_hms_smokes_gdf(
    noaa_hms_gdf: gpd.GeoDataFrame,
) -> None:
    """
    Print a hms_smokes geodataframe.

    Parameters
    ----------
    noaa_hms_gdf : gpd.GeoDataFrame
        The hms_smokes geodataframe
    """
    print(noaa_hms_gdf) # noqa: T201


# ----------------------------------------------------------------------
# loader functions
# ----------------------------------------------------------------------
def load_hms_smokes_gdf(
    noaa_hms_gdf: gpd.GeoDataFrame,
    *,
    force: bool = False,
) -> None:
    """
    Load a hms_smokes geodataframe.

    Parameters
    ----------
    noaa_hms_gdf : gpd.GeoDataFrame
        The hms_smokes geodataframe
    force : bool, optional
        The force argument, by default False
    """
    start_year  = noaa_hms_gdf["start_year"].iloc[0]
    start_day   = noaa_hms_gdf["start_day"].iloc[0]

    with psycopg.connect(POSTGRESQL_URL) as connection:
        hms_smokes_record_exists    = query_hms_smokes_record_exists(
                                        start_year,
                                        start_day,
                                        connection,
                                    )

        if hms_smokes_record_exists and not force:
            logger.warning("Warning: Terminating transaction. A record with the same start year and day already exists. To override this warning run the program with -f/--force.")

            return

        if hms_smokes_record_exists and force:
            query_delete_from_hms_smokes_record(
                start_year,
                start_day,
                connection,
            )

        query_insert_into_hms_smokes_record(
            noaa_hms_gdf,
            connection,
        )

        connection.commit()


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

    if args.subcommand == "inspect":
        noaa_hms_url    = build_noaa_hms_url(args.date)
        data            = download(noaa_hms_url)
        noaa_hms_gdf    = build_hms_smokes_gdf(data)

        print_hms_smokes_gdf(noaa_hms_gdf)
    elif args.subcommand == "ingest":
        noaa_hms_url    = build_noaa_hms_url(args.date)
        data            = download(noaa_hms_url)
        noaa_hms_gdf    = build_hms_smokes_gdf(data)

        load_hms_smokes_gdf(noaa_hms_gdf, force = args.force)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
