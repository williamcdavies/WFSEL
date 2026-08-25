r'''
utils.py

Description: 
   Provide definitions for esacci-utility functions.

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import pathlib

# Local Application/Library Specific Imports
from lib.esacci_lakes.vars import ESACCI_LAKES_VARIABLES


# Argument functions (main.py)
# ==================================================================================================
def add_argument_esacci_lakes_data_dir_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds an `esacci_lakes_data_dir_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser

   Notes
   -----
   Argument `esacci_lakes_data_dir_path` is of type
   :class:`pathlib.Path`
   '''
   parser.add_argument('esacci_lakes_data_dir_path', 
                       type=pathlib.Path, 
                       help=f'''path to the ESA CCI Lakes data directory as produced by main.py''')


def argument_esacci_lakes_data_dir_path_exists(esacci_lakes_data_dir_path: pathlib.Path, 
                                               *, 
                                               loud: bool=False) -> bool:
   '''
   Returns true if `esacci_lakes_data_dir_path` exists, returns false
   otherwise.

   Parameters
   ----------
   esacci_lakes_data_dir_path : :class:`pathlib.Path`
      The argument `esacci_lakes_data_dir_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if esacci_lakes_data_dir_path.exists():
      return True

   if loud:
      print(f'''error: argument esacci_lakes_data_dir_path: no such file or directory: {esacci_lakes_data_dir_path}''')

   return False
# ==================================================================================================


# Argument functions (SQL)
# ==================================================================================================
def add_argument_esacci_lakes_average_depths_csv_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds an `esacci_lakes_average_depths_csv_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser

   Notes
   -----
   Argument `esacci_lakes_average_depths_csv_path` is of type
   :class:`pathlib.Path`
   '''
   parser.add_argument('esacci_lakes_average_depths_csv_path', 
                       type=pathlib.Path, 
                       help=f'''path to some average depths data csv file as produced by query_esacci_lakes_average_depths.sql''')


def argument_esacci_lakes_average_depths_csv_path_exists(esacci_lakes_average_depths_csv_path: pathlib.Path, 
                                                         *, 
                                                         loud: bool=False) -> bool:
   '''
   Returns true if `esacci_lakes_average_depths_csv_path` exists,
   returns false otherwise.

   Parameters
   ----------
   esacci_lakes_average_depths_csv_path : :class:`pathlib.Path`
      The argument `esacci_lakes_average_depths_csv_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if esacci_lakes_average_depths_csv_path.exists():
      return True

   if loud:
      print(f'''error: argument esacci_lakes_average_depths_csv_path: no such file or directory: {esacci_lakes_average_depths_csv_path}''')

   return False


def add_argument_esacci_lakes_counts_of_smoke_days_csv_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds an `esacci_lakes_counts_of_smoke_days_csv_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser

   Notes
   -----
   Argument `esacci_lakes_counts_of_smoke_days_csv_path` is of type
   :class:`pathlib.Path`
   '''
   parser.add_argument('esacci_lakes_counts_of_smoke_days_csv_path', 
                       type=pathlib.Path, 
                       help=f'''path to some counts of smoke days data csv file as produced by query_esacci_lakes_counts_of_smoke_days.sql''')


def argument_esacci_lakes_counts_of_smoke_days_csv_path_exists(esacci_lakes_counts_of_smoke_days_csv_path: pathlib.Path, 
                                                               *, 
                                                               loud: bool=False) -> bool:
   '''
   Returns true if `esacci_lakes_counts_of_smoke_days_csv_path` exists,
   returns false otherwise.

   Parameters
   ----------
   esacci_lakes_counts_of_smoke_days_csv_path : :class:`pathlib.Path`
      The argument `esacci_lakes_counts_of_smoke_days_csv_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if esacci_lakes_counts_of_smoke_days_csv_path.exists():
      return True

   if loud:
      print(f'''error: argument esacci_lakes_counts_of_smoke_days_csv_path: no such file or directory: {esacci_lakes_counts_of_smoke_days_csv_path}''')

   return False


def add_argument_esacci_lakes_hydro_lakes_ids_csv_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds an `esacci_lakes_hydro_lakes_ids_csv_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser

   Notes
   -----
   Argument `esacci_lakes_hydro_lakes_ids_csv_path` is of type
   :class:`pathlib.Path`
   '''
   parser.add_argument('esacci_lakes_hydro_lakes_ids_csv_path', 
                       type=pathlib.Path, 
                       help=f'''path to some hydro lakes ids data csv file as produced by query_esacci_lakes_hydro_lakes_ids.sql''')


