"""
Filename:   wfsel.sources.noaa_hms.literals.py
Author:     William Chuter-Davies
"""

NOAA_HMS_URL_TEMPLATE = "https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/Shapefile/%Y/%m/hms_smoke%Y%m%d.zip"

NOAA_HMS_DENSITY_NAME_TO_DENSITY_VALUE  = {
                                            "NA":       0,
                                            "Light":    1,
                                            "Medium":   2,
                                            "Heavy":    3,
                                        }
