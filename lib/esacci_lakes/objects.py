r'''
objects.py

Description: 
   Provide definitions for esacci-utility classes.

Written by William Chuter-Davies
'''


class ESACCILakesVariable():
    '''
    Object for representing an ESA CCI Lakes variable.
    '''
    def __init__(self, 
                 var_id:    str, 
                 long_name: str, 
                 units:     str):
        self.var_id    = var_id
        self.long_name = long_name
        self.units     = units