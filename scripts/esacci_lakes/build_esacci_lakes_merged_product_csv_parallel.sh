# run from WFSEL/

A1="scripts/esacci_lakes/build_esacci_lakes_merged_product_csv_parallel.py"
A2="data/esacci_lakes/metadata_filtered.csv"
A3="data/esacci_lakes/static_lake_mask.nc"
A4="/Volumes/TOSHIBA EXT/"
A5="-o"
A6="data/esacci_lakes/T"

python "${A1}" "${A2}" "${A3}" "${A4}" "${A5}" "${A6}"
