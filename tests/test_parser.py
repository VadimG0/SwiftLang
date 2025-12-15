import pytest

from src.tokenizer_analyzer import SwiftLangAnalyzer
from src.parser import (
    Parser,
    Program,
    DeclStmt,
    AssignStmt,
    BinaryExpr,
    LiteralExpr,
    VarExpr,
    IfStmt,
    WhileStmt,
    BlockStmt,
    PrintStmt,
)


def parse_source(source: str) -> Program:
    analyzer = SwiftLangAnalyzer()
    analyzer.analyze(source)
    tokens = analyzer.get_tokens()
    parser = Parser(tokens)
    ast = parser.parse_program()
    assert isinstance(ast, Program)
    return ast


def test_parse_simple_declaration_and_expression_precedence():
    ast = parse_source("let x = 1 + 2 * 3;")
    assert len(ast.stmts) == 1
    stmt = ast.stmts[0]
    assert isinstance(stmt, DeclStmt)
    expr = stmt.expr
    assert isinstance(expr, BinaryExpr)
    assert expr.op == "+"
    assert isinstance(expr.left, LiteralExpr)
    assert expr.left.value == "1"
    assert isinstance(expr.right, BinaryExpr)
    assert expr.right.op == "*"
    assert isinstance(expr.right.left, LiteralExpr)
    assert expr.right.left.value == "2"
    assert isinstance(expr.right.right, LiteralExpr)
    assert expr.right.right.value == "3"


def test_parse_assignment_statement():
    ast = parse_source("let x = 1; x = 2;")
    assert len(ast.stmts) == 2
    decl, assign = ast.stmts
    assert isinstance(decl, DeclStmt)
    assert isinstance(assign, AssignStmt)
    assert assign.name == "x"
    assert isinstance(assign.expr, LiteralExpr)
    assert assign.expr.value == "2"


def test_parse_if_and_else_with_block():
    source = "let x = 1; if (x < 10) { print(x); } else { print(0); }"
    ast = parse_source(source)
    # decl + if
    assert len(ast.stmts) == 2
    _, if_stmt = ast.stmts
    assert isinstance(if_stmt, IfStmt)
    assert isinstance(if_stmt.cond, BinaryExpr)
    assert isinstance(if_stmt.then_body, BlockStmt)
    assert isinstance(if_stmt.else_body, BlockStmt)

    then_block = if_stmt.then_body
    else_block = if_stmt.else_body

    assert len(then_block.stmts) == 1
    assert isinstance(then_block.stmts[0], PrintStmt)
    assert len(else_block.stmts) == 1
    assert isinstance(else_block.stmts[0], PrintStmt)


def test_parse_while_loop():
    source = "let x = 0; while (x < 3) { x = x + 1; }"
    ast = parse_source(source)
    assert len(ast.stmts) == 2
    _, while_stmt = ast.stmts
    assert isinstance(while_stmt, WhileStmt)
    assert isinstance(while_stmt.cond, BinaryExpr)
    assert while_stmt.cond.op == "<"


def test_parse_invalid_missing_identifier_after_let_raises_syntax_error():
    source = "let = 1;"
    analyzer = SwiftLangAnalyzer()
    analyzer.analyze(source)
    tokens = analyzer.get_tokens()
    parser = Parser(tokens)
    with pytest.raises(SyntaxError):
        parser.parse_program()
