# parser.py (or extend symbol_table_generator.py)
from .tokenizer_analyzer import RESERVED_WORDS

# AST Node Classes
class ASTNode:
    pass

class BinaryExpr(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryExpr(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class LiteralExpr(ASTNode):
    def __init__(self, value, typ):
        self.value = value
        self.typ = typ

class VarExpr(ASTNode):
    def __init__(self, name):
        self.name = name

class AssignStmt(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class DeclStmt(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class IfStmt(ASTNode):
    def __init__(self, cond, then_body, else_body=None):
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body

class WhileStmt(ASTNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class PrintStmt(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class ReadStmt(ASTNode):
    def __init__(self, name):
        self.name = name

class BlockStmt(ASTNode):
    def __init__(self, stmts):
        self.stmts = stmts

class Program(ASTNode):
    def __init__(self, stmts):
        self.stmts = stmts

# Parser Class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _advance(self):
        self.pos += 1

    def _expect(self, kind, value=None):
        tok = self._current()
        if not tok or tok.kind != kind or (value and tok.value != value):
            raise SyntaxError(f"Expected {kind} '{value}' at pos {self.pos}")
        self._advance()
        return tok
    
    def _at_statement_end(self):
        tok = self._current()
        return tok is None or (tok.kind == 'OPERATOR' and tok.value in (';', ')', '}'))

    def parse_program(self):
        stmts = []
        while self._current():
            stmts.append(self.parse_stmt())
        return Program(stmts)

    def parse_stmt(self):
        tok = self._current()
        if tok.kind == 'IDENTIFIER':
            if tok.value == 'let':
                return self.parse_decl()
            elif tok.value == 'if':
                return self.parse_if()
            elif tok.value == 'while':
                return self.parse_while()
            elif tok.value == 'print':
                return self.parse_print()
            elif tok.value == 'read':
                return self.parse_read()
            elif tok.value not in RESERVED_WORDS:
                return self.parse_assign()
        elif tok.kind == 'OPERATOR' and tok.value == '{':
            return self.parse_block()
        raise SyntaxError(f"Unexpected token {tok.kind}:{tok.value} at pos {self.pos}")

    def parse_decl(self):
        self._expect('IDENTIFIER', 'let')
        name = self._expect('IDENTIFIER').value
        self._expect('OPERATOR', '=')
        expr = self.parse_expr()
        self._expect('OPERATOR', ';')
        return DeclStmt(name, expr)

    def parse_assign(self):
        name = self._expect('IDENTIFIER').value
        self._expect('OPERATOR', '=')
        expr = self.parse_expr()
        self._expect('OPERATOR', ';')
        return AssignStmt(name, expr)

    def parse_if(self):
        self._expect('IDENTIFIER', 'if')
        self._expect('OPERATOR', '(')
        cond = self.parse_expr()
        self._expect('OPERATOR', ')')
        then_body = self.parse_stmt()
        else_body = None
        if self._current() and self._current().value == 'else':
            self._advance()
            else_body = self.parse_stmt()
        return IfStmt(cond, then_body, else_body)

    def parse_while(self):
        self._expect('IDENTIFIER', 'while')
        self._expect('OPERATOR', '(')
        cond = self.parse_expr()
        self._expect('OPERATOR', ')')
        body = self.parse_stmt()
        return WhileStmt(cond, body)

    def parse_print(self):
        self._expect('IDENTIFIER', 'print')
        self._expect('OPERATOR', '(')
        expr = self.parse_expr()
        self._expect('OPERATOR', ')')
        self._expect('OPERATOR', ';')
        return PrintStmt(expr)

    def parse_read(self):
        self._expect('IDENTIFIER', 'read')
        self._expect('OPERATOR', '(')
        name = self._expect('IDENTIFIER').value
        self._expect('OPERATOR', ')')
        self._expect('OPERATOR', ';')
        return ReadStmt(name)

    def parse_block(self):
        self._expect('OPERATOR', '{')
        stmts = []
        while self._current() and self._current().value != '}':
            stmts.append(self.parse_stmt())
        self._expect('OPERATOR', '}')
        return BlockStmt(stmts)

    def parse_expr(self):
        # Logical: and / or (lowest precedence)
        expr = self.parse_logical_and_or()
        return expr

    def parse_logical_and_or(self):
        expr = self.parse_equality()
        while (self._current() and 
               self._current().value in ('and', 'or') and 
               not self._at_statement_end()):
            op = self._current().value
            self._advance()
            right = self.parse_equality()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_equality(self):
        expr = self.parse_comparison()
        while (self._current() and 
               self._current().value in ('==', '!=') and 
               not self._at_statement_end()):
            op = self._current().value
            self._advance()
            right = self.parse_comparison()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_comparison(self):
        expr = self.parse_additive()
        while (self._current() and 
               self._current().value in ('<', '>', '<=', '>=') and 
               not self._at_statement_end()):
            op = self._current().value
            self._advance()
            right = self.parse_additive()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_additive(self):
        expr = self.parse_multiplicative()
        while (self._current() and 
               self._current().value in ('+', '-') and 
               not self._at_statement_end()):
            op = self._current().value
            self._advance()
            right = self.parse_multiplicative()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_multiplicative(self):
        expr = self.parse_unary()
        while (self._current() and 
               self._current().value in ('*', '/', '%') and 
               not self._at_statement_end()):
            op = self._current().value
            self._advance()
            right = self.parse_unary()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_unary(self):
        if self._current() and self._current().kind == 'OPERATOR' and self._current().value in ('-', 'not'):
            op = self._current().value
            self._advance()
            operand = self.parse_unary()  # Allow --x, not not true, etc.
            return UnaryExpr(op, operand)
        return self.parse_primary()

    def parse_primary(self):
        tok = self._current()
        if tok is None:
            raise SyntaxError("Unexpected end of input")

        if tok.kind in ('INTEGER', 'FLOAT', 'STRING', 'BOOLEAN', 'NULL'):
            self._advance()
            return LiteralExpr(tok.value, tok.kind.lower())

        if tok.kind == 'IDENTIFIER':
            if tok.value in RESERVED_WORDS:
                raise SyntaxError(f"Unexpected reserved word in expression: {tok.value}")
            self._advance()
            return VarExpr(tok.value)

        if tok.kind == 'OPERATOR' and tok.value == '(':
            self._advance()
            expr = self.parse_expr()
            self._expect('OPERATOR', ')')
            return expr

        raise SyntaxError(f"Unexpected token in primary: {tok}")

# Integrate with your symbol table (optional, but call after parsing for now)
# In main, after analyzer.get_tokens(), do: ast = Parser(tokens).parse_program()