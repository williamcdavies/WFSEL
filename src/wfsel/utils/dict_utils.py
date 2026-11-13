"""
Filename:   wfsel.utils.dict_utils.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from typing import Any


def keys_are_similar(
    *dicts: dict[Any, Any],
) -> bool:
    """
    Validate the key set similarity of dictionaries.

    Returns
    -------
    bool
        True if all keys sets are similar, False otherwise
    """
    frozensets  = [
                    frozenset(d.keys())
                    for d
                    in dicts
                ]

    if len(set(frozensets)) == 1:
        return True

    return False
