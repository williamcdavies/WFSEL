# run from WFSEL/

A1="scripts/esa_lakes/C/build_esa_lakes_observations_csv.py"
A2="746"
A3="data/esa_lakes/queries/esa_counts_of_distinct_start_days_by_year.csv"
A4="data/esa_lakes/product"
A5="-o"
A6="746.csv"

python "${A1}" "${A2}" "${A3}" "${A4}" "${A5}" "${A6}"
