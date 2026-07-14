#!/bin/bash

# Usage ./batch_main.sh <year>

if [ $# -ne 1 ]; then
    echo "Usage: ${0} <year>"
    
    exit 1
fi

mkdir -p ~/Downloads/WFSEL/ESA/data/lakes/out/"${1}"

find ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/merged_product/"${1}" -type f -name "*.nc" -exec sh -c '
    year="${1}"
    ncfilename="${2}"
    ncbasename=$(basename "${ncfilename}" .nc)

    python main.py \
        "$ncfilename" \
        ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/ESA_CCI_static_lake_mask.nc \
        ~/Downloads/WFSEL/ESA/data/lakes/lakescci_v2.1.0_metadata_filtered.csv \
        ~/Downloads/WFSEL/ESA/data/lakes/out/"${year}"/"${ncbasename}".csv
    ' _ "${1}" {} \;