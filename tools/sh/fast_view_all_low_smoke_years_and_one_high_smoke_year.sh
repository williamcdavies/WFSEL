#!/bin/bash

# Usage ./fast_view_all_low_smoke_years_and_one_high_smoke_year.sh <lakes_cci_id> <ecv> <measure>

function help() {
    echo "usage: ${0} [options]
    
Runs view_all_low_smoke_years_and_one_high_smoke_year.py on assumed parameters.

positional arguments:
     lakes_cci_id
          lakes_cci_id as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0

     ecv
        One of ['chla', 
                'tsm', 
                'acdom440', 
                'Kd490', 
                'KdPAR', 
                'phycocyanin', 
                'lake_surface_water_temperature', 
                'lake_surface_water_extent']

     measure
          One of ['mean', 
                  'median', 
                  'var', 
                  'max', 
                  'min']
    "
}

# If first argument is `-h` or `--help`, exit 1
if [[ "${1}" = "-h" || "${1}" = "--help" ]]; then
    help
    
    exit 1
fi

# Read first argument into `lakes_cci_id`
lakes_cci_id="${1}"

# Read second argument into `ecv`
ecv="${2}"

# Read third argument into `measure`
measure="${3}"

psql -d spatial \
     -v lakes_cci_id="${lakes_cci_id}" \
     -v hms_smokes_table=hms_smokes2021 \
     < tools/db/query_smoke_days.sql \
     > data/"${lakes_cci_id}".csv
python tools/dv/view_all_low_smoke_years_and_one_high_smoke_year.py \
       "${lakes_cci_id}" \
       "${ecv}" \
       "${measure}" \
       ~/Downloads/WFSEL/ESA/lakes/data/ \
       data/count_of_smoke_days.csv \
       data/"${lakes_cci_id}".csv

rm data/"${lakes_cci_id}".csv