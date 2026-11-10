"""
Filename:   wfsel.literals.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from typing import Literal

type Direction  = Literal["forward", "reverse"]
type Edge       = Literal["left", "right"]
type Statistic  = Literal["mean", "std"]
