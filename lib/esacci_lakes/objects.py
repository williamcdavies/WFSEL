r'''
objects.py

Description: 
   Provide definitions for esacci-utility classes.

Written by William Chuter-Davies
'''


# Standard Library Imports
from dataclasses import dataclass


@dataclass
class ESACCILakesVariable():
    '''
    Object for representing an ESA CCI Lakes variable.
    '''
    var_id:    str
    long_name: str
    units:     str