"""
Filename:   wfsel.sources.umn_lakes.validators.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
import logging

# Local Application/Library Specific Imports
from wfsel.sources.umn_lakes.literals import UMN_LAKES_ID_LENGTH

logger = logging.getLogger(__name__)


def argument_is_valid_umn_lakes_id(
    argument_name:  str,
    argument_value: str,
) -> bool:
    """
    Validate an argument as a UMN Lakes id.

    Parameters
    ----------
    argument_name : str
        The argument name
    argument_value : str
        The argument value

    Returns
    -------
    bool
        True if argument is a valid UMN Lakes id, False otherwise
    """
    if len(argument_value) != UMN_LAKES_ID_LENGTH:
        logger.error("argument %s: expected a valid UMN Lakes id: got %s", argument_name, argument_value)

        return False

    return True
