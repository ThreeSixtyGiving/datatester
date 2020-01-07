#!/bin/bash
# 1. Deletes old data
# 2. Runs datagetter
# 3. Runs reports generation
# 4. Creates tar archive

set -e
echo 'Removing old data dir (abort with ctrl+c)'
for i in 3 2 1 0
do
  sleep 1
  echo -ne "$i ..."
done
rm -r data || true
echo 'Fetching and converting data'
datagetter.py $@
bash generate-reports.sh
echo 'Creating tarball'
tar -czf data_$(date +%F).tar.gz data
echo 'Finished'
