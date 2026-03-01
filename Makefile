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

#PYTHON_CODE_DIR   := ${SRC_DIR}/${RANGE_DIR}
#RST_DOC_DIR       := ${DOC_DIR}/source/api_doc/${RANGE_DIR}
PYTHON_CODE_DIR   := ${SRC_DIR}
RST_DOC_DIR       := ${DOC_DIR}/source/api_doc
PYTHON_CODE_FILES := $(shell find ${PYTHON_CODE_DIR} -name "*.py" ! -name "__*.py" 2>/dev/null)
RST_DOC_FILES     := $(patsubst ${PYTHON_CODE_DIR}/%.py,${RST_DOC_DIR}/%.rst,${PYTHON_CODE_FILES})
PYTHON_NONM_FILES := $(shell find ${PYTHON_CODE_DIR} -name "__init__.py" 2>/dev/null)
RST_NONM_FILES    := $(foreach file,${PYTHON_NONM_FILES},$(patsubst %/__init__.py,%/index.rst,$(patsubst ${PYTHON_CODE_DIR}/%,${RST_DOC_DIR}/%,$(patsubst ${PYTHON_CODE_DIR}/__init__.py,${RST_DOC_DIR}/index.rst,${file}))))

AUTO_OPTIONS ?= --param max_tokens=400000 --no-ignore-module hbutils --model-name gpt-5.2-codex

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
	python -m hbllmutils code pydoc -i "${RANGE_SRC_DIR}" ${AUTO_OPTIONS}
todos_auto:
	python -m hbllmutils code todo -i "${RANGE_SRC_DIR}" ${AUTO_OPTIONS}
tests_auto:
	python -m hbllmutils code unittest -i "${RANGE_SRC_DIR}" -o "${RANGE_SRC_DIR_TEST}" \
		${AUTO_OPTIONS}
rst_auto: ${RST_DOC_FILES} ${RST_NONM_FILES} auto_rst_top_index.py
	python auto_rst_top_index.py -i ${PYTHON_CODE_DIR} -o ${DOC_DIR}/source/api_doc.rst
${RST_DOC_DIR}/%.rst: ${PYTHON_CODE_DIR}/%.py auto_rst.py Makefile
	@mkdir -p $(dir $@)
	python auto_rst.py -i $< -o $@
${RST_DOC_DIR}/%/index.rst: ${PYTHON_CODE_DIR}/%/__init__.py auto_rst.py Makefile
	@mkdir -p $(dir $@)
	python auto_rst.py -i $< -o $@
${RST_DOC_DIR}/index.rst: ${PYTHON_CODE_DIR}/__init__.py auto_rst.py Makefile
	@mkdir -p $(dir $@)
	python auto_rst.py -i $< -o $@

tbuild:
	pyinstaller -D -F -n git_raw -c ${TBUILD_DIR}/git_raw.py
	pyinstaller -D -F -n git_lfs -c ${TBUILD_DIR}/git_lfs.py
clean:
	rm -rf ${DIST_DIR} *.egg-info hbutils.spec
