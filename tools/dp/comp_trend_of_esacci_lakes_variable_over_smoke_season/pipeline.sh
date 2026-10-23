# Variables
V=lake_surface_water_temperature
OUT=data/archive/results_w4_late/results/C
TAB=$OUT/tables
RAW=$OUT/raw_data
CAT=$OUT/categorised_data
RES=$OUT/results
VIS=$OUT/visuals
META=data/esacci_lakes/metadata_filtered.csv
HYLAK=data/esacci_lakes/queries/hylak_field_values.csv
COUNTS=data/esacci_lakes/queries/counts_of_distinct_start_days_by_year.csv

# ----------------------------------------------------------------------
# Step 1 — raw data
# ----------------------------------------------------------------------
python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season/comp_trend_of_esacci_lakes_variable_over_smoke_season_C.py \
    $V data $META $COUNTS \
    -o $RAW

# ----------------------------------------------------------------------
# Step 2 — categorised data (three-way)
# ----------------------------------------------------------------------
python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py \
    $V $RAW/high_smoke_season_${V}_anomaly.csv $RAW/low_smoke_season_${V}_anomaly.csv \
    depth_avg_m $HYLAK -f Anomaly \
    -o $CAT/depth_avg_m_anomaly

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py \
    $V $RAW/high_smoke_season_${V}_anomaly.csv $RAW/low_smoke_season_${V}_anomaly.csv \
    lake_area_m2 $HYLAK -f Anomaly \
    -o $CAT/lake_area_m2_anomaly

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field.py \
    $V $RAW/high_smoke_season_${V}_anomaly.csv $RAW/low_smoke_season_${V}_anomaly.csv \
    vol_total_m3 $HYLAK -f Anomaly \
    -o $CAT/vol_total_m3_anomaly

# ----------------------------------------------------------------------
# Step 2 — categorised data (two-way)
# ----------------------------------------------------------------------
python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_alt.py \
    $V $RAW/high_smoke_season_${V}_anomaly.csv $RAW/low_smoke_season_${V}_anomaly.csv \
    elevation_m 500 $HYLAK -f Anomaly \
    -o $CAT/elevation_m_anomaly

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_by_hylak_field_alt.py \
    $V $RAW/high_smoke_season_${V}_anomaly.csv $RAW/low_smoke_season_${V}_anomaly.csv \
    pour_lat 50 $HYLAK -f Anomaly \
    -o $CAT/pour_lat_anomaly

# ----------------------------------------------------------------------
# Step 3 — statistics (three-way)
# ----------------------------------------------------------------------
python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/depth_avg_m_anomaly/upper_high_lakes.csv $CAT/depth_avg_m_anomaly/upper_low_lakes.csv \
    -o $RES/depth_avg_m_anomaly/upper

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/depth_avg_m_anomaly/middle_high_lakes.csv $CAT/depth_avg_m_anomaly/middle_low_lakes.csv \
    -o $RES/depth_avg_m_anomaly/middle

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/depth_avg_m_anomaly/lower_high_lakes.csv $CAT/depth_avg_m_anomaly/lower_low_lakes.csv \
    -o $RES/depth_avg_m_anomaly/lower

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/lake_area_m2_anomaly/upper_high_lakes.csv $CAT/lake_area_m2_anomaly/upper_low_lakes.csv \
    -o $RES/lake_area_m2_anomaly/upper

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/lake_area_m2_anomaly/middle_high_lakes.csv $CAT/lake_area_m2_anomaly/middle_low_lakes.csv \
    -o $RES/lake_area_m2_anomaly/middle

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/lake_area_m2_anomaly/lower_high_lakes.csv $CAT/lake_area_m2_anomaly/lower_low_lakes.csv \
    -o $RES/lake_area_m2_anomaly/lower

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/vol_total_m3_anomaly/upper_high_lakes.csv $CAT/vol_total_m3_anomaly/upper_low_lakes.csv \
    -o $RES/vol_total_m3_anomaly/upper

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/vol_total_m3_anomaly/middle_high_lakes.csv $CAT/vol_total_m3_anomaly/middle_low_lakes.csv \
    -o $RES/vol_total_m3_anomaly/middle

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/vol_total_m3_anomaly/lower_high_lakes.csv $CAT/vol_total_m3_anomaly/lower_low_lakes.csv \
    -o $RES/vol_total_m3_anomaly/lower

# ----------------------------------------------------------------------
# Step 3 — statistics (two-way)
# ----------------------------------------------------------------------
python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/elevation_m_anomaly/above_high_lakes.csv $CAT/elevation_m_anomaly/above_low_lakes.csv \
    -o $RES/elevation_m_anomaly/above

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/elevation_m_anomaly/below_high_lakes.csv $CAT/elevation_m_anomaly/below_low_lakes.csv \
    -o $RES/elevation_m_anomaly/below

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/pour_lat_anomaly/above_high_lakes.csv $CAT/pour_lat_anomaly/above_low_lakes.csv \
    -o $RES/pour_lat_anomaly/above

python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_statistics.py \
    $CAT/pour_lat_anomaly/below_high_lakes.csv $CAT/pour_lat_anomaly/below_low_lakes.csv \
    -o $RES/pour_lat_anomaly/below

