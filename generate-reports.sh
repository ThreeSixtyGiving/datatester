#!/bin/bash
# Note these python scripts all assume './data/' dir
set -e
echo 'Generating status.json'
python aggregates.py
echo 'Generating coverage.json'
python coverage.py
echo 'Generating report.csv'
python report.py
echo 'Finished'
