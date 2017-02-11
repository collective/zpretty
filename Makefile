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
