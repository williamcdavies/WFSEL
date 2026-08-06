#!/bin/bash

# Usage ./fast_view_all_low_smoke_years_and_one_high_smoke_year.sh <lakes_cci_id> <ecv> <measure>

LAKES_CCI_ID="${1}"
ECV="${2}"
MEASURE="${3}"

psql -d spatial \
     -v lakes_cci_id="${LAKES_CCI_ID}" \
     -v hms_smokes_table=hms_smokes2021 \
     < tools/db/query_smoke_days.sql \
     > data/"${LAKES_CCI_ID}".csv
python tools/dv/view_all_low_smoke_years_and_one_high_smoke_year.py \
       "${LAKES_CCI_ID}" \
       "${ECV}" \
       "${MEASURE}" \
       ~/Downloads/WFSEL/ESA/lakes/data/ \
       data/count_of_smoke_days.csv \
       data/"${LAKES_CCI_ID}".csv

rm data/"${LAKES_CCI_ID}".csv