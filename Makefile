INTERPRETER = python
INTERPRETER_FLAGS = 
TEST_FLAGS = -m unittest

SRC_DIR = ./src
LIB_DIR = ./lib
TEST_DIR = ./test
MAIN_SCRIPT = $(SRC_DIR)/main.py

.PHONY : clean

all : tests

main : $(MAIN_SCRIPT) $(wildcard $(SRC_DIR)/*.py) $(wildcard $(LIB_DIR)/*.py)
	$(INTERPRETER) $(INTERPRETER_FLAGS) $(MAIN_SCRIPT)

tests : $(wildcard $(SRC_DIR)/*.py) $(wildcard $(TEST_DIR)/*.py)
	$(INTERPRETER) $(TEST_FLAGS) discover -s $(TEST_DIR) -p '*Tests.py'

%Tests : $(TEST_DIR)/%Tests.py $(SRC_DIR)/%.py
	$(INTERPRETER) $(TEST_FLAGS) discover -s $(TEST_DIR) -p '$@.py'

clean :
	-rm -rf $(SRC_DIR)/*.pyc $(LIB_DIR)/*.pyc $(TEST_DIR)/*.pyc
