"""
Filename:   wfsel.sources.esa_lakes.validators.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
import logging

# Local Application/Library Specific Imports
from wfsel.sources.esa_lakes.literals import ESA_LAKES_ID_UPPER_BOUND

logger = logging.getLogger(__name__)


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
    """
    if argument_value >= ESA_LAKES_ID_UPPER_BOUND:
        logger.error("argument %s: expected a valid ESA Lakes id: got %s", argument_name, argument_value)

        return False

    return True
