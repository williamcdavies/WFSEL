"""
template.py.

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse   import (
                    ArgumentParser,
                    Namespace,
                )

# Related Third-party Imports

# Local Application/Library Specific Imports
from wfsel.exit_codes           import (
                                    EXIT_FAILURE,
                                    EXIT_SUCCESS,
                                )
from wfsel.utils.argparse_utils import (
                                    arguments_are_valid as _arguments_are_valid,
                                    build_parser        as _build_parser,
                                )

PROG    = "template.py"
DESC    = ""


# ----------------------------------------------------------------------
# setup functions
# ----------------------------------------------------------------------
def build_parser(
) -> ArgumentParser:
    """
    Wrap _build_parser.

    Returns
    -------
    ArgumentParser

    """
    parser  = ArgumentParser(
        prog        = PROG,
        description = DESC,
        usage       = "%(prog)s [options]",
    )
    parser  = _build_parser(
        parser,
        positional_arguments    = None,
        optional_arguments      = None,
    )

    return parser


def arguments_are_valid(
    arguments: Namespace,
) -> bool:
    """
    Wrap _arguments_are_valid.

    Parameters
    ----------
    arguments : Namespace
        The argument namespace

    Returns
    -------
    bool
        True if all arguments are valid, False otherwise

    """
    argument_name_to_validator = {}

    boolean = _arguments_are_valid(
        arguments,
        argument_name_to_validator,
    )

    return boolean


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main(
) -> int:
    """
    Run program.

    Returns
    -------
    int
        0 if program runs successfully, 1 otherwise

    """
    args = build_parser().parse_args()

    if not arguments_are_valid(args):
        return EXIT_FAILURE

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
