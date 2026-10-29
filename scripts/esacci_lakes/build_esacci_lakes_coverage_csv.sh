# run from WFSEL/

A0="scripts/esacci_lakes/build_esacci_lakes_coverage_csv.py"
A1="data/esacci_lakes/metadata_filtered.csv"
A2="data/esacci_lakes/queries/counts_of_distinct_start_days_by_year.csv"
A3="data/esacci_lakes/merged_product"
A4="-o"
A5="coverage.csv"

python ${A0} ${A1} ${A2} ${A3} ${A4} ${A5}
