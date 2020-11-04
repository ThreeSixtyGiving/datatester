#!/bin/bash
# Travis deploy gist
gem install gist
echo $GIST_TOKEN > ~/.gist
gist -u 30d835ae16e2a30efde8a63acf03628d data/report.csv
gist -u 0ce4a96df3c8cd773079152552ae1381 data/coverage.json
gist -u cd8c12e426157478e2e8a537f99ecaef data/status.json
