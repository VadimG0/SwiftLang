import re
from collections import Counter, defaultdict

# === SwiftLang Language Definition ===
RESERVED_WORDS = {
    'if', 'else', 'switch', 'case', 'default', 'while', 'do', 'for', 'in',
    'break', 'continue', 'return', 'let', 'fun', 'try', 'catch',
    'throw', 'thread', 'spawn', 'join', 'lock', 'unlock', 'print', 'read',
    'true', 'false', 'null'
}

OPERATORS = {
    '+', '-', '*', '/', '%', '**', '==', '!=', '<', '>', '<=', '>=',
    'and', 'or', 'not', '=', '(', ')', '{', '}', '[', ']', ',', ':', '.', ';'
}

TOKEN_SPEC = [
    ('COMMENT_BLOCK', r'/\*[\s\S]*?\*/'),
    ('COMMENT_LINE',  r'//.*'),
    ('STRING',        r'"(?:\\.|[^"\\])*"'),
    ('FLOAT',         r'-?\d+\.\d*(?:[eE][+-]?\d+)?'),
    ('INTEGER',       r'-?\d+'),
    ('BOOLEAN',       r'\b(?:true|false)\b'),
    ('NULL',          r'\bnull\b'),
    ('OPERATOR',      r'\+=|-=|\*\*|>>|<<|>=|<=|==|!=|\b(and|or|not)\b|[-+*/%={}()[\].,:;<>]'),
    ('IDENTIFIER',    r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('WHITESPACE',    r'[ \t\r\n]+'),
    ('OTHER',         r'.')
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
SCANNER = re.compile(TOKEN_REGEX, re.DOTALL)

class Token:
    """Simple token container used by the symbol-table program."""
    __slots__ = ('kind', 'value')
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value


class SwiftLangAnalyzer:
    def __init__(self):
        self.literals = []
        self.operators = []
        self.variables = set()
        self.reserved = []
        self.var_declared = defaultdict(int)
        self.line_count = 0
        self._raw_tokens = []

    def analyze(self, source_code):
        clean_lines = []
        for line in source_code.splitlines():
            if line.strip().startswith('//') or not line.strip():
                continue
            line_no_comment = re.sub(r'//.*$', '', line)
            clean_lines.append(line_no_comment)
        self.line_count = len([l for l in clean_lines if l.strip()])
        clean_source = '\n'.join(clean_lines)

        pos = 0
        let_next = False

        while pos < len(clean_source):
            match = SCANNER.match(clean_source, pos)
            if not match:
                pos += 1
                continue

            kind = match.lastgroup
            value = match.group()
            pos = match.end()

            if kind in ('WHITESPACE', 'COMMENT_BLOCK', 'COMMENT_LINE'):
                continue
            
            self._raw_tokens.append((kind, value))

            if kind in ('STRING', 'INTEGER', 'FLOAT', 'BOOLEAN', 'NULL'):
                self.literals.append(value)
                continue

            if kind == 'OPERATOR':
                self.operators.append(value)
                let_next = False
                continue

            if kind == 'IDENTIFIER':
                if value in RESERVED_WORDS:
                    self.reserved.append(value)
                    let_next = (value == 'let')
                else:
                    if let_next:
                        self.variables.add(value)
                        self.var_declared[value] += 1
                        let_next = False
                    else:
                        self.variables.add(value)
                continue

        self.variables = sorted(self.variables)
    
    def get_tokens(self):
        return [Token(kind, value) for kind, value in self._raw_tokens]

    def generate_report(self):
        lines = []
        lines.append("=" * 60)
        lines.append("SWIFTLANG SOURCE CODE ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append("")

        unique_lits = sorted(set(self.literals))
        lines.append(f"1. Literals Used: {len(self.literals)}")
        lines.append(f"   Unique Literals: {len(unique_lits)}")
        if unique_lits:
            lines.append("   List: " + ", ".join(unique_lits))
        lines.append("")

        op_counter = Counter(self.operators)
        lines.append(f"2. Operators Used: {len(self.operators)}")
        lines.append("   Breakdown:")
        for op, cnt in sorted(op_counter.items(), key=lambda x: -x[1]):
            lines.append(f"      '{op}': {cnt}")
        lines.append("")

        explicit_declared = sum(self.var_declared.values())
        implicit_count = len([v for v in self.variables if v not in self.var_declared])
        total_declared = explicit_declared + implicit_count
        dup_vars = {v: c for v, c in self.var_declared.items() if c > 1}

        lines.append(f"3. Variables Used: {total_declared}")
        lines.append(f"   Unique Variables: {len(self.variables)}")
        if self.variables:
            lines.append("   List: " + ", ".join(self.variables))
        if dup_vars:
            lines.append("   DUPLICATE DECLARATIONS:")
            for v, c in dup_vars.items():
                lines.append(f"      '{v}' declared {c} times")
        else:
            lines.append("   No duplicate variable declarations.")

        res_counter = Counter(self.reserved)
        lines.append(f"4. Reserved Words Used: {len(self.reserved)}")
        lines.append("   Breakdown:")
        for word, cnt in sorted(res_counter.items(), key=lambda x: -x[1]):
            lines.append(f"      '{word}': {cnt}")
        lines.append("")

        lines.append("5. Explicit Data Type Hints: 0")
        lines.append("   No explicit type hints found (SwiftLang is dynamically typed).")
        lines.append("")

        lines.append(f"6. Lines of Code Processed: {self.line_count} (excluding comments and blank lines)")

        return "\n".join(lines)


def main():
    with open('input.sl', 'r', encoding='utf-8') as f:
        source = f.read()

    analyzer = SwiftLangAnalyzer()
    analyzer.analyze(source)
    report = analyzer.generate_report()
    print(report)
    with open('analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)


if __name__ == '__main__':
    main()
