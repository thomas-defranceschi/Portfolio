from symbols import *
from AST import *

### Semantic analysis of the parsed AST ###

def first_pass(ast_node, sym_table):
    """First pass semantic analysis: variable declarations."""
    
    # Base cases
    if ast_node is None:
        return
    elif isinstance(ast_node, Literal) or isinstance(ast_node, Variable) or isinstance(ast_node, OutputStatement):
        return
    elif isinstance(ast_node, BinaryExpression) or isinstance(ast_node, UnaryExpression):
        return
    
    # Declarations (3 types: explicit, implicit via assignment, implicit via input)
    elif isinstance(ast_node, VariableDeclaration):
        var_name = ast_node.variable.name
        var_line = ast_node.line
        try:
            sym_table.declare(var_name, var_line)
        except Exception as e:
            print(f"{e}")
    elif isinstance(ast_node, AssignmentStatement) or isinstance(ast_node, InputStatement):
        var_name = ast_node.variable.name
        var_line = ast_node.line
        if not sym_table.already_defined(var_name, var_line):
            try:
                sym_table.declare(var_name, var_line)
            except Exception as e:
                print(f"{e}")

    # Recursive cases
    elif isinstance(ast_node, Statements):
        for stmt in ast_node.statements:
            first_pass(stmt, sym_table)
    elif isinstance(ast_node, IfStatement):
        first_pass(ast_node.then_branch, sym_table)
        if ast_node.else_branch:
            first_pass(ast_node.else_branch, sym_table)
    elif isinstance(ast_node, ForStatement):
        first_pass(ast_node.body, sym_table)
    elif isinstance(ast_node, WhileStatement):
        first_pass(ast_node.body, sym_table)
    
def second_pass(ast_node, sym_table, line):
    """Second pass semantic analysis: variable usage."""
    
    # Base cases
    if ast_node is None:
        return
    elif isinstance(ast_node, Literal) or isinstance(ast_node, VariableDeclaration) or isinstance(ast_node, InputStatement):
        return
    
    # Variable usage
    elif isinstance(ast_node, Variable):
        var_name = ast_node.name
        var_line = line
        try:
            sym_table.lookup(var_name, var_line)
        except Exception as e:
            print(f"{e}")
    
    # Recursive cases
    elif isinstance(ast_node, AssignmentStatement):
        second_pass(ast_node.expression, sym_table, ast_node.line)
    elif isinstance(ast_node, OutputStatement):
        second_pass(ast_node.expression, sym_table, ast_node.line)
    elif isinstance(ast_node, UnaryExpression):
        second_pass(ast_node.operand, sym_table, ast_node.line)
    elif isinstance(ast_node, BinaryExpression):
        second_pass(ast_node.left, sym_table, ast_node.line)
        second_pass(ast_node.right, sym_table, ast_node.line)
    elif isinstance(ast_node, IfStatement):
        second_pass(ast_node.condition, sym_table, ast_node.line)
        second_pass(ast_node.then_branch, sym_table, ast_node.line)
        if ast_node.else_branch:
            second_pass(ast_node.else_branch, sym_table, ast_node.line)
    elif isinstance(ast_node, ForStatement):
        second_pass(ast_node.start, sym_table, ast_node.line)
        second_pass(ast_node.end, sym_table, ast_node.line)
        second_pass(ast_node.body, sym_table, ast_node.line)
    elif isinstance(ast_node, WhileStatement):
        second_pass(ast_node.condition, sym_table, ast_node.line)
        second_pass(ast_node.body, sym_table, ast_node.line)
    elif isinstance(ast_node, Statements):
        for stmt in ast_node.statements:
            second_pass(stmt, sym_table, stmt.line)

def semantic_analysis(ast_root, filename="temp"):
    """Performs semantic analysis on the AST."""
    sym_table = symbol_table()
    
    # First pass: declarations
    try:
        first_pass(ast_root, sym_table)
    except Exception as e:
        print(f"{e}")
        
    with open(f"{filename}_symbol_table.txt", "w") as f:
        f.write(str(sym_table))
    
    # Second pass: usage
    try:
        second_pass(ast_root, sym_table, 0)
    except Exception as e:
        print(f"{e}")