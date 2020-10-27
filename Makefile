.DEFAULT_GOAL := help
SRC_FILES = ./gaunit ./tests setup.py

##### Dev

pip-comp: ## * Compile requirements files
	pip-compile requirements/base.in
	pip-compile requirements/dev.in
	pip-compile requirements/robot.in

pip-up: ## Update requirements files
	pip-compile --upgrade requirements/base.in
	pip-compile --upgrade requirements/dev.in
	pip-compile --upgrade requirements/robot.in

install-dev: ## * Install dev requirements
	pip install .
	pip install -r requirements/robot.txt
	pip install -r requirements/dev.txt

clean-logs:  ## Remove all log & RF report files
	rm *.log log.html output.xml report.html || true

tests : test-unit test-robot test-lint test-format ## Run all tests

test-format: ## Run code formatting tests
	black --check --diff $(SRC_FILES)

test-lint: ## Run code linting tests
	pylint --errors-only ${SRC_FILES}

test-unit:  ## Run unit tests
	python -m unittest discover tests

test-robot:  ## Run RobotFramework library
	robot tests/test_home_engie.robot

format: ## Format code
	black $(SRC_FILES)

##### Use & Deploy

install-minimal: ## Install minimal usage requirements
	pip install .
	pip install -r requirements/base.txt

install-robot: ## Install Robot Framework requirements
	pip install .
	pip install -r requirements/robot.txt

build-package:   ## Build a python package ready to upload to pypi
	python setup.py sdist bdist_wheel

push-package: ## Push python packages to pypi
	python -m twine upload --skip-existing dist/*

###### Additional commands

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/\n               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'