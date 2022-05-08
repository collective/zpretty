.PHONY: pytests test flake8 black

all: py3/bin/pip
test: pytest

py3/bin/pip:
	python3 -m venv py3
	./py3/bin/pip install -U pip
	./py3/bin/pip install -U .[development,test]

pytest: py3/bin/pip
	@echo "==== Running nosetests ===="
	./py3/bin/pytest

flake8: py3/bin/pip
	@echo "==== Running Flake8 ===="
	./bin/flake8 zpretty *.py

py3/bin/black: requirements-dev.txt
	./bin/pip install -r requirements-dev.txt
	touch bin/black

black: py3/bin/black
	./py3/bin/black --check zpretty

requirements: py3/bin/pip
	./py3/bin/pip install -Ue .[development,test]
	./py3/bin/pip freeze --all|egrep -v '^(pip|pkg-resources|wheel|-e|-f)' > requirements-dev.txt
	@git difftool -y -x "colordiff -y" requirements-dev.txt
