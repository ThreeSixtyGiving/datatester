#!/bin/bash
rm -r data
mkdir -p data/{original,json_all,json_valid,json_acceptable_license,json_acceptable_license_valid}
python get.py
python report.py
tar -czf data_$(date +%F).tar.gz data
