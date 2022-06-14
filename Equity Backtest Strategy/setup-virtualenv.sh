#!/usr/bin/env bash

set -x
set -e

#
# Create Python virtualenv.
#
python3 -m venv venv
. ./venv/bin/activate

#
# Install requirements.
#

pip install requests pandas yfinance numpy matplotlib

set +x
set +e

# Print command to run.
echo "Run \". venv/bin/activate\" to enter virtualenv."
