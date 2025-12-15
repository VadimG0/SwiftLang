import pytest

from src.tokenizer_analyzer import SwiftLangAnalyzer, RESERVED_WORDS


def test_tokenizer_basic_tokens():
    source = "let x = 42; // comment\nprint(x);"
    analyzer = SwiftLangAnalyzer()
    analyzer.analyze(source)
    tokens = analyzer.get_tokens()

    kinds_values = [(t.kind, t.value) for t in tokens]
    assert kinds_values == [
        ("IDENTIFIER", "let"),
        ("IDENTIFIER", "x"),
        ("OPERATOR", "="),
        ("INTEGER", "42"),
        ("OPERATOR", ";"),
        ("IDENTIFIER", "print"),
        ("OPERATOR", "("),
        ("IDENTIFIER", "x"),
        ("OPERATOR", ")"),
        ("OPERATOR", ";"),
    ]


def test_tokenizer_tracks_variables_and_reserved_words():
    source = "let a = 1;\nlet b = 2;\nprint(a + b);"
    analyzer = SwiftLangAnalyzer()
    analyzer.analyze(source)

    # Literals collected
    assert analyzer.literals == ["1", "2"]

    # Variables are sorted and do NOT include reserved words like 'print' or 'let'
    assert analyzer.variables == ["a", "b"]
    assert "let" in analyzer.reserved
    assert "print" in analyzer.reserved

    # Declaration counts
    assert dict(analyzer.var_declared) == {"a": 1, "b": 1}

    # Sanity check: some known reserved words
    for word in ["if", "else", "while", "let", "print", "true", "false", "null"]:
        assert word in RESERVED_WORDS