# ----------------------------------------------------------------------
# Step 4 — visuals (three-way)
# ----------------------------------------------------------------------
python tools/dv/view_trend_of_esacci_lakes_variable_over_smoke_season.py \
    $V depth_avg_m \
    $CAT/depth_avg_m_anomaly/upper_high_lakes.csv $CAT/depth_avg_m_anomaly/upper_low_lakes.csv \
    $CAT/depth_avg_m_anomaly/middle_high_lakes.csv $CAT/depth_avg_m_anomaly/middle_low_lakes.csv \
    $CAT/depth_avg_m_anomaly/lower_high_lakes.csv $CAT/depth_avg_m_anomaly/lower_low_lakes.csv \
    $RES/depth_avg_m_anomaly/upper/results.csv \
    $RES/depth_avg_m_anomaly/middle/results.csv \
    $RES/depth_avg_m_anomaly/lower/results.csv \
    $RES/depth_avg_m_anomaly/upper/summary.csv \
    $RES/depth_avg_m_anomaly/middle/summary.csv \
    $RES/depth_avg_m_anomaly/lower/summary.csv \
    -f Anomaly -o $VIS/depth_avg_m_anomaly.png

python tools/dv/view_trend_of_esacci_lakes_variable_over_smoke_season.py \
    $V lake_area_m2 \
    $CAT/lake_area_m2_anomaly/upper_high_lakes.csv $CAT/lake_area_m2_anomaly/upper_low_lakes.csv \
    $CAT/lake_area_m2_anomaly/middle_high_lakes.csv $CAT/lake_area_m2_anomaly/middle_low_lakes.csv \
    $CAT/lake_area_m2_anomaly/lower_high_lakes.csv $CAT/lake_area_m2_anomaly/lower_low_lakes.csv \
    $RES/lake_area_m2_anomaly/upper/results.csv \
    $RES/lake_area_m2_anomaly/middle/results.csv \
    $RES/lake_area_m2_anomaly/lower/results.csv \
    $RES/lake_area_m2_anomaly/upper/summary.csv \
    $RES/lake_area_m2_anomaly/middle/summary.csv \
    $RES/lake_area_m2_anomaly/lower/summary.csv \
    -f Anomaly -o $VIS/lake_area_m2_anomaly.png

python tools/dv/view_trend_of_esacci_lakes_variable_over_smoke_season.py \
    $V vol_total_m3 \
    $CAT/vol_total_m3_anomaly/upper_high_lakes.csv $CAT/vol_total_m3_anomaly/upper_low_lakes.csv \
    $CAT/vol_total_m3_anomaly/middle_high_lakes.csv $CAT/vol_total_m3_anomaly/middle_low_lakes.csv \
    $CAT/vol_total_m3_anomaly/lower_high_lakes.csv $CAT/vol_total_m3_anomaly/lower_low_lakes.csv \
    $RES/vol_total_m3_anomaly/upper/results.csv \
    $RES/vol_total_m3_anomaly/middle/results.csv \
    $RES/vol_total_m3_anomaly/lower/results.csv \
    $RES/vol_total_m3_anomaly/upper/summary.csv \
    $RES/vol_total_m3_anomaly/middle/summary.csv \
    $RES/vol_total_m3_anomaly/lower/summary.csv \
    -f Anomaly -o $VIS/vol_total_m3_anomaly.png

# ----------------------------------------------------------------------
# Step 4 — visuals (two-way)
# ----------------------------------------------------------------------
python tools/dv/view_trend_of_esacci_lakes_variable_over_smoke_season_alt.py \
    $V elevation_m \
    $CAT/elevation_m_anomaly/above_high_lakes.csv $CAT/elevation_m_anomaly/above_low_lakes.csv \
    $CAT/elevation_m_anomaly/below_high_lakes.csv $CAT/elevation_m_anomaly/below_low_lakes.csv \
    $RES/elevation_m_anomaly/above/results.csv \
    $RES/elevation_m_anomaly/below/results.csv \
    $RES/elevation_m_anomaly/above/summary.csv \
    $RES/elevation_m_anomaly/below/summary.csv \
    500 -f Anomaly -o $VIS/elevation_m_anomaly.png

python tools/dv/view_trend_of_esacci_lakes_variable_over_smoke_season_alt.py \
    $V pour_lat \
    $CAT/pour_lat_anomaly/above_high_lakes.csv $CAT/pour_lat_anomaly/above_low_lakes.csv \
    $CAT/pour_lat_anomaly/below_high_lakes.csv $CAT/pour_lat_anomaly/below_low_lakes.csv \
    $RES/pour_lat_anomaly/above/results.csv \
    $RES/pour_lat_anomaly/below/results.csv \
    $RES/pour_lat_anomaly/above/summary.csv \
    $RES/pour_lat_anomaly/below/summary.csv \
    50 -f Anomaly -o $VIS/pour_lat_anomaly.png

# ----------------------------------------------------------------------
# Step 5 — deltas
# ----------------------------------------------------------------------
python tools/dp/comp_trend_of_esacci_lakes_variable_over_smoke_season_deltas/variable_windows.py \
    $META $HYLAK \
    $CAT/vol_total_m3_anomaly/lower_high_lakes.csv \
    $CAT/vol_total_m3_anomaly/lower_low_lakes.csv \
    $RES/vol_total_m3_anomaly/lower/summary.csv \
    $CAT/vol_total_m3_anomaly/middle_high_lakes.csv \
    $CAT/vol_total_m3_anomaly/middle_low_lakes.csv \
    $RES/vol_total_m3_anomaly/middle/summary.csv \
    $CAT/vol_total_m3_anomaly/upper_high_lakes.csv \
    $CAT/vol_total_m3_anomaly/upper_low_lakes.csv \
    $RES/vol_total_m3_anomaly/upper/summary.csv \
    -o $TAB/lake_deltas.csv

# ----------------------------------------------------------------------
# Step 6 — tables
# ----------------------------------------------------------------------
python summary.py data/archive/results_w4_late C -o $TAB/summary.csv