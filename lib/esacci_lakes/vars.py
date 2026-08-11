r'''
utils.py

Description: 
   Provide definitions for lakes_cci-utility variables.

Written by William Chuter-Davies
'''


# Local Application/Library Specific Imports
from lib.esacci_lakes.objects import ESACCILakesVariable


ESACCI_LAKES_VARIABLES          = {'chla':                           ESACCILakesVariable('chla', 
                                                                                         'Concentration of Chlorophyll-a', 
                                                                                         'mg.m-3'), 
                                   'KdPAR':                          ESACCILakesVariable('KdPAR', 
                                                                                         'Vertical Diffuse Downwelling Attenuation Coefficient Aggregated Over PAR', 
                                                                                         'm-1'), 
                                   'lake_surface_water_temperature': ESACCILakesVariable('lake_surface_water_temperature', 
                                                                                         'Lake Surface Skin Temperature', 
                                                                                         'kelvin')}

COUNT_OF_SMOKE_DAYS_LOWER_BOUND = 7
COUNT_OF_SMOKE_DAYS_UPPER_BOUND = 24