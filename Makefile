FLIT=flit
PYTEST=pytest
JAVA ?= java

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

$(ANTLR_JAR):
	curl -O https://www.antlr.org/download/$(ANTLR_JAR)

$(GENERATED): $(GRAMMAR_DIR)/$(GRAMMAR).g4 $(ANTLR_JAR)
	mkdir -p $(OUTPUT_DIR)
	$(ANTLR_TOOL) -Dlanguage=Python3 -o $(OUTPUT_DIR) $(GRAMMAR_DIR)/$(GRAMMAR).g4 -visitor

antlr: $(GENERATED)

clean:
	 rm -f $(GENERATED)

dist-clean: clean
	rm -rf dist/ build/ *.egg-info

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
	python -m venv ve
	(. ve/bin/activate; pip install antlr4-python3-runtime==$(ANTLR_VERSION))


test-wheel: build
	./test-wheel.sh
