"""
Filename:   wfsel.sources.esa_lakes.validators.py
Author:     William Chuter-Davies
"""

# Local Application/Library Specific Imports
from wfsel.sources.esa_lakes.literals import ESA_LAKES_ID_LOWER_BOUND, ESA_LAKES_ID_UPPER_BOUND


def argument_is_valid_esa_lakes_id(
    argument_name:  str,
    argument_value: int,
) -> bool:
    """
    Validate an argument as an ESA Lakes id.

    Parameters
    ----------
    argument_name : str
        The argument name
    argument_value : int
        The argument value

    Returns
    -------
    bool
        True if argument is a valid ESA Lakes id, False otherwise

    Raises
    ------
    ValueError
        If argument is not a valid ESA Lakes id
    """
    if (
            argument_value > ESA_LAKES_ID_UPPER_BOUND
        or  argument_value < ESA_LAKES_ID_LOWER_BOUND
    ):
        message = f"expected argument {argument_name} to be a valid ESA Lakes id"

        raise ValueError(message)

    return True
