#!/bin/bash

# Usage ./batch_main_centroid.sh <buffer> <year>

if [ $# -ne 2 ]; then
    echo "Usage: ${0} <buffer> <year>"
    
    exit 1
fi

mkdir -p ~/Downloads/WFSEL/ESA/data/lakes/out/"${2}"

find ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/merged_product/"${2}" -type f -name "*.nc" -exec sh -c '
    buffer="${1}"
    year="${2}"
    ncfilename="${3}"
    ncbasename=$(basename "${ncfilename}" .nc)

    python main_centroid.py \
        "${buffer}" \
        "${ncfilename}" \
        ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/ESA_CCI_static_lake_mask.nc \
        ~/Downloads/WFSEL/ESA/data/lakes/lakescci_v2.1.0_metadata_filtered.csv \
        ~/Downloads/WFSEL/ESA/data/lakes/out/"${year}"/"${ncbasename}".csv
    ' _ "${1}" "${2}" {} \;