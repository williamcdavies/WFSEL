# run from WFSEL/

A0="scripts/esacci_lakes/build_esacci_lakes_distinct_start_days_mask_csv.py"
A1="data/esacci_lakes/metadata_filtered.csv"
A2="data/esacci_lakes/queries/counts_of_distinct_start_days_by_year.csv"
A3="-o"
A4="distinct_start_days_mask.csv"

python "${A0}" "${A1}" "${A2}" "${A3}" "${A4}"
