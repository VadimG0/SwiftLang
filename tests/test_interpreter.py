import io
import contextlib

from src.tokenizer_analyzer import SwiftLangAnalyzer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.interpreter import Interpreter


def run_program(source: str):
    analyzer = SwiftLangAnalyzer()
    analyzer.analyze(source)
    tokens = analyzer.get_tokens()
    parser = Parser(tokens)
    ast = parser.parse_program()

    semantic = SemanticAnalyzer()
    symbol_table = semantic.analyze(ast)

    interpreter = Interpreter(symbol_table)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        interpreter.interpret(ast)
    return symbol_table, buf.getvalue()


def test_interpreter_arithmetic_and_assignment():
    source = """\
let x = 5;
let y = 10;
let z = 0;
z = x + y * 2;
print(z);
"""
    symtab, output = run_program(source)
    # Values
    assert symtab["x"]["value"] == 5
    assert symtab["y"]["value"] == 10
    assert symtab["z"]["value"] == 25
    # Types (note: z becomes 'number' due to BinaryExpr inference)
    assert symtab["x"]["type"] == "integer"
    assert symtab["y"]["type"] == "integer"
    assert symtab["z"]["type"] == "number"
    # Printed output
    assert output.strip().splitlines() == ["25"]


def test_interpreter_if_else_and_boolean_literals():
    source = """\
let flag = true;
if (flag) {
    print(1);
} else {
    print(0);
}
"""
    symtab, output = run_program(source)
    assert symtab["flag"]["type"] == "boolean"
    assert symtab["flag"]["value"] is True
    assert output.strip().splitlines() == ["1"]


def test_interpreter_while_loop_executes_until_condition_false():
    source = """\
let x = 0;
while (x < 3) {
    print(x);
    x = x + 1;
}
"""
    symtab, output = run_program(source)
    # x should end at 3 and be numeric
    assert symtab["x"]["type"] == "number"
    assert symtab["x"]["value"] == 3
    assert output.strip().splitlines() == ["0", "1", "2"]
