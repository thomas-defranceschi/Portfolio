from AST import *

### Helper functions for parsing tasks ###

def peek_token(tokens):
    """Return the next token without consuming it."""
    if tokens:
        return tokens[0]
    return None

def advance_token(tokens):
    """Consume and return the next token."""
    if tokens:
        return tokens.pop(0)
    return None

def expect_token(tokens, expected_type, optional_type = []):
    """Consume the next token if it matches the expected type, else raise an error."""
    token = advance_token(tokens)
    if token is None or (token.type != expected_type and token.type not in optional_type):
        raise ValueError(f"In line {token.line_number if token else 'EOF'}: Expected token type {expected_type}, but got {token.type if token else 'EOF'}")
    return token

def match_token(tokens, expected_types):
    """Check if the next token matches the expected type and consume it if so."""
    if tokens and tokens[0].type in expected_types:
        return advance_token(tokens)
    return None

### Parsing expressions ###

def parse_primary(tokens):
    """Parse a primary expression (identifier, number, string)."""
    next_token = peek_token(tokens)
    if next_token is None:
        raise ValueError("Unexpected end of input while parsing primary expression.")
    if next_token.type == "IDENTIFIER":
        token = next_token(tokens)
        advance_token(tokens)
        return Variable(token.value)
    elif next_token.type == "INTEGER" or next_token.type == "REAL":
        token = next_token(tokens)
        advance_token(tokens)
        return Literal(next_token.type, token.value)
    elif next_token.type == "TRUE" or next_token.type == "FALSE":
        token = next_token(tokens)
        advance_token(tokens)
        return Literal(next_token.type, token.value)
    elif next_token.type == "STRING":
        token = next_token(tokens)
        advance_token(tokens)
        return Literal(next_token.type, token.value)
    else:
        raise ValueError(f"In line {next_token.line_number if next_token else 'EOF'}: Unexpected token type in primary expression: {next_token.type}")

def parse_unary(tokens):
    """Parse a unary expression."""
    next_token = peek_token(tokens)
    if next_token and next_token.type in ["PLUS", "MINUS", "NOT"]:
        operator = next_token.type
        advance_token(tokens)
        operand = parse_unary(tokens)
        return UnaryExpression(operator, operand, next_token.line_number)
    else:
        return parse_primary(tokens)

def parse_binary(tokens):
    """Parse a binary expression."""
    left = parse_unary(tokens)
    operator = peek_token(tokens)
    if operator and operator.type in ["PLUS", "MINUS", "MULTIPLY", "DIVIDE", "EQUALS", "NEQ", "LT", "GT", "LEQ", "GEQ", "AND", "OR"]:
        advance_token(tokens)
        right = parse_unary(tokens)
        return BinaryExpression(left, operator, right, operator.line_number)
    else:
        return left

def parse_expression(tokens):
    """Parse an expression."""
    return parse_binary(tokens)

def parse_declare_statement(tokens):
    """Parse a variable declaration statement."""
    declare_token = expect_token(tokens, "DECLARE")
    var_token = expect_token(tokens, "IDENTIFIER")
    expect_token(tokens, "COLON")
    var_type = expect_token(tokens, "INTEGER", ["REAL", "CHAR","BOOLEAN", "STRING"])
    return VariableDeclaration(var_type.value, Variable(var_token.value), declare_token.line_number)

def parse_assignment(tokens):
    """Parse an assignment statement."""
    var_token = expect_token(tokens, "IDENTIFIER")
    expect_token(tokens, "ASSIGN")
    expr = parse_expression(tokens)
    return AssignmentStatement(Variable(var_token.value), expr, var_token.line_number)

def parse_input_statement(tokens):
    """Parse an input statement."""
    input_token = expect_token(tokens, "INPUT")
    var_token = expect_token(tokens, "IDENTIFIER")
    return InputStatement(Variable(var_token.value), input_token.line_number)

def parse_output_statement(tokens):
    """Parse an output statement."""
    output_token = expect_token(tokens, "OUTPUT")
    expr = parse_expression(tokens)
    return OutputStatement(expr, output_token.line_number)

def parse_if_statement(tokens):
    """Parse an IF statement."""
    if_token = expect_token(tokens, "IF")
    condition = parse_expression(tokens)
    expect_token(tokens, "THEN")
    then_statements = []
    while not peek_token(tokens) or peek_token(tokens).type not in ["ELSE", "ENDIF"]:
        stmt = parse_statement(tokens)
        then_statements.append(stmt)
    then_statements = Statements(then_statements)
    else_statements = []
    if match_token(tokens, ["ELSE"]):
        while not peek_token(tokens) or peek_token(tokens).type != "ENDIF":
            stmt = parse_statement(tokens)
            else_statements.append(stmt)
        else_statements = Statements(else_statements)
    expect_token(tokens, "ENDIF")
    return IfStatement(condition, then_statements, if_token.line_number, else_statements)

def parse_while_statement(tokens):
    """Parse a WHILE statement."""
    while_token = expect_token(tokens, "WHILE")
    condition = parse_expression(tokens)
    expect_token(tokens, "DO")
    body_statements = []
    while not peek_token(tokens) or peek_token(tokens).type != "ENDWHILE":
        stmt = parse_statement(tokens)
        body_statements.append(stmt)
    body_statements = Statements(body_statements)
    expect_token(tokens, "ENDWHILE")
    return WhileStatement(condition, body_statements, while_token.line_number)

def parse_statement(tokens):
    """Parse a single statement."""
    next_token = peek_token(tokens)
    if next_token.type == "IDENTIFIER":
        return parse_assignment(tokens)
    elif next_token.type == "DECLARE":
        return parse_declare_statement(tokens)
    elif next_token.type == "INPUT":
        return parse_input_statement(tokens)
    elif next_token.type == "OUTPUT":
        return parse_output_statement(tokens)
    elif next_token.type == "IF":
        return parse_if_statement(tokens)
    elif next_token.type == "WHILE":
        return parse_while_statement(tokens)
    else:
        raise ValueError(f"In line {next_token.line_number if next_token else 'EOF'}: Unexpected token type: {next_token.type}")

def parse_statements(tokens):
    """Parse a sequence of statements."""
    statements = []
    while tokens:
        if peek_token(tokens).type == "EOF":
                advance_token(tokens)  # consume EOF
                break
        stmt = parse_statement(tokens)
        statements.append(stmt)
    return Statements(statements)

def parse(tokens, filename = "temp"):
    """Parse a list of tokens into an AST."""
    ast_root = parse_statements(tokens)
    with open(filename + "_ast.txt", "w") as f:
        f.write(ast_root.str_indented(0))
    
    return ast_root
    
