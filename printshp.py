"""
printshp.py is a utility program that prints Shapefile metadata to sys.stdout.

Usage: python printshp.py <file>

Written by William Chuter-Davies
"""

# Standard Imports
import sys

# Third Party Imports
import shapefile

filename = sys.argv[1]
sf       = shapefile.Reader(filename)

print(sf)