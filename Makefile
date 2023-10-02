.DEFAULT_GOAL := help

PYTHON ?= $(shell which python)


.PHONY: help
help: ## Prints help for available target rule
	$(info Available target rules:)
	@echo
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: clean-pyc
clean-pyc:
	$(info Cleaning Python files..)
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@find . -iname '.coverage' -delete
	@rm -rf htmlcov/


.PHONY: clean-dist
clean-dist:
	$(info Cleaning Python distribution files..)
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info


.PHONY: clean
clean: clean-pyc clean-dist  ## Cleans project building and caching files


.PHONY: test
test:  ## Runs project tests using Pytest
	$(info Running project tests..)
	py.test -vvv --cov=simple_rest_client tests


.PHONY: dist
dist: clean
	$(info Building Python distribution..)
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel


.PHONY: release
release: dist  ## Generates a new project release
	$(info Generating a new project release..)
	git tag `python setup.py -q version`
	git push origin `python setup.py -q version`
	twine upload dist/*


.PHONY: lint
lint:  ## Runs Python lint on the source code
	$(info Running lint against project..)
	SKIP=no-commit-to-branch pre-commit run -a -v
