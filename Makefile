.PHONY: docs test unittest build clean benchmark zip bin_test bin_build bin_clean bin bin_install

PYTHON := $(shell which python)

PROJ_DIR       := .
DOC_DIR        := ${PROJ_DIR}/docs
DIST_DIR       := ${PROJ_DIR}/dist
WHEELHOUSE_DIR := ${PROJ_DIR}/wheelhouse
TEST_DIR       := ${PROJ_DIR}/test
BENCHMARK_DIR  := ${PROJ_DIR}/benchmark
SRC_DIR        := ${PROJ_DIR}/pyuutils
RUNS_DIR       := ${PROJ_DIR}/runs
BUILD_DIR      := ${PROJ_DIR}/build
BINSTALL_DIR   := ${PROJ_DIR}/bin_install

RANGE_DIR       ?= .
RANGE_TEST_DIR  := ${TEST_DIR}/${RANGE_DIR}
RANGE_BENCH_DIR := ${BENCHMARK_DIR}/${RANGE_DIR}
RANGE_SRC_DIR   := ${SRC_DIR}/${RANGE_DIR}

build:
	BINSTALL_DIR="${BINSTALL_DIR}" $(PYTHON) setup.py build_ext --inplace
clean:
	rm -rf $(shell find ${SRC_DIR} -name '*.so')
	rm -rf ${DIST_DIR} ${WHEELHOUSE_DIR}

package:
	BINSTALL_DIR="${BINSTALL_DIR}" $(PYTHON) -m build --sdist --wheel --outdir ${DIST_DIR}

unittest:
	$(PYTHON) -m pytest "${RANGE_TEST_DIR}" \
		-sv -m unittest \
		$(shell for type in ${COV_TYPES}; do echo "--cov-report=$$type"; done) \
		--cov="${RANGE_SRC_DIR}" \
		$(if ${MIN_COVERAGE},--cov-fail-under=${MIN_COVERAGE},) \
		$(if ${WORKERS},-n ${WORKERS},)

bin_build:
	cmake -S UUtils -B ${BUILD_DIR}
	cmake --build ${BUILD_DIR}
bin_test:
	ctest --test-dir ${BUILD_DIR} --output-on-failure -C Release
bin_install:
	cmake --install build --prefix "${BINSTALL_DIR}"
bin_clean:
	rm -rf ${BUILD_DIR} ${BINSTALL_DIR}
bin: bin_build bin_test bin_install
