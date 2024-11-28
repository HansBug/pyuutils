.PHONY: docs test unittest build clean benchmark zip

PYTHON := $(shell which python)

PROJ_DIR      := .
DIST_DIR      := ${PROJ_DIR}/dist

build:
	$(PYTHON) setup.py build_ext --inplace
clean:
	rm -rf $(shell find ${SRC_DIR} -name '*.so')
	rm -rf ${DIST_DIR} ${WHEELHOUSE_DIR}

package:
	$(PYTHON) -m build --sdist --wheel --outdir ${DIST_DIR}
