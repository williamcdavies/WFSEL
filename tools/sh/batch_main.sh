#!/bin/bash

# Usage ./batch_main.sh <buffer> <year>

function help() {
    echo "usage: ${0} [options]
    
Runs main.py on each netcdf file in ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/merged_product/<year>

positional arguments:
    buffer
        n in N | n >= 0 or 'inf'

    year
        s in ['2011', '2023']
    "
}

# If first argument is `-h` or `--help`, or argument count is not 2, exit 1
if [[ "${1}" = "-h" || "${1}" = "--help" || "$#" -ne 2 ]]; then
    help
    
    exit 1
fi

# Read first argument into `buffer`
buffer="${1}"

# Read second argument into `year`
year="${2}"

# If `buffer` is invalid, exit 1
if [[ ! "${buffer}" =~ ^([0-9]+|inf)$ ]]; then
    echo "error: argument buffer: unexpected value: "${buffer}""

    exit 1
fi

# If `year` is invalid, exit 1
if [[ ! "${year}" =~ ^(2011|2023)$ ]]; then
    echo "error: argument year: unexpected value: "${year}""

    exit 1
fi

# Ensure output directory exists
mkdir -p ~/Downloads/WFSEL/ESA/lakes/data/"${year}"

# Run `main.py` on each netcdf file in ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/merged_product/<year>
find ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/merged_product/"${year}" -type f -name "*.nc" -exec sh -c '
    # Read first argument into `buffer`
    buffer="${1}"
    
    # Read second argument into `year`
    year="${2}"

    # Read third argument into `ncfilename`
    ncfilename="${3}"

    # Read `ncfilename` basename into `ncbasename`
    ncbasename=$(basename "${ncfilename}" .nc)

    # Run `main.py`
    python main.py \
        "${buffer}" \
        "${ncfilename}" \
        ~/dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/ESA_CCI_static_lake_mask.nc \
        ~/Downloads/WFSEL/ESA/lakes/data/lakescci_v2.1.0_metadata_filtered.csv \
        ~/Downloads/WFSEL/ESA/lakes/data/"${year}"/"${ncbasename}".csv
    ' _ "${buffer}" "${year}" {} \;