def argument_esacci_lakes_hydro_lakes_ids_csv_path_exists(esacci_lakes_hydro_lakes_ids_csv_path: pathlib.Path, 
                                                          *, 
                                                          loud: bool=False) -> bool:
   '''
   Returns true if `esacci_lakes_hydro_lakes_ids_csv_path` exists,
   returns false otherwise.

   Parameters
   ----------
   esacci_lakes_hydro_lakes_ids_csv_path : :class:`pathlib.Path`
      The argument `esacci_lakes_hydro_lakes_ids_csv_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if esacci_lakes_hydro_lakes_ids_csv_path.exists():
      return True

   if loud:
      print(f'''error: argument esacci_lakes_hydro_lakes_ids_csv_path: no such file or directory: {esacci_lakes_hydro_lakes_ids_csv_path}''')

   return False


def add_argument_esacci_lakes_smoke_days_csv_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds an `esacci_lakes_smoke_days_csv_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser

   Notes
   -----
   Argument `esacci_lakes_smoke_days_csv_path` is of type
   :class:`pathlib.Path`
   '''
   parser.add_argument('esacci_lakes_smoke_days_csv_path', 
                       type=pathlib.Path, 
                       help=f'''path to some smoke days data csv file as produced by query_esacci_lakes_smoke_days.sql''')


def argument_esacci_lakes_smoke_days_csv_path_exists(esacci_lakes_smoke_days_csv_path: pathlib.Path, 
                                                     *, 
                                                     loud: bool=False) -> bool:
   '''
   Returns true if `esacci_lakes_smoke_days_csv_path` exists, returns
   false otherwise.

   Parameters
   ----------
   esacci_lakes_smoke_days_csv_path : :class:`pathlib.Path`
      The argument `esacci_lakes_smoke_days_csv_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if esacci_lakes_smoke_days_csv_path.exists():
      return True

   if loud:
      print(f'''error: argument esacci_lakes_smoke_days_csv_path: no such file or directory: {esacci_lakes_smoke_days_csv_path}''')

   return False
# ==================================================================================================


# Argument functions (ESA CCI Lakes)
# ==================================================================================================
def add_argument_esacci_lakes_id(parser: argparse.ArgumentParser) -> None:
   '''
   Adds an `esacci_lakes_id` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser

   Notes
   -----
   Argument `esacci_lakes_id` is of type int
   '''
   parser.add_argument('esacci_lakes_id', 
                       type=int, 
                       help=f'''lake_cci_id as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0''')


def add_argument_esacci_lakes_merged_product_dir_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds an `esacci_lakes_merged_product_dir_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser

   Notes
   -----
   Argument `esacci_lakes_merged_product_dir_path` is of type
   :class:`pathlib.Path`
   '''
   parser.add_argument('esacci_lakes_merged_product_dir_path', 
                       type=pathlib.Path, 
                       help=f'''path to the ESA CCI merged_product directory as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0''')


def argument_esacci_lakes_merged_product_dir_path_exists(esacci_lakes_merged_product_dir_path: pathlib.Path, 
                                                         *, 
                                                         loud: bool=False) -> bool:
   '''
   Returns true if `esacci_lakes_merged_product_dir_path` exists,
   returns false otherwise.

   Parameters
   ----------
   esacci_lakes_merged_product_dir_path : :class:`pathlib.Path`
      The argument `esacci_lakes_merged_product_dir_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if esacci_lakes_merged_product_dir_path.exists():
      return True

   if loud:
      print(f'''error: argument esacci_lakes_merged_product_dir_path: no such file or directory: {esacci_lakes_merged_product_dir_path}''')

   return False


def add_argument_esacci_lakes_metadata_csv_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds an `esacci_lakes_metadata_csv_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser

   Notes
   -----
   Argument `esacci_lakes_metadata_csv_path` is of type
   :class:`pathlib.Path`
   '''
   parser.add_argument('esacci_lakes_metadata_csv_path',
                       type=pathlib.Path,
                       help=f'''path to the `lakescci_v2.1.0_metadata.csv` file as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0''')


