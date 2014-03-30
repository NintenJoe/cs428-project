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

UML_OUTPUT = dot

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

# Default output is `dot` file, which is automatically converted to a `graphml`
# file.
#
# Override the output type by passing in a desired image format. For example,
#
# 	make UML_IMG_TYPE=png uml
#
# which will produce a classes_Zol.png and packages_Zol.png file.
uml :
ifndef IMG_TYPE
	pyreverse $(SRC_DIR) --output=dot --filter-mode=PUB_ONLY --ignore=$(DOC_DIR) --ignore=$(TEST_DIR) --ignore=$(TOOL_DIR) --project=$(PROJECT_NAME)
	python $(TOOL_DIR)/dottoxml/dottoxml.py ./classes_$(PROJECT_NAME).dot ./classes_$(PROJECT_NAME).graphml
	python $(TOOL_DIR)/dottoxml/dottoxml.py ./packages_$(PROJECT_NAME).dot ./packages_$(PROJECT_NAME).graphml
else
	pyreverse $(SRC_DIR) --output=$(IMG_TYPE) --filter-mode=PUB_ONLY --ignore=$(DOC_DIR) --ignore=$(TEST_DIR) --ignore=$(TOOL_DIR) --project=$(PROJECT_NAME)
endif

clean :
	-rm -rf $(SRC_DIR)/*.pyc $(LIB_DIR)/*.pyc $(TEST_DIR)/*.pyc ./classes_$(PROJECT_NAME).* ./packages_$(PROJECT_NAME).*
