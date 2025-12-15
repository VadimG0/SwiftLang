import io
import contextlib

from src.tokenizer_analyzer import SwiftLangAnalyzer
from src.symbol_table_generator import SymbolTableBuilder


def test_symbol_table_builder_decl_and_assign():
    source = "let x = 1; y = 2;"
    analyzer = SwiftLangAnalyzer()
    analyzer.analyze(source)
    tokens = analyzer.get_tokens()

    builder = SymbolTableBuilder(tokens)

    # Suppress the pretty-printing to keep test output clean
    with contextlib.redirect_stdout(io.StringIO()):
        builder.build()

    entries = dict(builder.st.ht.entries())

    assert "x" in entries
    assert "y" in entries

    assert entries["x"]["type"] == "integer"
    assert entries["x"]["value"] == 1

    assert entries["y"]["type"] == "integer"
    assert entries["y"]["value"] == 2
