.PHONY: all
all: install

.PHONY: test
test: pre-commit pytest

.venv/bin/pip:
	python3 -m venv .venv

.PHONY: install
install: .venv/bin/pip
	./.venv/bin/pip install -IU pip
	./.venv/bin/pip install -IU .[development,test]
	./.venv/bin/pip install -e .

requirements := $(wildcard requirements-dev.txt requirements.d/*.txt)

.venv/bin/pre-commit: $(requirements)
	make install

.venv/bin/pytest: $(requirements)
	make install

.PHONY: pre-commit
pre-commit: .venv/bin/pre-commit
	./.venv/bin/pre-commit install
	./.venv/bin/pre-commit run --all

.PHONY: pytests
pytest: .venv/bin/pytest
	./.venv/bin/pytest

.PHONY: htmlreport
htmlreport: .venv/bin/pytest
	./.venv/bin/pytest --cov-report html
