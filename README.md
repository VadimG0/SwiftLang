# SwiftLang

SwiftLang is a small, educational, Swift-inspired language implemented in Python.  
It includes:

- A tokenizer / lexical analyzer  
- A hand-written recursive-descent parser  
- A simple semantic analyzer with a symbol table  
- A tree-walking interpreter  
- A separate symbol-table generator tool  
- Example `.sl` programs that exercise the language  
- A pytest-based unit test suite in `tests/`

The goal of the project is to demonstrate the classic compiler / interpreter pipeline on a compact, readable codebase.

---

## Project Structure

```text
SwiftLang/
  src/
    __init__.py
    tokenizer_analyzer.py
    parser.py
    semantic_analyzer.py
    interpreter.py
    symbol_table_generator.py
    main.py
  examples/
    inputCase3.sl
    inputCase4.sl
    currentlyImplemented.sl
    notWorking.sl
  tests/
    test_*.py           # pytest unit tests for tokenizer, parser, semantics, interpreter, CLI, etc.
```

- `tokenizer_analyzer.py` – turns source code into tokens and collects statistics.  
- `parser.py` – builds an abstract syntax tree (AST) for statements and expressions.  
- `semantic_analyzer.py` – performs simple semantic checks and builds a symbol table.  
- `interpreter.py` – executes the AST using the symbol table as runtime environment.  
- `symbol_table_generator.py` – standalone script to tokenize a file and build/print a symbol table.  
- `main.py` – command-line driver that runs a `.sl` program end-to-end.  
- `examples/` – sample programs in SwiftLang.  
- `tests/` – pytest-based unit tests that exercise all major components of the language pipeline.

For the full language tutorial and keyword reference, see the separate documents:

- `Language_Tutorial.pdf` – step-by-step introduction with a worked example and an exercise.  
- `Language_Reference_Manual.pdf` – list of keywords and syntax rules.

---

## Requirements

- **Python**: 3.8 or newer  
- No non-standard runtime dependencies for the language itself (only standard library).  
- For testing, you’ll want **pytest** installed.

---

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/VadimG0/SwiftLang.git
   cd SwiftLang
   ```

2. *(Optional but recommended)* **Create and activate a virtual environment**

   **macOS / Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows (PowerShell):**
   ```bash
   py -m venv .venv
   .\.venv\Scripts\Activate
   ```

3. **Install dev dependencies (for tests)**

   If you just want pytest:

   ```bash
   pip install pytest
   ```


---

## Running SwiftLang Programs

The main entry point is `src/main.py`. The easiest way to run it is as a module from the project root so that the `src` package imports work cleanly:

```bash
# From the SwiftLang repo root
python -m src.main examples/inputCase4.sl
```

You should see output similar to:

```text
Running SwiftLang program: examples/inputCase4.sl
--------------------------------------------------
true
true
true
true
--------------------------------------------------
Program finished successfully.
```

### General usage

```bash
python -m src.main path/to/your_program.sl
```

The driver will:

1. Tokenize the source  
2. Parse it into an AST  
3. Run semantic analysis  
4. Interpret the program and print any `print(...)` results to stdout  

If there are errors at any stage, the driver prints a friendly message like **“Syntax Error:”**, **“Semantic Error:”**, or **“Runtime Error:”** and exits with a non-zero status code.

---

## Running the Test Suite (pytest)

With the `tests/` directory in place, you can run all tests from the project root:

```bash
pytest
```

Or run a single test file:

```bash
pytest tests/test_interpreter.py
```

The tests are organized to cover:

- Tokenization (identifiers, literals, operators, reserved words)  
- Parsing of declarations, assignments, expressions, `if`/`else`, and `while` loops  
- Semantic checks (duplicate declarations, undeclared variables, boolean conditions)  
- Interpreter behavior (arithmetic, control flow, boolean logic)  
- The symbol table generator helper  
- The command-line interface in `src/main.py` (usage, missing file, successful run)  


## Documentation
[Language Tutorial](docs/SwiftLang_Language_Tutorial.pdf)

---

