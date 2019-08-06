#!/bin/bash
set -e
rm -r data || true
echo 'Fetching and converting data'
echo $PATH
datagetter.py $@
python aggregates.py
python coverage.py
echo 'Generating report.csv'
python report.py
echo 'Creating tarball'
tar -czf data_$(date +%F).tar.gz data
echo 'Finished'
