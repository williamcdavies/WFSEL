r'''
utils.py

Description: 
   Provide definitions for lakes_cci-utility functions.

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import pathlib


def add_argument_lakes_cci_count_of_smoke_days_csv_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds a `lakes_cci_count_of_smoke_days_csv_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser
   '''
   parser.add_argument('lakes_cci_count_of_smoke_days_csv_path', 
                       type=pathlib.Path, 
                       help=f'''path to some count of smoke days data
                             csv file as produced by
                             query_lakes_cci_count_of_smoke_days.sql''')


def add_argument_lakes_cci_ecv_data_dir_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds a `lakes_cci_ecv_data_dir_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser
   '''
   parser.add_argument('lakes_cci_ecv_data_dir_path', 
                       type=pathlib.Path, 
                       help=f'''path to the Lakes ECV data directory as
                             produced by main.py''')


def add_argument_lakes_cci_merged_prod_nc_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds a `lakes_cci_merged_prod_nc_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser
   '''
   parser.add_argument('lakes_cci_merged_prod_nc_path', 
                       type=pathlib.Path, 
                       help=f'''path to some
                             `ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.nc`
                             file as provided by ESA Lakes Climate
                             Change Initiative (Lakes_cci): Lake
                             products, Version 3.0''')


def add_argument_lakes_cci_meta_data_csv_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds a `lakes_cci_meta_data_csv_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser
   '''
   parser.add_argument('lakes_cci_meta_data_csv_path',
                       type=pathlib.Path,
                        help=f'''path to the
                              `lakescci_v2.1.0_metadata.csv` file
                              provided by ESA Lakes Climate Change
                              Initiative (Lakes_cci): Lake products,
                              Version 3.0''')


def add_argument_lakes_cci_static_mask_nc_path(parser: argparse.ArgumentParser) -> None:
   '''
   Adds a `lakes_cci_static_mask_nc_path` argument to a
   :class:`argparse.ArgumentParser`.

   Parameters
   ----------
   parser : :class:`argparse.ArgumentParser`
      The parser
   '''
   parser.add_argument('lakes_cci_static_mask_nc_path', 
                       type=pathlib.Path, 
                       help=f'''path to the
                             `ESA_CCI_static_lake_mask.nc` file as
                             provided by ESA Lakes Climate Change
                             Initiative (Lakes_cci): Lake products,
                             Version 3.0''')


def argument_lakes_cci_count_of_smoke_days_csv_path_exists(lakes_cci_count_of_smoke_days_csv_path: pathlib.Path, 
                                                           *, 
                                                           loud=True) -> bool:
   '''
   Returns true if `lakes_cci_count_of_smoke_days_csv_path` exists,
   returns false otherwise.

   Parameters
   ----------
   lakes_cci_count_of_smoke_days_csv_path : :class:`pathlib.Path`
      The argument `lakes_cci_count_of_smoke_days_csv_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if lakes_cci_count_of_smoke_days_csv_path.exists():
      return True

   if loud:
      print(f'''error: argument lakes_cci_count_of_smoke_days_csv_path:
             no such file or directory:
             {lakes_cci_count_of_smoke_days_csv_path}''')

   return False


def argument_lakes_cci_ecv_data_dir_path_exists(lakes_cci_ecv_data_dir_path: pathlib.Path, 
                                                *, 
                                                loud=True) -> bool:
   '''
   Returns true if `lakes_cci_ecv_data_dir_path` exists, returns false
   otherwise.

   Parameters
   ----------
   lakes_cci_ecv_data_dir_path : :class:`pathlib.Path`
      The argument `lakes_cci_ecv_data_dir_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if lakes_cci_ecv_data_dir_path.exists():
      return True

   if loud:
      print(f'''error: argument lakes_cci_ecv_data_dir_path: no such
             file or directory: {lakes_cci_ecv_data_dir_path}''')

   return False


def argument_lakes_cci_merged_prod_nc_path_exists(lakes_cci_merged_prod_nc_path: pathlib.Path, 
                                                  *, 
                                                  loud=False) -> bool:
   '''
   Returns true if `lakes_cci_merged_prod_nc_path` exists, returns false
   otherwise.

   Parameters
   ----------
   lakes_cci_merged_prod_nc_path : :class:`pathlib.Path`
      The argument `lakes_cci_merged_prod_nc_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if lakes_cci_merged_prod_nc_path.exists():
      return True

   if loud:
      print(f'''error: argument lakes_cci_merged_prod_nc_path: no such
             file or directory: {lakes_cci_merged_prod_nc_path}''')

   return False


def argument_lakes_cci_meta_data_csv_path_exists(lakes_cci_meta_data_csv_path: pathlib.Path, 
                                                 *, 
                                                 loud=True) -> bool:
   '''
   Returns true if `lakes_cci_meta_data_csv_path` exists, returns false
   otherwise.

   Parameters
   ----------
   lakes_cci_meta_data_csv_path : :class:`pathlib.Path`
      The argument `lakes_cci_meta_data_csv_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if lakes_cci_meta_data_csv_path.exists():
      return True

   if loud:
      print(f'''error: argument lakes_cci_meta_data_csv_path: no such
             file or directory: {lakes_cci_meta_data_csv_path}''')

   return False


def argument_lakes_cci_static_mask_nc_path_exists(lakes_cci_static_mask_nc_path: pathlib.Path, 
                                                  *, 
                                                  loud=True) -> bool:
   '''
   Returns true if `lakes_cci_static_mask_nc_path` exists, returns false
   otherwise.

   Parameters
   ----------
   lakes_cci_static_mask_nc_path : :class:`pathlib.Path`
      The argument `lakes_cci_static_mask_nc_path`

   loud : bool
      If true, prints an error message to stdout. default=False
   '''
   if lakes_cci_static_mask_nc_path.exists():
      return True

   if loud:
      print(f'''error: argument lakes_cci_static_mask_nc_path: no such
             file or directory: {lakes_cci_static_mask_nc_path}''')

   return False