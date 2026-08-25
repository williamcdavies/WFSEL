#!/bin/bash

# Usage ./batch_main.sh <path>

function help() {
    echo "usage: ${0} [options]

Runs main.py on each netcdf file in <path>
"
}

# If first argument is `-h` or `--help`, or argument count is not 1, exit 1
if [[ "${1}" = "-h" || "${1}" = "--help" || "$#" -ne 1 ]]; then
    help
    exit 1
fi

# Read first argument into `path`
path="${1}"

# Read basename of `path` into `outdir`
outdir="$(basename "${path}")"

# Ensure output directory exists
mkdir -p "data/main.py/buffer_inf/${outdir}"

# Run `main.py` on each netcdf file in <path>, skipping macOS AppleDouble shadow files
find "${path}" -type f -name "*.nc" ! -name "._*" -exec sh -c '
    ncfilename="$1"
    ncbasename=$(basename "${ncfilename}" .nc)
    outdir="$2"

    python main.py \
        data/lakescci_v2.1.0_metadata_filtered.csv \
        data/ESA_CCI_static_lake_mask.nc \
        "${ncfilename}" \
        "data/main.py/buffer_inf/${outdir}/${ncbasename}.csv"
' _ {} "${outdir}" \;