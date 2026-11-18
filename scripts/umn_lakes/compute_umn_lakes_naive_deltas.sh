# run from WFSEL/

A1="scripts/umn_lakes/compute_umn_lakes_naive_deltas.py"
A2="data/umn_lakes/product"
A3="-o"
A4="data/T"

python "${A1}" "${A2}" "${A3}" "${A4}"
