# Standard Library Imports
import fractions

# Related Third-party Imports
import pytest
import shapely


@pytest.fixture
def sample_geometry():
    return shapely.Polygon([(0, 0), 
                            (1, 0), 
                            (1, 1), 
                            (0, 1)])


@pytest.fixture
def sample_resolution():
    return fractions.Fraction(1, 
                              2)