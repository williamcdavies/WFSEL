# run from WFSEL/

A1="scripts/esa_lakes/build_esa_lakes_product_csv_parallel.py"
A2="data/esa_lakes/metadata_filtered.csv"
A3="data/esa_lakes/static_lake_mask.nc"
A4="/Volumes/TOSHIBA EXT/"
A5="-o"
A6="data/T"

python "${A1}" "${A2}" "${A3}" "${A4}" "${A5}" "${A6}"
