FLIT ?= flit
JAVA ?= java
CURL ?= curl
PYTHON ?= python

PYTEST=pytest

ANTLR_VERSION=4.13.2
ANTLR_JAR=antlr-$(ANTLR_VERSION)-complete.jar
ANTLR_TOOL=$(JAVA) -jar $(ANTLR_JAR)

GRAMMAR_DIR=antlr
OUTPUT_DIR=src/friendlydateparser
GRAMMAR=FriendlyDate

GENERATED= \
	$(OUTPUT_DIR)/$(GRAMMAR_DIR)/$(GRAMMAR)Visitor.py \
	$(OUTPUT_DIR)/$(GRAMMAR_DIR)/$(GRAMMAR)Lexer.py \
	$(OUTPUT_DIR)/$(GRAMMAR_DIR)/$(GRAMMAR)Parser.py \
	$(OUTPUT_DIR)/$(GRAMMAR_DIR)/$(GRAMMAR).tokens \
	$(OUTPUT_DIR)/$(GRAMMAR_DIR)$(GRAMMAR).interp

$(GENERATED): $(GRAMMAR_DIR)/$(GRAMMAR).g4 $(ANTLR_JAR)
	mkdir -p $(OUTPUT_DIR)
	$(ANTLR_TOOL) -Dlanguage=Python3 -o $(OUTPUT_DIR) $(GRAMMAR_DIR)/$(GRAMMAR).g4 -visitor

$(ANTLR_JAR):
	$(CURL) -O https://www.antlr.org/download/$(ANTLR_JAR)

antlr: $(GENERATED)

dist-clean:
	rm -rf dist/ build/ *.egg-info $(GENERATED) ve/ test-ve/

build: antlr
	$(FLIT) build

install: antlr
	$(FLIT) install

test: antlr
	$(PYTEST)

publish: test build
	$(FLIT) publish

ve:
	rm -Rf ve
	$(PYTHON) -m venv ve
	(. ve/bin/activate; pip install antlr4-python3-runtime==$(ANTLR_VERSION) pytest python-dateutil)

test-wheel: build
	./test-wheel.sh
