#!/bin/bash
set -e
rm -r data || true
mkdir -p data/{original,json_all,json_valid,json_acceptable_license,json_acceptable_license_valid}
echo 'Fetching and converting data'
python get.py $@
python aggregates.py
python coverage.py
echo 'Generating report.csv'
python report.py
echo 'Creating tarball'
tar -czf data_$(date +%F).tar.gz data
echo 'Finished'
