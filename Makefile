.PHONY: nosetests test flake8 black

all: bin/pip
test: nosetests flake8 black

bin/pip:
	virtualenv -p python3 . || python3 -m venv .
	./bin/pip install -U pip
	./bin/pip install -U .[development,test]

nosetests: bin/pip
	@echo "==== Running nosetests ===="
	./bin/nosetests

flake8: bin/pip
	@echo "==== Running Flake8 ===="
	./bin/flake8 zpretty *.py

bin/black: requirements-dev.txt
	./bin/pip install -r requirements-dev.txt
	touch bin/black

black: bin/black
	./bin/black --check zpretty

requirements: bin/pip
	./bin/pip install -U .[development,test]
	./bin/pip freeze --all|egrep -v '^(pkg-resources|zpretty|-f)' > requirements-dev.txt
	@git difftool -y -x "colordiff -y" requirements-dev.txt
