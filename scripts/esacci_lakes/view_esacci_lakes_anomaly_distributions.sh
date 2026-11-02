# run from WFSEL/

A1="scripts/esacci_lakes/view_esacci_lakes_anomaly_distributions.py"
A2="data/archive/results_w4_late/results/C/raw_data/high_smoke_season_lake_surface_water_temperature_anomaly.csv"
A3="data/archive/results_w4_late/results/C/raw_data/low_smoke_season_lake_surface_water_temperature_anomaly.csv"
A4="1"
A5="20"
A6="-o"
A7="anomaly_distributions.svg"

python "${A1}" "${A2}" "${A3}" "${A4}" "${A5}" "${A6}" "${A7}"
