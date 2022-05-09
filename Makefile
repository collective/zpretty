.PHONY: all
all: py3/bin/pip

.PHONY: test
test: pre-commit pytest

requirements := $(wildcard requirements-dev.txt requirements.d/*.txt)
py3/bin/pip: $(requirements)
	python3 -m venv py3
	./py3/bin/pip install -IU pip
	./py3/bin/pip install -IU .[development,test]


./py3/bin/pre-commit: py3/bin/pip

.PHONY: pre-commit
pre-commit:
	./py3/bin/pre-commit install
	./py3/bin/pre-commit run --all

.PHONY: pytests
pytest: py3/bin/pip
	./py3/bin/pytest

.PHONY: htmlreport
htmlreport: py3/bin/pip
	./py3/bin/pytest --cov-report html

.PHONY: requirements
requirements: py3/bin/pip
	./py3/bin/pip install -Ue .[development,test]
	./py3/bin/pip freeze --all|egrep -v '^(pip|pkg-resources|wheel|-e|-f)' > requirements.d/requirements-dev.txt
	@git difftool -y -x "colordiff -y" requirements.d/requirements-dev.txt
