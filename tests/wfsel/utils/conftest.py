"""
Filename:   tests.utils.conftest.py
Author:     William Chuter-Davies
"""

# Related Third-party Imports
import pandas as pd
import pytest


@pytest.fixture
def index_ser() -> pd.Series:
    """An index series."""
    return pd.Series([1, 100, 365])


@pytest.fixture
def empty_index_ser() -> pd.Series:
    """An empty index series."""
    return pd.Series([], dtype = int)
