### Red-red archiver

* Python 3.x script 
* Enables bulk archiving of Redshift tables using the Redash API.
* create a python3 virtualenv `virtualenv -p python3 venv && source venv/bin/activate && pip install -r requirements.txt`
* Fill out settings.py using the example file and make sure you have aws credentials stored in the usual place.
* run with `python archive.py`