.DEFAULT_GOAL := html
.PHONY: help


html:
	sphinx-build -b html -a -E "." "build/html"

open:
	chrome build/html/index.html