def argument_esacci_lakes_metadata_csv_path_exists(esacci_lakes_metadata_csv_path: pathlib.Path, 
                                                   *, 
                                                   loud: bool=False) -> bool:
   '''
   Returns true if `esacci_lakes_metadata_csv_path` exists, returns
   false otherwise.

   Parameters
   ----------
   esacci_lakes_metadata_csv_path : :class:`pathlib.Path`
      The argument `esacci_lakes_metadata_csv_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if esacci_lakes_metadata_csv_path.exists():
      return True

   if loud:
      print(f'''error: argument esacci_lakes_metadata_csv_path: no such file or directory: {esacci_lakes_metadata_csv_path}''')

   return False


def add_argument_esacci_lakes_products_merged_nc_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds an `esacci_lakes_products_merged_nc_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser

   Notes
   -----
   Argument `esacci_lakes_products_merged_nc_path` is of type
   :class:`pathlib.Path`
   '''
   parser.add_argument('esacci_lakes_products_merged_nc_path', 
                       type=pathlib.Path, 
                       help=f'''path to some `ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.nc` file as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0''')


def argument_esacci_lakes_products_merged_nc_path_exists(esacci_lakes_products_merged_nc_path: pathlib.Path, 
                                                         *, 
                                                         loud: bool=False) -> bool:
   '''
   Returns true if `esacci_lakes_products_merged_nc_path` exists,
   returns false otherwise.

   Parameters
   ----------
   esacci_lakes_products_merged_nc_path : :class:`pathlib.Path`
      The argument `esacci_lakes_products_merged_nc_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if esacci_lakes_products_merged_nc_path.exists():
      return True

   if loud:
      print(f'''error: argument esacci_lakes_products_merged_nc_path: no such file or directory: {esacci_lakes_products_merged_nc_path}''')

   return False


def add_argument_esacci_lakes_static_lake_mask_nc_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds an `esacci_lakes_static_lake_mask_nc_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser

   Notes
   -----
   Argument `esacci_lakes_static_lake_mask_nc_path` is of type
   :class:`pathlib.Path` 
   '''
   parser.add_argument('esacci_lakes_static_lake_mask_nc_path', 
                       type=pathlib.Path, 
                       help=f'''path to the `ESA_CCI_static_lake_mask.nc` file as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0''')


def argument_esacci_lakes_static_lake_mask_nc_path_exists(esacci_lakes_static_lake_mask_nc_path: pathlib.Path, 
                                                          *, 
                                                          loud: bool=False) -> bool:
   '''
   Returns true if `esacci_lakes_static_lake_mask_nc_path` exists,
   returns false otherwise.

   Parameters
   ----------
   esacci_lakes_static_lake_mask_nc_path : :class:`pathlib.Path`
      The argument `esacci_lakes_static_lake_mask_nc_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if esacci_lakes_static_lake_mask_nc_path.exists():
      return True

   if loud:
      print(f'''error: argument esacci_lakes_static_lake_mask_nc_path: no such file or directory: {esacci_lakes_static_lake_mask_nc_path}''')

   return False


def add_argument_esacci_lakes_variable(parser: argparse.ArgumentParser) -> None:
   '''
   Adds an `esacci_lakes_variable` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser

   Notes
   -----
   Argument `esacci_lakes_variable` is of type str
   '''
   parser.add_argument('esacci_lakes_variable', 
                       type=str, 
                       help=f'''one of {ESACCI_LAKES_VARIABLES}''')


def argument_esacci_lakes_variable_is_in_esacci_lakes_variables(esacci_lakes_variable: str, 
                                                                *, 
                                                                loud: bool=False) -> bool:
   '''
   Returns true if `esacci_lakes_variable` is one of ['chla', 'tsm',
   'acdom440', 'Kd490', 'KdPAR', 'phycocyanin',
   'lake_surface_water_temperature', 'lake_surface_water_extent'],
   returns false otherwise.

   Parameters
   ----------
   esacci_lakes_variable : str
      The argument `esacci_lakes_variable`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if esacci_lakes_variable in ESACCI_LAKES_VARIABLES:
      return True

   if loud:
      print(f'''error: argument esacci_lakes_variable: not one of {list(ESACCI_LAKES_VARIABLES.keys())}: {esacci_lakes_variable}''')

   return False
# ==================================================================================================