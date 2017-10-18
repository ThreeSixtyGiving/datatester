# 360Giving Data Getter

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

When running the datagetter, you may see several UserWarnings from python while running the script. You can happily ignore most of those that don't cause the program to fail. Run data/report.csv to review what datasets have been downloaded.
```

Generating a report of what data was downloaded/converted/valid:

```
python report.py
```

The script `run.sh` is provided for convenience. It does the run and report
steps above, and then creates a tar.gz of the data.

## Checking downloaded data

GrantNav will only work properly if certain assumptions about the downloaded
data are correct. We have a script to help check these:

```
python check_grantnav_assumptions.py
```

If you get any lines that don't start with `Checking ` then something's gone wrong.
