# run from WFSEL/

A0="scripts/esacci_lakes/build_esacci_lakes_merged_product_csv.py"
A1="data/esacci_lakes/metadata_filtered.csv"
A2="data/esacci_lakes/static_lake_mask.nc"
A3="/Volumes/TOSHIBA EXT/2023/01/ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-20230101-fv3.0.0.nc"
A4="-o"
A5="ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-20230101-fv3.0.0.csv"

python "${A0}" "${A1}" "${A2}" "${A3}" "${A4}" "${A5}"
