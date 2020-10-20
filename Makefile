.DEFAULT_GOAL := help
SRC_DIRS = ./gaunit ./tests

##### Dev

pip-comp: ## Compile requirements files
	pip-compile requirements/base.in
	pip-compile requirements/dev.in
	pip-compile requirements/robot.in

pip-up: ## Compile requirements files
	pip-compile --upgrade requirements/base.in
	pip-compile --upgrade requirements/dev.in
	pip-compile --upgrade requirements/robot.in

install-dev: setup-robot ## Install dev requirements
	pip install .
	pip install -r requirements/robot.txt
	pip install -r requirements/dev.txt

clean-logs:  ## Remove all log & RF report files
	rm logs/*.log log.html output.xml report.html || true

tests : test-unit test-lint test-format ## Run all tests

test-format: ## Run code formatting tests
	black --check --diff $(SRC_DIRS)

test-lint: ## Run code linting tests
	pylint --errors-only --ignore=templates ${SRC_DIRS}

test-unit:  ## Run unit tests
	python -m unittest discover tests

format: ## Format code
	black $(SRC_DIRS)

##### Use & Deploy

install-minimal:
	pip install 
	pip install -r requirements/base.txt

install-robot: ## Install Robot Framework requirements
	pip install .
	pip install -r requirements/robot.txt

###### Additional commands

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/\n               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'