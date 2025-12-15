import sys
import io
import contextlib
import os
import pytest

from src import main as swift_main


def run_main_with_argv(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        with pytest.raises(SystemExit) as excinfo:
            sys.argv = argv
            swift_main.main()
    return excinfo.value.code, buf.getvalue()


def test_main_no_arguments_prints_usage_and_exits():
    code, output = run_main_with_argv(["main.py"])
    assert code == 1
    assert "No source file provided" in output
    assert "Usage: python main.py <source_file.sl>" in output


def test_main_file_not_found_exits_with_error(tmp_path):
    missing = tmp_path / "missing.sl"
    code, output = run_main_with_argv(["main.py", str(missing)])
    assert code == 1
    assert "not found" in output


def test_main_runs_valid_program_successfully(tmp_path):
    program = """\
let x = 1;
print(x);
"""
    path = tmp_path / "test.sl"
    path.write_text(program, encoding="utf-8")

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        old_argv = sys.argv[:]
        try:
            sys.argv = ["main.py", str(path)]
            swift_main.main()
        finally:
            sys.argv = old_argv

    output = buf.getvalue()
    assert "Running SwiftLang program" in output
    assert "Program finished successfully." in output
    # Program should have printed 1 on its own line
    assert "1" in output.splitlines()
