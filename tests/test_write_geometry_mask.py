r"""
test_write_geometry_mask.py

Description: 
   The purpose of this file is to test lib.utils.write_geometry_mask.

Written by William Chuter-Davies
"""


# Standard Library Imports
import datetime
import os
import pathlib

# Related Third-party Imports
import numpy
import rasterio

from lib.utils import get_geometry_mask, write_geometry_mask


def test_write_geometry_mask_output_raster_matches_input_raster(sample_geometry, 
                                                               sample_resolution) -> None:
   geometry_mask, transform = get_geometry_mask(sample_geometry, sample_resolution)
   tmp_dir                  = os.environ['TMPDIR']
   now_str                  = datetime.datetime.now().strftime(f'%y%j%H%M%S')
   path                     = pathlib.Path(tmp_dir + now_str + '.TIFF')
   
   write_geometry_mask(geometry_mask, transform, path)

   with rasterio.open(path) as ds:
      actual = ds.read(1)

   numpy.testing.assert_array_equal(actual, geometry_mask)