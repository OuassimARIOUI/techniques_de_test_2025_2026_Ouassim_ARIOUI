PY ?= python

test:
	$(PY) -m pytest -v

unit_test:
	$(PY) -m pytest -v -m "not perf"

perf_test:
	$(PY) -m pytest -v -m "perf"

coverage:
	$(PY) -m coverage run -m pytest && $(PY) -m coverage report -m

lint:
	$(PY) -m ruff check triangulator

doc:
	$(PY) -m pdoc3 --html triangulator --output-dir docs

