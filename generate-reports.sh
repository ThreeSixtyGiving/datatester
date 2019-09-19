#!/bin/bash
# Note these python scripts all assume './data/' dir
set -e
python aggregates.py
python coverage.py
echo 'Generating report.csv'
python report.py
echo 'Finished'
