#!/bin/bash

find ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/merged_product -type f -name "*.nc" -exec sh -c '
    name=$(basename "${1}" .nc)
    
    python main.py \
        "$1" \
        ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/ESA_CCI_static_lake_mask.nc \
        ~/Downloads/WFSEL/ESA_CCI/data/csv/lakescci_v2.1.0_metadata_filtered.csv \
        ~/Downloads/WFSEL/ESA_CCI/data/out/2023/${name}.csv
    ' _ {} \;