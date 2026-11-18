# run from WFSEL/

A1="scripts/umn_lakes/view_umn_lakes_product.py"
A2="41008400"
A3="data/umn_lakes/product"
A4="-o"
A5="UMN_${A2}_stratified.svg"

python "${A1}" "${A2}" "${A3}" "${A4}" "${A5}"
