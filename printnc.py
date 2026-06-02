"""
printnc.py is a utility program that prints netCDF metadata to sys.stdout.

Usage: python printnc.py <file>

Written by William Chuter-Davies
"""

# Standard Imports
import sys

# Third Party Imports
from netCDF4 import Dataset

filename = sys.argv[1]
rootgrp  = Dataset(filename)

print(rootgrp)

rootgrp.close()