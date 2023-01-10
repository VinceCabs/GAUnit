.DEFAULT_GOAL := help
.PHONY: docs
SRC_FILES = ./gaunit ./tests setup.py
FORMAT_FILES = ./gaunit ./tests setup.py ./examples 
PACKAGE = gaunit

##### Dev

docs: ## Build html documentation
	$(MAKE) -C docs

pip-comp: ## Compile requirements files
	pip-compile requirements/base.in
	pip-compile requirements/dev.in
	pip-compile requirements/samples.in

pip-up: ## Update requirements files
	pip-compile --upgrade --resolver=backtracking requirements/base.in
	pip-compile --upgrade --resolver=backtracking requirements/dev.in
	pip-compile --upgrade --resolver=backtracking requirements/samples.in

install-dev: ## * Install dev requirements
	pip install -e .
	pip install -r requirements/dev.txt
	npm install -g conventional-changelog-cli

install-examples: ## Install examples requirements
	pip install -e .
	pip install -r requirements/samples.txt

clean-logs:  ## Remove all log & RF report files
	rm *.log log.html output.xml report.html || true

tests : test-unit test-cli test-lint test-format test-package ## * Run all tests

test-format: ## Run code formatting tests
	black --check --diff $(FORMAT_FILES)

test-lint: ## Run code linting tests
	pylint --errors-only ${SRC_FILES}

test-unit:  ## Run unit tests (with coverage run)
	coverage run -m unittest discover tests

test-cli : ## Run tests on gaunit command
	ga --version
	ga check tests/test_cli_mock.har home_engie -t tests/tracking_plan.json
	ga check tests/test_cli_mock.har home_engie -t tests/tracking_plan.json | grep "OK: all expected events found"  # test for https://github.com/VinceCabs/GAUnit/issues/3
	ga check tests/test_cli_mock.har home_engie -t tests/tracking_plan.json --all
	ga extract tests/test_cli_mock.har -f dp | grep "[{'dp': 'A'}, {'dp': 'B'}, {'dp': 'C'}, {'dp': 'X'}]"
	
test-unit-v:  ## Run unit tests (verbose)
	coverage run -m unittest discover tests -v

test-package: build-package ## Test that package can be uploaded to pypi
	twine check dist/${PACKAGE}-$(shell make version).tar.gz

format: ## * Format code
	black $(FORMAT_FILES)

##### Use & Deploy

install-minimal: ## Install minimal usage requirements
	pip install --upgrade gaunit

build-package:   ## Build a python package ready to upload to pypi
	python setup.py sdist bdist_wheel

push-package: test-package ## * Build, test and push python packages to pypi
	python -m twine upload --skip-existing dist/${PACKAGE}-*.tar.gz

changelog:  ## updates CHANGELOG.md
	conventional-changelog ---preset angular --infile CHANGELOG.md --same-file

release: tests ## * Test, create a release tag and push it to repos (origin and public)
	$(MAKE) retag release-origin TAG=v$(shell make version)

retag:
	@echo "=== Creating tag $(TAG)"
	git tag -d $(TAG) || true
	git tag $(TAG)

release-origin:
	@echo "=== Pushing tag $(TAG) to origin"
	git push origin
	git push origin :$(TAG) || true
	git push origin $(TAG)

release-public:
	@echo "=== Pushing tag $(TAG) to public"
	git push public
	git push public :$(TAG) || true
	git push public $(TAG)

###### Additional commands

version: ## Print the current tutor version
	@python -c 'import io, os; about = {}; exec(io.open(os.path.join("${PACKAGE}", "__about__.py"), "rt", encoding="utf-8").read(), about); print(about["__version__"])'

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/\n               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'