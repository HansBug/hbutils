.PHONY: docs test unittest tbuild

PROJ_DIR := ${CURDIR}

DOC_DIR    := ${PROJ_DIR}/docs
TEST_DIR   := ${PROJ_DIR}/test
SRC_DIR    := ${PROJ_DIR}/hbutils
DIST_DIR   := ${PROJ_DIR}/dist
TBUILD_DIR := ${PROJ_DIR}/tbuild

RANGE_DIR      ?= .
RANGE_TEST_DIR := ${TEST_DIR}/${RANGE_DIR}
RANGE_SRC_DIR  := ${SRC_DIR}/${RANGE_DIR}

COV_TYPES ?= xml term-missing

test: unittest

unittest:
	pytest "${RANGE_TEST_DIR}" \
		-sv -m unittest \
		$(shell for type in ${COV_TYPES}; do echo "--cov-report=$$type"; done) \
		--cov="${RANGE_SRC_DIR}" \
		$(if ${MIN_COVERAGE},--cov-fail-under=${MIN_COVERAGE},) \
		$(if ${WORKERS},-n ${WORKERS},)

docs:
	$(MAKE) -C "${DOC_DIR}" build
pdocs:
	$(MAKE) -C "${DOC_DIR}" prod
docs_auto:
	python remake_docs_via_llm.py -i "${RANGE_SRC_DIR}"

tbuild:
	pyinstaller -D -F -n git_raw -c ${TBUILD_DIR}/git_raw.py
	pyinstaller -D -F -n git_lfs -c ${TBUILD_DIR}/git_lfs.py
clean:
	rm -rf ${DIST_DIR} *.egg-info hbutils.spec
