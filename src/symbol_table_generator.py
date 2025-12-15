import sys
from .tokenizer_analyzer import SwiftLangAnalyzer, Token, RESERVED_WORDS


#  Simple hash table (separate chaining)
class HashTable:
    def __init__(self, size=101):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, payload):
        h = self._hash(key)
        for i, (k, _) in enumerate(self.buckets[h]):
            if k == key:
                self.buckets[h][i] = (key, payload)
                return
        self.buckets[h].append((key, payload))

    def get(self, key):
        h = self._hash(key)
        for k, p in self.buckets[h]:
            if k == key:
                return p
        return None

    def entries(self):
        """Return list of (name, payload) in alphabetical order."""
        all_entries = [item for bucket in self.buckets for item in bucket]
        return sorted(all_entries, key=lambda x: x[0])


#  Symbol table wrapper
class SymbolTable:
    def __init__(self):
        self.ht = HashTable()

    def declare(self, name, typ, value):
        """Insert a freshly declared variable."""
        self.ht.insert(name, {'type': typ, 'value': value})

    def assign(self, name, typ, value):
        """Update an existing variable (warn if it never existed)."""
        if self.ht.get(name) is None:
            print(f"[WARN] Assigning to undeclared variable '{name}' - treating as declaration.")
        self.ht.insert(name, {'type': typ, 'value': value})

    def print_state(self, title):
        print("\n" + "=" * 60)
        print(title)
        print("=" * 60)
        entries = self.ht.entries()
        if not entries:
            print("  <no variables>")
            return
        for name, info in entries:
            print(f"  {name} : {info['type']} = {repr(info['value'])}")
        print()


# Helper
def literal_to_type_value(tok: Token):
    """Infer a basic type/value from a literal token."""
    if tok.kind == 'INTEGER':
        return 'integer', int(tok.value)
    if tok.kind == 'FLOAT':
        return 'float', float(tok.value)
    if tok.kind == 'STRING':
        return 'string', eval(tok.value)
    if tok.kind == 'BOOLEAN':
        return 'boolean', tok.value == 'true'
    if tok.kind == 'NULL':
        return 'null', None
    # Handle arrays and objects
    if tok.value == '[':
        return 'array', '<array literal>'
    if tok.value == '{':
        return 'object', '<object literal>'
    # Fallback: unknown expression
    return 'unknown', '<expression>'


# Parser
class SymbolTableBuilder:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.st = SymbolTable()

    def _current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _advance(self):
        self.pos += 1

    def _parse_expression_until_semicolon(self):
        """Collects tokens until the next ';' to form an expression summary."""
        expr_tokens = []
        while self._current() and not (self._current().kind == 'OPERATOR' and self._current().value == ';'):
            expr_tokens.append(self._current())
            self._advance()
        if expr_tokens:
            first_tok = expr_tokens[0]
            typ, val = literal_to_type_value(first_tok)
            return typ, val
        return 'unknown', '<empty>'

    def _expect_semicolon(self):
        semi = self._current()
        if not (semi and semi.kind == 'OPERATOR' and semi.value == ';'):
            raise SyntaxError("Expected ';' after expression")
        self._advance()

    def _parse_declaration(self):
        """Parse: let ID = <expr> ;"""
        self._advance()  # skip 'let'
        id_tok = self._current()
        if not id_tok or id_tok.kind != 'IDENTIFIER' or id_tok.value in RESERVED_WORDS:
            raise SyntaxError("Invalid identifier in declaration")
        name = id_tok.value
        self._advance()

        eq = self._current()
        if not (eq and eq.kind == 'OPERATOR' and eq.value == '='):
            raise SyntaxError("Expected '=' after identifier")
        self._advance()

        typ, val = self._parse_expression_until_semicolon()
        self.st.declare(name, typ, val)
        self._expect_semicolon()

    def _parse_assignment(self):
        """Parse: ID = <expr> ;"""
        id_tok = self._current()
        if not id_tok or id_tok.kind != 'IDENTIFIER' or id_tok.value in RESERVED_WORDS:
            raise SyntaxError("Invalid identifier in assignment")
        name = id_tok.value
        self._advance()

        eq = self._current()
        if not (eq and eq.kind == 'OPERATOR' and eq.value == '='):
            raise SyntaxError("Expected '=' after identifier")
        self._advance()

        typ, val = self._parse_expression_until_semicolon()
        self.st.assign(name, typ, val)
        self._expect_semicolon()

    def build(self):
        # FIRST PASS: collect ALL declarations
        while self._current():
            cur = self._current()
            if cur.kind == 'IDENTIFIER' and cur.value == 'let':
                try:
                    self._parse_declaration()
                except Exception as e:
                    print(f"[WARN] Skipping malformed declaration at pos {self.pos}: {e}")
                    self._advance()
            else:
                self._advance()

        self.st.print_state("INITIAL STATE OF SYMBOL TABLE")

        # SECOND PASS: process assignments
        self.pos = 0
        while self._current():
            cur = self._current()
            if cur.kind == 'IDENTIFIER' and cur.value not in RESERVED_WORDS:
                # peek ahead for '='
                if (self.pos + 1 < len(self.tokens) and
                    self.tokens[self.pos + 1].kind == 'OPERATOR' and
                    self.tokens[self.pos + 1].value == '='):
                    try:
                        self._parse_assignment()
                    except Exception as e:
                        print(f"[WARN] Skipping malformed assignment at pos {self.pos}: {e}")
                        self._advance()
                else:
                    self._advance()
            else:
                self._advance()

        self.st.print_state("UPDATED STATE OF SYMBOL TABLE")


#  Main driver
def main():
    if len(sys.argv) > 1:
        src_path = sys.argv[1]
    else:
        src_path = 'inputCase2.sl'

    with open(src_path, 'r', encoding='utf-8') as f:
        source = f.read()

    analyzer = SwiftLangAnalyzer()
    analyzer.analyze(source)
    tokens = analyzer.get_tokens()

    builder = SymbolTableBuilder(tokens)
    builder.build()


if __name__ == '__main__':
    main()
