#!/bin/bash
# This follows broadly the approach from
# http://www.kennethreitz.org/essays/a-better-pip-workflow
rm -rf .ve
virtualenv --python=python3 .ve
source .ve/bin/activate
pip install --upgrade -r requirements.in
pip freeze -r requirements.in | grep -v 'pkg-resources' > requirements.txt
# Put comments back on the same line (mostly for requires.io's benefit)
sed -i '$!N;s/\n#\^\^/ #/;P;D' requirements*txt
sed -i 's/^-r.*//' requirements*txt
