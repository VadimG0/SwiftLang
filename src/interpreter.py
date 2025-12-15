# interpreter.py
from .parser import ASTNode

class Interpreter:
    def __init__(self, symbol_table):
        self.env = symbol_table  # {name: {'type': str, 'value': any}}

    def interpret(self, ast):
        self.visit(ast)

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
        return None

    def visit_Program(self, node):
        self.generic_visit(node)

    def visit_DeclStmt(self, node):
        value = self.visit(node.expr)
        self.env[node.name]['value'] = value

    def visit_AssignStmt(self, node):
        value = self.visit(node.expr)
        self.env[node.name]['value'] = value

    def visit_PrintStmt(self, node):
        value = self.visit(node.expr)
        print(value)

    def visit_ReadStmt(self, node):
        value = input("Enter value: ")
        # Infer type from input (simplify: assume string)
        self.env[node.name]['value'] = value

    def visit_IfStmt(self, node):
        cond = self.visit(node.cond)
        if cond:
            self.visit(node.then_body)
        elif node.else_body:
            self.visit(node.else_body)

    def visit_WhileStmt(self, node):
        while self.visit(node.cond):
            self.visit(node.body)

    def visit_BinaryExpr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        ops = {
            '+': lambda l, r: l + r,
            '-': lambda l, r: l - r,
            '*': lambda l, r: l * r,
            '/': lambda l, r: l / r,
            '%': lambda l, r: l % r,
            '==': lambda l, r: l == r,
            '!=': lambda l, r: l != r,
            '<': lambda l, r: l < r,
            '>':  lambda l, r: l > r,
            'and': lambda l, r: l and r,
            'or': lambda l, r: l or r,
            '<=': lambda l, r: l <= r,
            '>=': lambda l, r: l >= r,

        }
        return ops[node.op](left, right)

    def visit_UnaryExpr(self, node):
        expr = self.visit(node.expr)
        if node.op == '-':
            return -expr
        elif node.op == 'not':
            return not expr

    def visit_LiteralExpr(self, node):
        if node.typ == 'integer':
            return int(node.value)
        elif node.typ == 'float':
            return float(node.value)
        elif node.typ == 'string':
            return node.value.strip('"')
        elif node.typ == 'boolean':
            return node.value == 'true'
        elif node.typ == 'null':
            return None

    def visit_VarExpr(self, node):
        return self.env[node.name]['value']
    
    def visit_BlockStmt(self, node):
        for stmt in node.stmts:
            self.visit(stmt)


    # Add infer_type if needed (from semantic analyzer)

# In main: after analysis, Interpreter(symbol_table).interpret(ast)