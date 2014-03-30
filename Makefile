PROJECT_NAME = Zol
INTERPRETER = python
INTERPRETER_FLAGS = 
TEST_FLAGS = -m unittest

COVERAGER = coverage
COVERAGER_FLAGS = run -m unittest discover -s $(TEST_DIR) -p '*Tests.py'

SRC_DIR = ./src
TEST_DIR = ./test
TOOL_DIR = ./tool
DOC_DIR = ./doc
MAIN_SCRIPT = $(SRC_DIR)/main.py

UML_DIAG_FILETYPE = dot

.PHONY : clean main tests coverage

all : tests

main : $(MAIN_SCRIPT) $(wildcard $(SRC_DIR)/*.py) $(wildcard $(LIB_DIR)/*.py)
	$(INTERPRETER) $(INTERPRETER_FLAGS) $(MAIN_SCRIPT)

tests : $(wildcard $(SRC_DIR)/*.py) $(wildcard $(TEST_DIR)/*.py)
	$(INTERPRETER) $(TEST_FLAGS) discover -s $(TEST_DIR) -p '*Tests.py'

coverage :
	$(COVERAGER) $(COVERAGER_FLAGS)

%Tests : $(TEST_DIR)/%Tests.py $(SRC_DIR)/%.py
	$(INTERPRETER) $(TEST_FLAGS) discover -s $(TEST_DIR) -p '$@.py'

# --output: run `dot -Txxx` to see the list of supported image types. 
# 			Common types include: bmp, dot, eps, png, svg
uml :
	pyreverse $(SRC_DIR) --output=$(UML_DIAG_FILETYPE) --filter-mode=PUB_ONLY --ignore=$(DOC_DIR) --ignore=$(TEST_DIR) --ignore=$(TOOL_DIR) --project=$(PROJECT_NAME)
ifeq ($(UML_DIAG_FILETYPE),dot)
	python $(TOOL_DIR)/dottoxml/dottoxml.py ./classes_$(PROJECT_NAME).$(UML_DIAG_FILETYPE) ./classes_$(PROJECT_NAME).graphml
endif

clean :
	-rm -rf $(SRC_DIR)/*.pyc $(LIB_DIR)/*.pyc $(TEST_DIR)/*.pyc ./classes_$(PROJECT_NAME).* ./packages_$(PROJECT_NAME).*
