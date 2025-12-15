# src/main.py
import sys
import os
from .parser import Parser, Program
from .interpreter import Interpreter
from .semantic_analyzer import SemanticAnalyzer, SemanticError
from .tokenizer_analyzer import SwiftLangAnalyzer

def print_usage():
    print("Usage: python main.py <source_file.sl>")
    print("Example: python main.py examples/currentlyImplemented.sl")
    print("         python main.py myprogram.sl")

def main():
    if len(sys.argv) != 2:
        print("Error: No source file provided.")
        print_usage()
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    if not filepath.lower().endswith('.sl'):
        print(f"Warning: File '{filepath}' does not have .sl extension (but proceeding anyway)")

    print(f"Running SwiftLang program: {filepath}")
    print("-" * 50)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")
        sys.exit(1)

    # 1. Tokenize
    tokenizer = SwiftLangAnalyzer()
    tokenizer.analyze(source)
    tokens = tokenizer.get_tokens()

    # Optional: Print tokens for debugging
    # for t in tokens:
    #     print(t.kind, t.value)

    # 2. Parse
    try:
        parser = Parser(tokens)
        ast: Program = parser.parse_program()
    except SyntaxError as e:
        print("Syntax Error:")
        print(e)
        sys.exit(1)
    except Exception as e:
        print("Parsing Error:")
        print(e)
        sys.exit(1)

    # 3. Semantic Analysis
    try:
        semantic_analyzer = SemanticAnalyzer()
        symbol_table = semantic_analyzer.analyze(ast)
    except SemanticError as e:
        print("Semantic Error:")
        print(e)
        sys.exit(1)
    except Exception as e:
        print("Semantic Analysis Error:")
        print(e)
        sys.exit(1)

    # 4. Interpret
    try:
        interpreter = Interpreter(symbol_table)
        interpreter.interpret(ast)
    except Exception as e:
        print("Runtime Error:")
        print(e)
        sys.exit(1)

    print("-" * 50)
    print("Program finished successfully.")

if __name__ == '__main__':
    main()