"""
Filename:   tests.utils.test_pandas_utils.py
Author:     William Chuter-Davies
"""

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from wfsel.utils.pandas_utils import build_mask_from_index_ser


class TestBuildMaskFromIndexSer:


    def test_marked_positions_are_one(
        self,
        index_ser: pd.Series,
    ) -> None:
        """Positions at index labels are marked with 1."""
        mask = build_mask_from_index_ser(index_ser, start = 1, stop = 366)

        assert mask.loc[1]      == 1
        assert mask.loc[100]    == 1
        assert mask.loc[365]    == 1


    def test_unmarked_positions_are_zero(
        self,
        index_ser: pd.Series,
    ) -> None:
        """Positions at non-index labels are marked with 0."""
        mask = build_mask_from_index_ser(index_ser, start = 1, stop = 366)

        assert mask.loc[101]    == 0
        assert mask.loc[102]    == 0
        assert mask.loc[103]    == 0


    def test_mask_index_runs_from_start_to_stop_minus_one(
        self,
        index_ser: pd.Series,
    ) -> None:
        """Mask index runs from [start, stop - 1]."""
        mask = build_mask_from_index_ser(index_ser, start = 1, stop = 366)

        assert mask.index[0]    == 1
        assert mask.index[-1]   == 365


    def test_empty_index_ser_produces_all_zero_mask(
        self,
        empty_index_ser: pd.Series,
    ) -> None:
        """An empty index series produces an all-zero mask."""
        mask = build_mask_from_index_ser(empty_index_ser, start = 1, stop = 366)

        assert (mask == 0).all()
