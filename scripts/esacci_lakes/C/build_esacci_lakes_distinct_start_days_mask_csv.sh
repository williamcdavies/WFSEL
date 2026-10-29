# run from WFSEL/

A1="scripts/esacci_lakes/build_esacci_lakes_distinct_start_days_mask_csv.py"
A2="data/esacci_lakes/metadata_filtered.csv"
A3="data/esacci_lakes/queries/counts_of_distinct_start_days_by_year.csv"
A4="-o"
A5="distinct_start_days_mask.csv"

python "${A1}" "${A2}" "${A3}" "${A4}" "${A5}"
