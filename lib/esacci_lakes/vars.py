r'''
utils.py

Description: 
   Provide definitions for lakes_cci-utility variables.

Written by William Chuter-Davies
'''


# Local Application/Library Specific Imports
from lib.esacci_lakes.objects import ESACCILakesVariable


ESACCI_LAKES_VARIABLES          = [ESACCILakesVariable('chla', 
                                                       'Concentration of Chlorophyll-a', 
                                                       'mg.m-3'), 
                                   ESACCILakesVariable('tsm', 
                                                       'Concentration of Total Suspended Matter', 
                                                       'g.m-3'),
                                   ESACCILakesVariable('acdom440', 
                                                       'Absorption Coefficient of Coloured Dissolved Organic Matter at 440 nm', 
                                                       'm-1'),
                                   ESACCILakesVariable('Kd490', 
                                                       'Vertical Diffuse Downwelling Attenuation Coefficient at 490 nm', 
                                                       'm-1'), 
                                   ESACCILakesVariable('KdPAR', 
                                                       'Vertical Diffuse Downwelling Attenuation Coefficient Aggregated Over PAR', 
                                                       'm-1'), 
                                   ESACCILakesVariable('phycocyanin', 
                                                       'Concentration of Phycocyanin Calculated From MDN Algorithm by O\'Shea et al. 2021', 
                                                       'mg.m-3'), 
                                   ESACCILakesVariable('lake_surface_water_temperature', 
                                                       'Lake Surface Skin Temperature', 
                                                       'kelvin'), 
                                   ESACCILakesVariable('lake_surface_water_extent', 
                                                       'Lake Water Extent', 
                                                       'km2')]

COUNT_OF_SMOKE_DAYS_LOWER_BOUND = 7
COUNT_OF_SMOKE_DAYS_UPPER_BOUND = 24