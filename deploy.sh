#!/bin/bash
# Script to deploy the results of the data reports
DATA_DIR=$1
DEPLOY_DIR=$2
PREFIX=$3
GIST_SHA=$4

function help {
  echo "Deploy the output of data tests"
  echo "Usage: deploy.sh <data_dir> <deploy_dir> <prefix> <gist_sha>"
}

if [[ $1 == '--help' || $1 == '-h' ]]
then
  help
  exit 0
fi

if [[ $1 == "" || $2 == "" || $3 == "" || $4 == "" ]]
then
  echo "Not enough parameters"
  help
  exit 1
fi

if [ ! -e ~/.gist ]
then
  echo "Gist config not present ~/.gist"
  help
  exit 1
fi

cp $DATA_DIR/data_all.json $DEPLOY_DIR/$PREFIX\_data_all.json
cp $DATA_DIR/report.csv $DEPLOY_DIR/$PREFIX\_report.csv
cp $DATA_DIR/coverage.json $DEPLOY_DIR/$PREFIX\_coverage.json

# We don't always have this one
if [ -e $DATA_DIR/status.json ]
then
  cp $DATA_DIR/status.json $DEPLOY_DIR/$PREFIX\_status.json
fi

# Ruby! https://guides.rubygems.org/faqs/#user-install 
PATH="$(ruby -r rubygems -e 'puts Gem.user_dir')/bin:$PATH"

gem install gist --user-install

gist -u $GIST_SHA $DEPLOY_DIR/$PREFIX\_report.csv
