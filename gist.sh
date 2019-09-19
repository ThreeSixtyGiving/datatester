#!/bin/bash
# Travis deploy gist
gem install gist
echo $GIST_TOKEN > ~/.gist
gist -u 30d835ae16e2a30efde8a63acf03628d data/report.csv
