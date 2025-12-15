# semantic_analyzer.py
from .parser import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # {name: {'type': str, 'value': any}} - extend your HashTable if needed
        self.errors = []

    def analyze(self, ast):
        self.visit(ast)
        if self.errors:
            raise SemanticError("\n".join(self.errors))
        return self.symbol_table  # Or whatever you need

    def visit(self, node):
        method = f'visit_{type(node).__name__}'
        return getattr(self, method, self.generic_visit)(node)

    def generic_visit(self, node):
        for child in vars(node).values():
            if isinstance(child, ASTNode):
                self.visit(child)
            elif isinstance(child, list):
                for item in child:
                    if isinstance(item, ASTNode):
                        self.visit(item)

    def visit_Program(self, node):
        self.generic_visit(node)

    def visit_DeclStmt(self, node):
        if node.name in self.symbol_table:
            self.errors.append(f"Duplicate declaration: {node.name}")
            return
        # Dynamic typing: store type but allow changes later
        typ = self.infer_type(node.expr)
        self.symbol_table[node.name] = {'type': typ, 'value': None}
        self.visit(node.expr)


    def visit_AssignStmt(self, node):
        if node.name not in self.symbol_table:
            self.errors.append(f"Undeclared variable: {node.name}")
            return
        # Dynamic typing: update type on assignment
        new_type = self.infer_type(node.expr)
        self.symbol_table[node.name]['type'] = new_type
        self.visit(node.expr)

    def visit_VarExpr(self, node):
        if node.name not in self.symbol_table:
            self.errors.append(f"Undeclared variable: {node.name}")

    def visit_BinaryExpr(self, node):
        self.visit(node.left)
        self.visit(node.right)
        left_type = self.infer_type(node.left)
        right_type = self.infer_type(node.right)
        if not self.types_compatible(left_type, right_type):
            self.errors.append(f"Type mismatch in binary op {node.op}")

    def visit_IfStmt(self, node):
        cond_type = self.infer_type(node.cond)
        if cond_type != 'boolean':
            self.errors.append("Condition must be boolean")
        self.visit(node.cond)
        self.visit(node.then_body)
        if node.else_body:
            self.visit(node.else_body)

    # Add visit_WhileStmt, etc. (check cond is boolean)

    def infer_type(self, expr):
        if isinstance(expr, LiteralExpr):
            return expr.typ
        elif isinstance(expr, VarExpr):
            if expr.name not in self.symbol_table:
                return 'unknown'
            return self.symbol_table[expr.name]['type']
        elif isinstance(expr, BinaryExpr):
            # Infer based on op (e.g., + for numbers/strings)
            left_type = self.infer_type(expr.left)
            if expr.op in ('+', '-', '*', '/', '%'):
                return 'number' if left_type in ('integer', 'float') else 'unknown'
            elif expr.op in ('==', '!=', '<', '>'):
                return 'boolean'
            # etc.
        return 'unknown'

    def types_compatible(self, t1, t2):
        return True

class SemanticError(Exception):
    pass

# In main: after parsing ast, SemanticAnalyzer().analyze(ast)