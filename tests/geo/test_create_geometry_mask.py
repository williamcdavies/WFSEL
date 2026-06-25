r"""
test_create_geometry_mask.py

Description: 
   The purpose of this file is to test lib.utils.create_geometry_mask.

Written by William Chuter-Davies
"""


# Standard Library Imports
import fractions

# Related Third-party Imports
import pytest
import numpy
import shapely

# Local Application/Library Specific Imports
from lib.geo.utils import create_geometry_mask


def test_create_geometry_mask_returns_ndarray_of_dtype_bool(sample_geometry, 
                                                            sample_resolution) -> None:
    geometry_mask, _ = create_geometry_mask(sample_geometry, 
                                            sample_resolution)

    assert geometry_mask.dtype == bool


def test_create_geometry_mask_returns_shape_1x1_if_geometry_is_unit_square_and_resolution_is_1(sample_geometry: shapely.geometry.base.BaseGeometry) -> None:
    geometry_mask, _ = create_geometry_mask(sample_geometry, 
                                            fractions.Fraction(1, 
                                                               1))

    assert geometry_mask.shape == (1, 1)


def test_create_geometry_mask_returns_shape_2x2_if_geometry_is_unit_square_and_resolution_is_one_half(sample_geometry: shapely.geometry.base.BaseGeometry) -> None:
    geometry_mask, _ = create_geometry_mask(sample_geometry, fractions.Fraction(1, 
                                                                                2))

    assert geometry_mask.shape == (2, 2)


def test_create_geometry_mask_returns_shape_4x4_if_geometry_is_unit_square_and_resolution_is_one_fourth(sample_geometry: shapely.geometry.base.BaseGeometry) -> None:
    geometry_mask, _ = create_geometry_mask(sample_geometry, fractions.Fraction(1, 
                                                                                4))

    assert geometry_mask.shape == (4, 4)


def test_create_geometry_mask_returns_expected_ndarray_if_geometry_completely_overlaps_raster(sample_resolution: fractions.Fraction) -> None:
    geometry_mask, _ = create_geometry_mask(shapely.Polygon([(0, 0), 
                                                            (0, 1), 
                                                            (1, 1),
                                                            (1, 0)]),
                                            sample_resolution)

    numpy.testing.assert_array_equal(geometry_mask, 
                                     numpy.array([(True, True), 
                                                  (True, True)]))


def test_create_geometry_mask_returns_expected_ndarray_if_geometry_partially_overlaps_raster(sample_resolution: fractions.Fraction) -> None:
    geometry_mask, _ = create_geometry_mask(shapely.Polygon([(0, 0), 
                                                            (0, 1), 
                                                            (1, 1)]),
                                            sample_resolution)

    numpy.testing.assert_array_equal(geometry_mask, 
                                     numpy.array([(True, True), 
                                                  (True, False)]))


def test_create_geometry_mask_returns_correct_transform_if_geometry_is_unit_square_and_resolution_is_one_half(sample_geometry: shapely.geometry.base.BaseGeometry, 
                                                                                                           sample_resolution: fractions.Fraction) -> None:
    _, transform = create_geometry_mask(sample_geometry, 
                                        sample_resolution)

    assert transform.a ==  float(sample_resolution)
    assert transform.e == -float(sample_resolution)
    assert transform.c == sample_geometry.bounds[0]
    assert transform.f == sample_geometry.bounds[3]


def test_create_geometry_mask_raises_value_error_if_geometry_is_empty(sample_resolution) -> None:
    with pytest.raises(ValueError):
        _, _ = create_geometry_mask(shapely.Polygon(), 
                                    sample_resolution)


def test_create_geometry_mask_raises_value_error_if_resolution_is_zero(sample_geometry) -> None:
    with pytest.raises(ValueError):
        _, _ = create_geometry_mask(sample_geometry, 
                                    fractions.Fraction(0, 
                                                       1))


def test_create_geometry_mask_raises_value_error_if_geometry_produces_zero_width_or_zero_height_raster(sample_resolution) -> None:
    with pytest.raises(ValueError):
        _, _ = create_geometry_mask(shapely.Polygon([(0, 0), 
                                                    (0, 1)]), 
                                    sample_resolution)


def test_create_geometry_mask_raises_value_error_if_resolution_produces_zero_width_or_zero_height_raster(sample_geometry) -> None:
    with pytest.raises(ValueError):
        _, _ = create_geometry_mask(sample_geometry, 
                                    fractions.Fraction(-1, 
                                                       2))