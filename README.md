# Hotohete
Web page to share steam groups.


## Dev setup (Ubuntu/deb)

You need to install the nex dependencies:

	python 2.7
	postgresql 9.5
	pip


Then, install the python requirements with `pip` (it is recommend to use virtualenvs not installing at sytem root):

	pip install -r requirements-dev.txt

Also, you need to set-up your dabase, which you can do simply running a set-up script:

	./scripts/setup_db.sh


### Running tests

On CI the we run pylint and unit tests. To run tests with coverge and pytlint, you can run the next scripts from project root:

	./scripts/run_coverage.sh
	./scripts/run_pylint.sh

