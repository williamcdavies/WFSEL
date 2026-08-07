r'''
utils.py

Description: 
   Provide definitions for lakes_cci-utility variables.

Written by William Chuter-Davies
'''


LAKES_CCI_ECVS     = ['chla', 
                      'tsm', 
                      'acdom440', 
                      'Kd490', 
                      'KdPAR', 
                      'phycocyanin', 
                      'lake_surface_water_temperature', 
                      'lake_surface_water_extent']
LAKES_CCI_MEASURES = ['mean', 
                      'median', 
                      'var', 
                      'max', 
                      'min']
COUNT_OF_SMOKE_DAYS_LOWER_BOUND = 7
COUNT_OF_SMOKE_DAYS_UPPER_BOUND = 24