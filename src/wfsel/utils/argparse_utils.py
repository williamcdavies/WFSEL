"""
Filename:   wfsel.utils.argparse_utils.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""

# Standard Library Imports
from argparse           import (
                            ArgumentParser,
                            Namespace,
                        )
from collections.abc    import Callable
from pathlib            import Path
from typing             import Any


def build_parser(
    parser: ArgumentParser,
    *,
    positional_arguments:   list[Callable[[ArgumentParser], None]] | None = None,
    optional_arguments:     list[Callable[[ArgumentParser], None]] | None = None,
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
        A parser
    """
    for f in (
        *(positional_arguments or []),  # if None, unpack empty list
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
    argument_name_to_validator : dict[str, Callable[[str, Any], bool]]
        The mapping of argument names to validators

    Returns
    -------
    bool
        True if all arguments are valid, False otherwise
    """
    for (
        argument_name,
        validator,
    ) in argument_name_to_validator.items():
        argument_value  = getattr(
                            arguments,
                            argument_name,
                        )

        if not validator(
            argument_name,
            argument_value,
        ):
            return False

    return True


def argument_is_dir(
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
        True if argument is a directory, False otherwise
    """
    if not argument_value.is_dir():
        message = f"expected argument {argument_name} to be a directory"

        raise ValueError(message)

    return True


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
        True if argument is a file, False otherwise
    """
    if not argument_value.is_file():
        message = f"expected argument {argument_name} to be a file"

        raise ValueError(message)

    return True
