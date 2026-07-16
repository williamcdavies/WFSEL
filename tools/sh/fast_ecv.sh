#!/bin/bash

# Usage ./fast_ecv.sh [options]

function help() {
    echo "usage: ${0} [options]
    
Description

positional arguments:
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

# Read fourth argument into `ecv_data_dir_path`
ecv_data_dir_path="${4}"

# Read fifth argument into `x_label`
x_label="${5}"

# Read sixth argument into `y_label`
y_label="${6}"

# Read seventh argument into `t_label`
t_label="${7}"

# Read eighth argument into `reg_colour`
reg_colour="${8}"

# Read ninth argument into `hist_colour`
hist_colour="${9}"

# Read tenth argument into `lakes_id`
lakes_id="${10}"

# Read eleventh argument into `year`
year="${11}"

# If `lakes_cci_id` is invalid, exit 1
if [[ ! "${lakes_cci_id}" =~ ^[0-9]+$ ]]; then
    echo "error: argument lakes_cci_id: unexpected value: "${lakes_cci_id}""

    exit 1
fi

# If `lakes_id` is invalid, exit 1
if [[ ! "${lakes_id}" =~ ^[0-9]+$ ]]; then
    echo "error: argument lakes_id: unexpected value: "${lakes_id}""

    exit 1
fi

# If `year` is invalid, exit 1
if [[ ! "${year}" =~ ^[0-9]{4}$ ]]; then
    echo "error: argument year: unexpected value: "${year}""

    exit 1
fi

# Set `smoke_data_csv_path`
smoke_data_csv_path=data/"${lakes_id}"_"${year}".csv

psql -d spatial \
    -v lakes_id="${lakes_id}" -v hms_smokes_table=hms_smokes"${year}" \
    -f tools/db/query_smoke_data.sql \
    > "${smoke_data_csv_path}"

python tools/dv/ecv.py \
    "${lakes_cci_id}" "${ecv}" "${measure}" "${ecv_data_dir_path}" "${smoke_data_csv_path}" \
    --x_label "${x_label}" --y_label "${y_label}" --t_label "${t_label}" --reg_colour "${reg_colour}" --hist_colour "${hist_colour}"