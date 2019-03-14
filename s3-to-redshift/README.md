# S3 to Redshift

This set of Python 3 scripts will import files from S3 to Redshift. `import_s3_file.py` can import a single file. `s3_file_list.py` can give a list of files in a directory. And `import_s3_directory` combines the previous two to import all files in a directory.

Before running, do this:

`pip install -r requirements.txt`

Then copy `settings.py.example` to `settings.py` and fill in your info.

All parameters can be set as environment variables, passed as command-line flags, or set in `settings.py`, and are prioritized in that order. To see all available parameters for a given script, run with `--help`.
