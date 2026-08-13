#!/bin/bash

# Usage ./_.sh <esacci_lakes_id> <esacci_lakes_variable>

function help() {
    echo "usage: ${0} [options]
    
Runs view_all_low_smoke_years_and_one_high_smoke_year.py on assumed parameters.

positional arguments:
     esacci_lakes_id
          esacci_lakes_id as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0

     esacci_lakes_variable
        One of ['chla', 
                'tsm', 
                'acdom440', 
                'Kd490', 
                'KdPAR', 
                'phycocyanin', 
                'lake_surface_water_temperature', 
                'lake_surface_water_extent']"
}

if [[ "${1}" = "-h" || "${1}" = "--help" ]]; then
    help
    
    exit 1
fi

esacci_lakes_id="${1}"
esacci_lakes_variable="${2}"

psql -d spatial \
     -v esacci_lakes_id="${esacci_lakes_id}" \
     -v hms_smokes_table=hms_smokes2023 \
     < tools/db/query_esacci_lakes_smoke_days.sql \
     > data/"${esacci_lakes_id}".csv
python tools/dv/view_all_low_smoke_years_and_one_high_smoke_year.py \
       data/counts_of_smoke_days.csv \
       ~/Downloads/WFSEL/esacci/lakes/data \
       "${esacci_lakes_id}" \
       data/"${esacci_lakes_id}".csv \
       "${esacci_lakes_variable}"

rm data/"${esacci_lakes_id}".csv