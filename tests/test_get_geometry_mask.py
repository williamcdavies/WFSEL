r"""
test_get_geometry_mask.py

Description: 
    The purpose of this program is to pre-compute and save, for each
    feature in the attribute table of a Shapefile, a geometry mask for
    application against netCDF files of a common coordinate reference
    system (CRS) and spatial resolution.

Written by William Chuter-Davies
"""

# Standard Library Imports
import fractions

# Related Third-party Imports
import pytest
import shapely

from lib.utils import get_geometry_mask


def test_get_geometry_mask_returns_ndarray_of_dtype_bool(sample_geometry, sample_resolution):
    geometry_mask, _ = get_geometry_mask(sample_geometry, sample_resolution)

    assert geometry_mask.dtype == bool


def test_get_geometry_mask_returns_shape_1x1_if_geometry_is_unit_square_and_resolution_is_1(sample_geometry: shapely.geometry.base.BaseGeometry):
    geometry_mask, _ = get_geometry_mask(sample_geometry, fractions.Fraction(1, 1))

    assert geometry_mask.shape == (1, 1)


def test_get_geometry_mask_returns_shape_2x2_if_geometry_is_unit_square_and_resolution_is_one_half(sample_geometry: shapely.geometry.base.BaseGeometry):
    geometry_mask, _ = get_geometry_mask(sample_geometry, fractions.Fraction(1, 2))

    assert geometry_mask.shape == (2, 2)


def test_get_geometry_mask_returns_shape_4x4_if_geometry_is_unit_square_and_resolution_is_one_fourth(sample_geometry: shapely.geometry.base.BaseGeometry):
    geometry_mask, _ = get_geometry_mask(sample_geometry, fractions.Fraction(1, 4))

    assert geometry_mask.shape == (4, 4)


def test_get_geometry_mask_returns_expected_ndarray_if_geometry_completely_overlaps_raster(sample_resolution: fractions.Fraction):
    geometry_mask, _ = get_geometry_mask(shapely.Polygon([(0, 0), 
                                                          (0, 1), 
                                                          (1, 1),
                                                          (1, 0)]),
                                         sample_resolution)

    assert geometry_mask.shape == (2, 2)
    assert geometry_mask.all()


def test_get_geometry_mask_returns_expected_ndarray_if_geometry_partially_overlaps_raster(sample_resolution: fractions.Fraction):
    geometry_mask, _ = get_geometry_mask(shapely.Polygon([(0, 0), 
                                                          (0, 1), 
                                                          (1, 1)]),
                                        sample_resolution)

    assert geometry_mask.shape == (2, 2)
    assert geometry_mask.any()
    assert not geometry_mask.all()


def test_get_geometry_mask_returns_correct_transform_if_geometry_is_unit_square_and_resolution_is_one_half(sample_geometry: shapely.geometry.base.BaseGeometry, sample_resolution: fractions.Fraction):
    _, transform = get_geometry_mask(sample_geometry, sample_resolution)

    assert transform.a ==  float(sample_resolution)
    assert transform.e == -float(sample_resolution)
    assert transform.c == sample_geometry.bounds[0]
    assert transform.f == sample_geometry.bounds[3]


def test_get_geometry_mask_raises_value_error_if_geometry_is_empty(sample_resolution):
    with pytest.raises(ValueError):
        _, _ = get_geometry_mask(shapely.Polygon(), sample_resolution)


def test_get_geometry_mask_raises_value_error_if_geometry_produces_zero_width_or_zero_height_raster(sample_resolution):
    with pytest.raises(ValueError):
        _, _ = get_geometry_mask(shapely.Polygon([(0, 0), 
                                                  (0, 1)]), 
                                 sample_resolution)


def test_get_geometry_mask_raises_value_error_if_resolution_produces_zero_width_or_zero_height_raster(sample_geometry):
    with pytest.raises(ValueError):
        _, _ = get_geometry_mask(sample_geometry, 
                                 fractions.Fraction(-1, 2))