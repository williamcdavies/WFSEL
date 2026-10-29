# run from WFSEL/

A0="scripts/esacci_lakes/build_esacci_lakes_deltas_csv.py"
A1="data/archive/results_w4_late/results/C/raw_data/high_smoke_season_lake_surface_water_temperature_anomaly.csv"
A2="data/archive/results_w4_late/results/C/raw_data/low_smoke_season_lake_surface_water_temperature_anomaly.csv"
A3="1"
A4="20"
A5="-o"
A6="deltas.csv"

python ${A0} ${A1} ${A2} ${A3} ${A4} ${A5} ${A6}
