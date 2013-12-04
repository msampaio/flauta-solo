PYTHON_FILES = $(wildcard *.py)
VERSION = 0.1
DIR = contour-module-$(VERSION)
SRC_DIR = analysis
TEST_DIR = tests

.PHONY: doc tests

check:
	pep8 *.py $(SRC_DIR)/*.py $(TEST_DIR)/*.py

clean:
	rm -f *.pyc *~
	rm -f $(SRC_DIR)/*~
	rm -f $(SRC_DIR)/*.pyc
	rm -f $(TEST_DIR)/*~
	rm -f $(TEST_DIR)/*.pyc

tests:
	python -m unittest discover -p 'test_*.py'
