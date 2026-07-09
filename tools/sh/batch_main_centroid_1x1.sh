#!/bin/bash

# Usage ./batch_nc <year>

find ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/merged_product/${1} -type f -name "*.nc" -exec sh -c '
    name=$(basename "${1}" .nc)
    
    python main_centroid_1x1.py \
        "${1}" \
        ~/Downloads/WFSEL/ESA_CCI/data/csv/lakescci_v2.1.0_metadata_filtered.csv \
        ~/Downloads/WFSEL/ESA_CCI/data/out/${2}/${name}.csv
    ' _ {} ${1} \;