# [0.4.0](https://github.com/engie-b2c-perf/ga-unit/compare/v0.3.3...v0.4.0) (2021-02-11)


### Bug Fixes

* **examples:** 🐛 add missing '.har' extension ([17f75ef](https://github.com/engie-b2c-perf/ga-unit/commit/17f75ef401f73545839357ff7244eda094cd73d4))


### Features

* ✨ add custom GAUnit exceptions ([50d9291](https://github.com/engie-b2c-perf/ga-unit/commit/50d9291b2c1ad596725c754696eb32ed73fcc341))
* **examples:** add full GA4 example ([be9f432](https://github.com/engie-b2c-perf/ga-unit/commit/be9f4320cb801ec56e3cf04c16b809205a2360af))



## [0.3.3](https://github.com/engie-b2c-perf/ga-unit/compare/v0.3.2...v0.3.3) (2021-02-02)


### Features

* **examples:** add manual browsing session sample ([fcbc686](https://github.com/engie-b2c-perf/ga-unit/commit/fcbc6862ccf53b089884afd6dc8be467e5b98ae0))
* **cli:** add description to shell commands



## [0.3.2](https://github.com/engie-b2c-perf/ga-unit/compare/v0.3.1...v0.3.2) (2021-01-25)


### Features

* **models:** add export tracking plan to JSON method: `TrackingPlan.to json()`
* **docs:** add more examples in docstrings

### Bug Fixes

* **models:** fix `TrackingPlan.from_events()` method

### BREAKING CHANGES

* **models:** remove `expected_events=` parameter in `TrackingPlan` constructor
* **api:** adapt api to change above



## [0.3.1](https://github.com/engie-b2c-perf/ga-unit/compare/v0.3.0...v0.3.1) (2021-01-08)

### Features

* **examples:** add import tracking plan from gsheet
* **examples:** all samples rely on enhanced e-commerce demo website

### BREAKING CHANGES

* **models:** simplify `TrackingPlan()` constructor
* **models:** add `TrackingPlan.add_test_case()` alias method to add or update test cases
* **models:** add `TestCase.was_succesful()` method
* require Python 3.7+



## [0.3.0](https://github.com/engie-b2c-perf/ga-unit/compare/v0.2.1...v0.3.0) (2021-01-05)

### Features

* **models:** accept numbers in tracking plan
* **cli:** new `gaextract`command

### Bug Fixes

* **models:** process events parameters to manage numbers and URL encoding

### BREAKING CHANGES

* **models:** add `TrackingPlan` class for more import capabilities
* **cli:** much better cli ( output, arguments, exit code, etc.)