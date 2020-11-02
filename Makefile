# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# list all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
.PHONY: list
# required for list
no_targets__:

# install dependencies and pre-commit hooks
setup:
	@PIP_REQUIRE_VIRTUALENV=true pip install -Ur requirements.txt
	@pre-commit install -f --hook-type pre-commit
	@pre-commit install -f --hook-type pre-push
.PHONY: setup

# install dependencies
setup-ci:
	@pip install -Ur requirements.txt black flake8 isort
.PHONY: setup-ci

# run isort, black and flake8 for style guide enforcement
isort:
	@isort .
.PHONY: isort

black:
	@black .
.PHONY: black

flake8:
	@flake8
.PHONY: flake8

lint: isort black flake8
.PHONY: lint

# run all missions
run:
	@for mission in *.py; do \
		echo "==> Running $$mission..."; \
		python $$mission; \
	done;
.PHONY: run

# run the specified mission (e.g.: make 00-warmup.py)
%.py: FORCE
	@python $*.py
FORCE:

# clean python object, test and coverage files
pyclean:
	@find . -type f -name "*.pyc" -delete -print
	@find . -type f -iname '.coverage' -exec rm -rf \{\} + -print
	@find . -type d -iname '.pytest_cache' -exec rm -rf \{\} + -print
	@find . -type d -iname '__pycache__' -exec rm -rf \{\} + -print
	@find . -type d -iname '.benchmarks' -exec rm -rf \{\} + -print
	@find . -type d -iname '*.egg-info' -exec rm -rf \{\} + -print
.PHONY: pyclean

# run `pyclean` and remove generated files
clean: pyclean
	@rm *.gif *.jpg *.p *.pack *.png *.wav *.zip
.PHONY: clean
