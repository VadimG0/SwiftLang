import pytest

from src.tokenizer_analyzer import SwiftLangAnalyzer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer, SemanticError


def build_ast(source: str):
    analyzer = SwiftLangAnalyzer()
    analyzer.analyze(source)
    tokens = analyzer.get_tokens()
    parser = Parser(tokens)
    return parser.parse_program()


def test_semantic_dynamic_typing_updates_type_on_assignment():
    source = "let x = 1; x = 2.5;"
    ast = build_ast(source)
    sem = SemanticAnalyzer()
    symbol_table = sem.analyze(ast)
    assert "x" in symbol_table
    assert symbol_table["x"]["type"] == "float"


def test_semantic_duplicate_declaration_raises():
    source = "let x = 1; let x = 2;"
    ast = build_ast(source)
    sem = SemanticAnalyzer()
    with pytest.raises(SemanticError) as excinfo:
        sem.analyze(ast)
    assert "Duplicate declaration: x" in str(excinfo.value)


def test_semantic_undeclared_variable_assignment_raises():
    source = "x = 1;"
    ast = build_ast(source)
    sem = SemanticAnalyzer()
    with pytest.raises(SemanticError) as excinfo:
        sem.analyze(ast)
    assert "Undeclared variable: x" in str(excinfo.value)


def test_semantic_if_condition_must_be_boolean():
    source = "let x = 1; if (x) { print(x); }"
    ast = build_ast(source)
    sem = SemanticAnalyzer()
    with pytest.raises(SemanticError) as excinfo:
        sem.analyze(ast)
    assert "Condition must be boolean" in str(excinfo.value)
