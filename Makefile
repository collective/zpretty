.PHONY: nosetests test flake8

all: bin/python
test: nosetests flake8

bin/python:
	@virtualenv .
	@bin/pip install -U pip
	@bin/pip install -U .[development,test]

nosetests:
	@echo "==== Running nosetests ===="
	@bin/nosetests

flake8:
	@echo "==== Running Flake8 ===="
	@bin/flake8 zpretty *.py

requirements: bin/python
	@bin/pip install -U .[development,test]
	@./bin/pip freeze --all|egrep -v '^(pkg-resources|zpretty)' > requirements-dev.txt
	@git difftool -y -x "colordiff -y" requirements-dev.txt
