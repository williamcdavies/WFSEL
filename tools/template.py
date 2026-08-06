# Standard Library Imports
import argparse
import sys

# Related Third-party Imports

# Local Application/Library Specific Imports
from lib.io.vars import (RETURN_FAILURE, 
                         RETURN_SUCCESS)


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog='_.py', 
                                     usage='%(prog)s [options]', 
                                     description='''Templated .py file.
                                                 Includes sections for
                                                 argument parsing,
                                                 argument validation,
                                                 and program logic.''')

    # Positional arguments
    
    # Optional arguments

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================

    return RETURN_SUCCESS
    # ==================================================================================================
    

if __name__ == '__main__':
   sys.exit(main())