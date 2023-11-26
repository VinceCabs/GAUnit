#!/usr/bin/env bash
TIMEFORMAT="Task completed in %3lR"
SRC_FILES="./gaunit ./tests setup.py"
FORMAT_FILES="./gaunit ./tests setup.py ./examples"
PACKAGE="gaunit"

##### Dev

docs() {  ## Build html documentation
    # TODO
    #$(MAKE) -C docs
	echo "docs"
}

pip-comp() { ## Compile requirements files
	pip-compile requirements/base.in
	pip-compile requirements/dev.in
	pip-compile requirements/samples.in
}

pip-up() {  ## Update requirements files
	pip-compile --upgrade --resolver=backtracking requirements/base.in
	pip-compile --upgrade --resolver=backtracking requirements/dev.in
	pip-compile --upgrade --resolver=backtracking requirements/samples.in
}

install-dev() {  ## * Install dev requirements
	pip install -e .
	pip install -r requirements/dev.txt
	npm install -g conventional-changelog-cli
}

install-examples() {  ## Install examples requirements
	pip install -e .
	pip install -r requirements/samples.txt
}

clean-logs() {  ## Remove all log & RF report files
	rm *.log log.html output.xml report.html || true
}

tests() {  ## * Run all tests
    test-unit
    test-cli 
    test-lint
    test-format
    test-package 
}

test-format() {  ## Run code formatting tests
	black --check --diff $FORMAT_FILES
}

test-lint() {  ## Run code linting tests
	pylint --errors-only $SRC_FILES
}

test-unit() {  ## Run unit tests (with coverage run)
	coverage run -m unittest discover tests
}

test-cli() {  ## Run tests on gaunit command
	ga --version
	ga check tests/test_cli_mock.har home_engie -t tests/tracking_plan.json
	ga check tests/test_cli_mock.har home_engie -t tests/tracking_plan.json | grep "OK: all expected events found"  # test for https://github.com/VinceCabs/GAUnit/issues/3
	ga check tests/test_cli_mock.har home_engie -t tests/tracking_plan.json --all
	ga extract tests/test_cli_mock.har -f dp | grep "[{'dp': 'A'}, {'dp': 'B'}, {'dp': 'C'}, {'dp': 'X'}]"
}
	
test-unit-v() {  ## Run unit tests (verbose)
	coverage run -m unittest discover tests -v
}

test-package() {  ## Test that package can be uploaded to pypi
	twine check dist/$PACKAGE-$(version).tar.gz
}

format() {  ## * Format code
	black $FORMAT_FILES
}

##### Use & Deploy

install-minimal() {  ## Install minimal usage requirements
	pip install --upgrade gaunit
}

build-package() {  ## Build a python package ready to upload to pypi
	python setup.py sdist bdist_wheel
}

push-package() {  ## * Build, test and push python packages to pypi
	test-package
    python -m twine upload --skip-existing dist/$PACKAGE-*.tar.gz
}

changelog() {  ## updates CHANGELOG.md
	conventional-changelog ---preset angular --infile CHANGELOG.md --same-file
}

release() {  ## * Test, create a release tag and push it to repos (origin)
    tests
    TAG=v$(version)
	# create tag
	echo "=== Creating tag $TAG"
	git tag -d v$(version) || true
	git tag v$TAG
	# push tag
	echo "=== Pushing tag $TAG to origin"
	git push origin
	git push origin :$(TAG) || true
	git push origin $(TAG)
}

###### Additional commands

version() {  ## Print the current tutor version
	python -c "import io, os; about = {}; exec(io.open(os.path.join('$PACKAGE', '__about__.py'), 'rt', encoding='utf-8').read(), about); print(about['__version__'])"
}

help() {
    echo "$0 <task> <args>"
    echo "Tasks:"
    compgen -A function | grep -v "^_" | cat -n
}

default() {
    help
}

"${@:-default}"