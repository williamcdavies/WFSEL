# run from WFSEL/

A1="scripts/esacci_lakes/build_esacci_lakes_coverage_csv.py"
A2="data/esacci_lakes/metadata_filtered.csv"
A3="data/esacci_lakes/queries/counts_of_distinct_start_days_by_year.csv"
A4="data/esacci_lakes/merged_product"
A5="-o"
A6="coverage.csv"

python "${A1}" "${A2}" "${A3}" "${A4}" "${A5}" "${A6}"
