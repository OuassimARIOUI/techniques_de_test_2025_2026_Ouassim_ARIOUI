VENV_PYTHON = $(shell which python3)

test:
	$(VENV_PYTHON) -m pytest -v

unit_test:
	$(VENV_PYTHON) -m pytest -v -m "not perf"

perf_test:
	$(VENV_PYTHON) -m pytest -v -m "perf"

coverage:
	$(VENV_PYTHON) -m coverage run -m pytest && coverage report

lint:
	$(VENV_PYTHON) -m ruff check triangulator

doc:
	$(VENV_PYTHON) -m pdoc3 --html triangulator --output-dir docs
