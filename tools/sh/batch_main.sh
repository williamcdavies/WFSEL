#!/bin/bash

# Usage ./batch_main.sh <year> <main*.py>

if [ $# -ne 2 ]; then
    echo "Usage: $0 <year> <main*.py>"
    
    exit 1
fi

mkdir -p ~/Downloads/WFSEL/ESA/data/lakes/out/"${1}"

find ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/merged_product/${1} -type f -name "*.nc" -exec sh -c '
    year="$1"
    script="$2"
    ncfile="$3"
    name=$(basename "$ncfile" .nc)
    python "$script" \
        "$ncfile" \
        ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/ESA_CCI_static_lake_mask.nc \
        ~/Downloads/WFSEL/ESA/data/lakes/lakescci_v2.1.0_metadata_filtered.csv \
        ~/Downloads/WFSEL/ESA/data/lakes/out/"${year}"/"${name}".csv
    ' _ "${1}" "${2}" {} \;