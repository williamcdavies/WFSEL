# run from WFSEL/

A1="scripts/esa_lakes/view_esa_lakes_observation_distributions_by_week.py"
A2="data/archive/results_w4_late/results/C/raw_data/high_smoke_season_lake_surface_water_temperature_anomaly.csv"
A3="data/archive/results_w4_late/results/C/raw_data/low_smoke_season_lake_surface_water_temperature_anomaly.csv"
A4="1"
A5="20"
A6="-o"
A7="anomaly_distributions.svg"
A8="-d"
A9="3"
A10="-e"
A11="45"
A12="-a"
A13="-45"

# python "${A1}" "${A2}" "${A3}" "${A4}" "${A5}" "${A6}" "${A7}"
python "${A1}" "${A2}" "${A3}" "${A4}" "${A5}" "${A6}" "${A7}" "${A8}" "${A9}" "${A10}" "${A11}" "${A12}" "${A13}"
