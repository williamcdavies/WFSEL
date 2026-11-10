# run from WFSEL/

A1="scripts/noaa_hms/etl_noaa_hms_parallel.py"
A2="2025-01-01"
A3="2025-12-31"
A4="-o"
A5="data/T"

python "${A1}" "${A2}" "${A3}" "${A4}" "${A5}"
