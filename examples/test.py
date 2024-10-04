from antlr4 import *
from friendlydateparser.antlr.FriendlyDateLexer import FriendlyDateLexer
from friendlydateparser.antlr.FriendlyDateParser import FriendlyDateParser

def test_parser(input_text):
    input_stream = InputStream(input_text)
    lexer = FriendlyDateLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = FriendlyDateParser(token_stream)
    
    # Assuming 'dateExpression' is the entry rule in your grammar
    tree = parser.dateExpression()
    
    # Print the parse tree
    print(tree.toStringTree(recog=parser))

if __name__ == "__main__":
    # Test inputs
    inputs = [
        "last sunday",
        "next monday",
        "next friday",
        "last tuesday",
        "next tue",
        "october/3/2017",
        "october/3",
        "3/october/2017",
        "3/october",
        "10/3/2017",
        "10/3",
        "october/2017",
        "10/2017",
        "october",
        "the 3rd of october, 2017",
        "the 3rd of october 2017",
        "the 3rd of october"
    ]

    for input_text in inputs:
        print(f"Testing input: {input_text}")
        test_parser(input_text)
        print()
