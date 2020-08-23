# solid-spork

## Install steps

- required Python 3. Tested on Python 3.8, will possibly work on lower versions
  up to 3.6.

Steps:

1. (optional) virtual environment
	- create virtual environment using `python -m venv env`
	- change source using `source env/bin/activate`
2. install required packages with `pip install -r requirements.txt`
3. `export FLASK_APP=app.py`
4. `flask run`

The server will run on port 5000. Use your browser to navigate to
`localhost:5000`. When running the first time, make sure to add some data into
database.

## Known 'features'

- when dictionary is very long, `bash` command gets too long when compiling and
  breaks. This could be solved by writing `.tex` file to disk rather than
  giving `LaTeX` text as arguments to `pdflatex` command. Please don't give too
  long input to dictionaries. Thank you
- (possibly) jinja has no LaTeX escaping implemented so it is possible that
  some characters might be feeded into dictionary and break generating PDF. So
  far the escaped characters are: `&`, `$`, `_` and `%`.
- sometimes there are errors with matplotlib since it is run on server and not
	on main thread. Therefore it's sometimes needed to restart server
