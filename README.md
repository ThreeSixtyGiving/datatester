*
# _This repository has been superceeded by [dataquality](https://github.com/ThreeSixtyGiving/dataquality). The scripts from the datatester can be found in the "tools" directory of dataquality_
*


# 360Giving datatester

datatester is a tool to test 360Giving data that is listed on the [360Giving Registry](http://data.threesixtygiving.org). It is used to load [GrantNav](http://grantnav.threesixtygiving.org), and can be used by anyone needing to obtain 360Giving data directly from publishers.

This repo also contains scripts to produce a number of reports on the data, which is run nightly on [TravisCI](https://travis-ci.com/ThreeSixtyGiving/datatester/builds):

### status.json

A [JSON file](https://storage.googleapis.com/datagetter-360giving-output/branch/master/status.json) containing a wide range of insights into all of the files on the registry, including whether or not the file is valid, where it was obtained from and whether it’s appropriately licensed, aggregate statistics on the grants, insights into the identifiers present in the file, and information about the file itself. It is updated daily. It is provided on a best-effort basis and the URL is liable to change, so is not recommended for use in a live application. If you'd like to use this data in your application, please [contact us](info@threesixtygiving.org).

### report.csv

A [CSV report](https://gist.github.com/30d835ae16e2a30efde8a63acf03628d) of all the files in the Registry, along with some key stats such as the number of grants in a file, first/last awardDate, total value, and more.  It is updated daily. It is provided on a best-effort basis and the URL is liable to change, so is not recommended for use in a live application.


## Usage

Install dependencies:

```
python3 -m virtualenv -p $(which python3) .ve
source .ve/bin/activate
pip install -r requirements.txt
```

Run:

```
# Warning this deletes previously downloaded data
mkdir -p data/{original,json_all,json_valid,json_acceptable_license,json_acceptable_license_valid}
python get.py

When running the datatester, you may see several UserWarnings from python while running the script. You can happily ignore most of those that don't cause the program to fail. Run report.py, then read data/report.csv to review what datasets have been downloaded.
```

Generating a report of what data was downloaded/converted/valid:

```
python aggregates.py
python report.py
```

The script `run.sh` is provided for convenience. It does the run and report
steps above, and then creates a tar.gz of the data.

## Checking downloaded data for loading into GrantNav

GrantNav will only work properly if certain assumptions about the downloaded
data are correct. We have a script to help check these:

```
python check_grantnav_assumptions.py
```

If you get any lines that don't start with `Checking ` then something's gone wrong.
