# GDPR Cleanup

This set of Python 3.6 scripts will erase private data from ActionKit users listed in a database table.

Before running, do this:

`pip install -r requirements.txt`

Then copy `settings.py.example` to `settings.py` and fill in your info.

All parameters can be passed as command-line flags, lambda event keys, set in `settings.py`, or set as environment variables, and are prioritized in that order. To see all available parameters for a given script, run with `--help`.
