test:
	pytest -v

unit_test:
	pytest -v -m "not perf"

perf_test:
	pytest -v -m "perf"

coverage:
	coverage run -m pytest && coverage report

lint:
	ruff check implementation/triangulator

doc:
	pdoc3 --html implementation/triangulator --output-dir docs
