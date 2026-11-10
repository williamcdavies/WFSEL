"""
Filename:   wfsel.sources.umn_lakes.validators.py
Author:     William Chuter-Davies
"""

# Local Application/Library Specific Imports
from wfsel.sources.umn_lakes.literals import UMN_LAKES_ID_LENGTH


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

    Raises
    ------
    ValueError
        If argument is not a valid UMN Lakes id
    """
    if len(argument_value) != UMN_LAKES_ID_LENGTH:
        message = f"expected argument {argument_name} to be a valid UMN Lakes id"

        raise ValueError(message)

    return True
