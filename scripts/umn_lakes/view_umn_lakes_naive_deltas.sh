# run from WFSEL/

A1="scripts/umn_lakes/view_umn_lakes_naive_deltas.py"
A2="data/umn_lakes/results/a4_naive_deltas.csv"
A3="data/umn_lakes/results/cl_naive_deltas.csv"
A4="data/umn_lakes/results/sd_naive_deltas.csv"
A5="-o"
A6="naive_deltas.png"

python "${A1}" "${A2}" "${A3}" "${A4}" "${A5}" "${A6}"
