"""
wfsel.core.argparse_utils.

Written by William Chuter-Davies
"""

# Standard Library Imports
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from argparse        import (
        ArgumentParser,
        Namespace,
    )
    from collections.abc import Callable
    from pathlib         import Path


# ----------------------------------------------------------------------
# setup functions
# ----------------------------------------------------------------------
def build_parser(
    parser: ArgumentParser,
    *,
    positional_arguments: list[Callable[[ArgumentParser], None]] | None = None,
    optional_arguments:   list[Callable[[ArgumentParser], None]] | None = None,
) -> ArgumentParser:
    """
    Build a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    positional_arguments : list[Callable[[ArgumentParser], None]] | None, optional
        The list of positional argument adder functions, by default None
    optional_arguments : list[Callable[[ArgumentParser], None]] | None, optional
        The list of optional argument adder functions, by default None

    Returns
    -------
    ArgumentParser
    """
    for f in (
        *(positional_arguments or []), # if None, unpack empty list
        *(optional_arguments   or []),  # if None, unpack empty list
    ):
        f(parser)

    return parser


def arguments_are_valid(
    arguments:                  Namespace,
    argument_name_to_validator: dict[str, Callable[[str, Any], bool]],
) -> bool:
    """
    Validate a list of arguments.

    Parameters
    ----------
    arguments : Namespace
        The arguments
    argument_name_to_validator : dict[str, Callable[[Any], bool]]
        The mapping of argument names to validators

    Returns
    -------
    bool
    """
    for (
        argument_name,
        validator,
    ) in argument_name_to_validator.items():
        argument_value = getattr(
            arguments,
            argument_name,
        )

        if not validator(
            argument_name,
            argument_value,
        ):
            return False

    return True


# ----------------------------------------------------------------------
# validation functions
# ----------------------------------------------------------------------
def argument_is_directory(
    argument_name:  str,
    argument_value: Path,
) -> bool:
    """
    Validate an argument as a directory.

    Parameters
    ----------
    argument_name : str
        The argument name
    argument_value : Path
        The argument value

    Returns
    -------
    bool
    """
    boolean = argument_value.is_dir()

    if not boolean:
        message = f"expected argument {argument_name} to be a directory"

        raise ValueError(message)

    return boolean


def argument_is_file(
    argument_name:  str,
    argument_value: Path,
) -> bool:
    """
    Validate an argument as a file.

    Parameters
    ----------
    argument_name : str
        The argument name
    argument_value : Path
        The argument value

    Returns
    -------
    bool
    """
    boolean = argument_value.is_file()

    if not boolean:
        message = f"expected argument {argument_name} to be a file"

        raise ValueError(message)

    return boolean


def argument_is_in_set(
    value_set: list[str],
) -> Callable[[str, str], bool]:
    """
    Validate an argument as belonging to a value set.

    Parameters
    ----------
    value_set : list[str]
        The value set

    Returns
    -------
    Callable[[str, str], bool]
    """
    def _validator(
        argument_name:  str,
        argument_value: str,
    ) -> bool:
        boolean = argument_value in value_set

        if not boolean:
            message = f"expected argument {argument_name} to be in {value_set}"

            raise ValueError(message)

        return boolean

    return _validator
