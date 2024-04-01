WORKDIR = app
DEVREQS = dev-requirements.txt
REQS = requirements.txt

style:
	black $(WORKDIR)
	isort $(WORKDIR)
	flake8 $(WORKDIR)
	mypy $(WORKDIR)
	pymarkdown scan .

test:
	pytest

install-dev-deps: dev-deps
	pip-sync $(DEVREQS)

install-deps: deps
	pip-sync $(REQS)

deps:
	pip install --upgrade pip pip-tools
	pip-compile --output-file $(REQS) --resolver=backtracking pyproject.toml

dev-deps: deps
	pip-compile --extra=dev --output-file $(DEVREQS) --resolver=backtracking pyproject.toml
