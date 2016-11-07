# 360Giving Data Getter

Install dependencies:

```
python3 -m virtualenv -p $(which python3) .ve
source .ve/bin/activate
pip install -r requirements.txt
```

Run:

```
mkdir -p data/{original,json_all,json_valid,json_acceptable_license,json_acceptable_license_valid}
python get.py
```

## Checking downloaded data

GrantNav will only work properly if certain assumptions about the downloaded
data are correct. We have a script to help check these:

```
python check_grantnav_assumptions.py
```

If you get any lines that don't start with `Checking ` then something's gone wrong.
