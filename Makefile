ANTLR=antlr4
FLIT=flit
PYTEST=pytest

GRAMMAR_DIR=antlr
OUTPUT_DIR=src/friendlydateparser
GRAMMAR=FriendlyDate

GENERATED= \
	$(OUTPUT_DIR)/$(GRAMMAR_DIR)/$(GRAMMAR)Visitor.py \
	$(OUTPUT_DIR)/$(GRAMMAR_DIR)/$(GRAMMAR)Lexer.py \
	$(OUTPUT_DIR)/$(GRAMMAR_DIR)/$(GRAMMAR)Parser.py \
	$(OUTPUT_DIR)/$(GRAMMAR_DIR)/$(GRAMMAR).tokens \
	$(OUTPUT_DIR)/$(GRAMMAR_DIR)$(GRAMMAR).interp

$(GENERATED): $(GRAMMAR_DIR)/$(GRAMMAR).g4
	mkdir -p $(OUTPUT_DIR)
	$(ANTLR) -Dlanguage=Python3 -o $(OUTPUT_DIR) $(GRAMMAR_DIR)/$(GRAMMAR).g4 -visitor

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
