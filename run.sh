#!/bin/bash
set -e
echo 'Removing old data dir (abort with ctrl+c)'
for i in 3 2 1 0
do
  sleep 1
  echo -ne "$i ..."
done
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
