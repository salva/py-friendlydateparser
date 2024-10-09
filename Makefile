ANTLR=antlr4
GRAMMAR_DIR=antlr
OUTPUT_DIR=src/friendlydateparser
GRAMMAR=FriendlyDate

GENERATED=$(OUTPUT_DIR)/$(GRAMMAR_DIR)/$(GRAMMAR)Lexer.py $(OUTPUT_DIR)/$(GRAMMAR_DIR)/$(GRAMMAR)Parser.py

$(GENERATED): $(GRAMMAR_DIR)/$(GRAMMAR).g4
	mkdir -p $(OUTPUT_DIR)
	$(ANTLR) -Dlanguage=Python3 -o $(OUTPUT_DIR) $(GRAMMAR_DIR)/$(GRAMMAR).g4 -visitor

clean:
	rm -rf $(OUTPUT_DIR)/$(GRAMMAR_DIR)
