"""
Filename:   wfsel.literals.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from typing import (
                Literal,
                TypeAlias
            )

Direction:  TypeAlias   = Literal["forward", "reverse"]
Edge:       TypeAlias   = Literal["left", "right"]
Statistic:  TypeAlias   = Literal["mean", "std"]
