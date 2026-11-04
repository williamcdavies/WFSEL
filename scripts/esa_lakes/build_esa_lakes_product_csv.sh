# run from WFSEL/

A1="scripts/esa_lakes/build_esa_lakes_product_csv.py"
A2="data/esa_lakes/metadata_filtered.csv"
A3="data/esa_lakes/static_lake_mask.nc"
A4="/Volumes/TOSHIBA EXT/2023/01/ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-20230101-fv3.0.0.nc"
A5="-o"
A6="ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-20230101-fv3.0.0.csv"

python "${A1}" "${A2}" "${A3}" "${A4}" "${A5}" "${A6}"
