.PHONY: docs test unittest build clean benchmark zip

PYTHON := $(shell which python)

PROJ_DIR       := .
DOC_DIR        := ${PROJ_DIR}/docs
DIST_DIR       := ${PROJ_DIR}/dist
WHEELHOUSE_DIR := ${PROJ_DIR}/wheelhouse
TEST_DIR       := ${PROJ_DIR}/test
BENCHMARK_DIR  := ${PROJ_DIR}/benchmark
SRC_DIR        := ${PROJ_DIR}/pyuutils
RUNS_DIR       := ${PROJ_DIR}/runs

RANGE_DIR       ?= .
RANGE_TEST_DIR  := ${TEST_DIR}/${RANGE_DIR}
RANGE_BENCH_DIR := ${BENCHMARK_DIR}/${RANGE_DIR}
RANGE_SRC_DIR   := ${SRC_DIR}/${RANGE_DIR}

build:
	$(PYTHON) setup.py build_ext --inplace
clean:
	rm -rf $(shell find ${SRC_DIR} -name '*.so')
	rm -rf ${DIST_DIR} ${WHEELHOUSE_DIR}

package:
	$(PYTHON) -m build --sdist --wheel --outdir ${DIST_DIR}

unittest:
	$(PYTHON) -m pytest "${RANGE_TEST_DIR}" \
		-sv -m unittest \
		$(shell for type in ${COV_TYPES}; do echo "--cov-report=$$type"; done) \
		--cov="${RANGE_SRC_DIR}" \
		$(if ${MIN_COVERAGE},--cov-fail-under=${MIN_COVERAGE},) \
		$(if ${WORKERS},-n ${WORKERS},)
