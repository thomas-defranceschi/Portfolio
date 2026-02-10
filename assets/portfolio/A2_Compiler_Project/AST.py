### Define AST nodes for the CIE pseudocode language subset. ###

### Helper function to convert operators to python code ###
operators_map = {
    "PLUS": "+",
    "MINUS": "-",
    "MULTIPLY": "*",
    "DIVIDE": "/",
    "AND": "and",
    "OR": "or",
    "NOT": "not",
    "EQ": "==",
    "NEQ": "!=",
    "LT": "<",
    "LTE": "<=",
    "GT": ">",
    "GTE": ">="
}

class ASTNode:
    """ Base class for all AST nodes. """
    def str_indented(self, indent_level):
        raise NotImplementedError("Subclasses must implement str_indented method")
    def to_code(self, indent=""):
        raise NotImplementedError("Subclasses must implement to_code method")

class Literal(ASTNode):
    def __init__(self, type : str, value):
        self.type = type
        self.value = value
    
    def str_indented(self, indent_level):
        indent = "    " * indent_level
        return f"{indent}{self.type} Literal: {self.value}"
    
    def __repr__(self):
        return f"LiteralNode({self.type}, {self.value})"
    
    def to_code(self, indent=""):
        if self.type == "STRING":
            return f'"{self.value}"'
        elif self.type == "TRUE":
            return "True"
        elif self.type == "FALSE":
            return "False"
        return str(self.value)
    
class Variable(ASTNode):
    def __init__(self, name):
        self.name = name
    
    def str_indented(self, indent_level):
        indent = "    " * indent_level
        return f"{indent}Variable: {self.name}"
    
    def to_code(self, indent=""):
        return self.name

    def __repr__(self):
        return f"VariableNode({self.name})"

class VariableDeclaration(ASTNode):
    def __init__(self, var_type : str, variable : Variable, line : int):
        self.var_type = var_type
        self.variable = variable
        self.line = line

    def str_indented(self, indent_level):
        indent = "    " * indent_level
        result = f"{indent}Declaration:\n"
        result += f"{indent + "    "}Type: {self.var_type}\n"
        result += self.variable.str_indented(indent_level + 1)
        return result
    
    def to_code(self, indent=""):
        match self.var_type:
            case "INTEGER":
                return f"{indent}{self.variable.name} = 0"
            case "REAL":
                return f"{indent}{self.variable.name} = 0.0"
            case "STRING":
                return f'{indent}{self.variable.name} = ""'
            case "BOOLEAN":
                return f"{indent}{self.variable.name} = False"
    
    def __repr__(self):
        return f"VarDeclNode({self.var_type}, {self.variable}, line {self.line})"

class InputStatement(ASTNode):
    def __init__(self, variable, line):
        self.variable = variable
        self.line = line

    def str_indented(self, indent_level):
        indent = "    " * indent_level
        result = f"{indent}Input:\n"
        result += self.variable.str_indented(indent_level + 1)
        return result
    
    def to_code(self, indent=""):
        result = f"{indent}{self.variable.name} = input()\n"
        result += f"{indent}try:\n"
        result += f"{indent}    {self.variable.name} = int({self.variable.name})\n"
        result += f"{indent}except ValueError:\n"
        result += f"{indent}    try:\n"
        result += f"{indent}        {self.variable.name} = float({self.variable.name})\n"
        result += f"{indent}    except ValueError:\n"
        result += f"{indent}        pass\n"
        return result

    def __repr__(self):
        return f"InputStmtNode({self.variable}, line {self.line})"

class OutputStatement(ASTNode):
    def __init__(self, expression, line):
        self.expression = expression
        self.line = line

    def str_indented(self, indent_level):
        indent = "    " * indent_level
        result = f"{indent}Output:\n"
        result += self.expression.str_indented(indent_level + 1)
        return result
    
    def to_code(self, indent=""):
        return f"{indent}print({self.expression.to_code()})"
    
    def to_C_sharp(self, indent=""):
        return f"{indent}Console.WriteLine({self.expression.to_code()});"
    
    def to_JAVA(self, indent=""):
        return f"{indent}System.out.println({self.expression.to_code()});"
    
    def __repr__(self):
        return f"OutputStmtNode({self.expression}, line {self.line})"

class AssignmentStatement(ASTNode):
    def __init__(self, variable, expression, line):
        self.variable = variable
        self.expression = expression
        self.line = line

    def str_indented(self, indent_level):
        indent = "    " * indent_level
        result = f"{indent}Assign: \n"
        result += self.variable.str_indented(indent_level + 1) + "\n"
        result += self.expression.str_indented(indent_level + 1)
        return result
    
    def to_code(self, indent=""):
        return f"{indent}{self.variable.name} = {self.expression.to_code()}"
    
    def __repr__(self):
        return f"AssignStmtNode({self.variable}, {self.expression}, line {self.line})"

class UnaryExpression(ASTNode):
    def __init__(self, operator, operand : ASTNode, line):
        self.operator = operator
        self.operand = operand
        self.line = line
    
    def str_indented(self, indent_level):
        indent = "    " * indent_level
        result = f"{indent}UnaryExpr: {self.operator}\n"
        result += self.operand.str_indented(indent_level + 1)
        return result
    
    def to_code(self, indent=""):
        return f"({operators_map[self.operator]} {self.operand.to_code()})"

    def __repr__(self):
        return f"UnaryExprNode({self.operator}, {self.operand}, line {self.line})"

class BinaryExpression(ASTNode):
    def __init__(self, left : ASTNode, operator, right : ASTNode, line):
        self.left = left
        self.operator = operator
        self.right = right
        self.line = line

    def str_indented(self, indent_level):
        indent = "    " * indent_level
        result = f"{indent}BinaryExpr: {self.operator}\n"
        result += self.left.str_indented(indent_level + 1) + "\n"
        result += self.right.str_indented(indent_level + 1)
        return result
    
    def to_code(self, indent=""):
        return f"({self.left.to_code()} {operators_map[self.operator.type]} {self.right.to_code()})"
    
    def __repr__(self):
        return f"BinaryExprNode({self.left}, {self.operator}, {self.right}, line {self.line})"

class IfStatement(ASTNode):
    def __init__(self, condition : ASTNode, then_branch : ASTNode, line, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
        self.line = line

    def str_indented(self, indent_level):
        indent = "    " * indent_level
        result = f"{indent}If: \n"
        result += self.condition.str_indented(indent_level + 1) + "\n"
        result += f"{indent}Then:\n"
        result += self.then_branch.str_indented(indent_level + 1) + "\n"
        if self.else_branch:
            result += f"{indent}else:\n"
            for i, statement in enumerate(self.else_branch.statements):
                result += statement.str_indented(indent_level + 1)
                if i < len(self.else_branch.statements) - 1:
                    result += "\n"
        return result
    
    def to_code(self, indent=""):
        result = f"{indent}if {self.condition.to_code()}:\n"
        result += self.then_branch.to_code(indent + "    ") + "\n"
        if self.else_branch:
            result += f"{indent}else:\n"
            result += self.else_branch.to_code(indent + "    ")
        return result
    
    def __repr__(self):
        return f"IfStmtNode({self.condition}, {self.then_branch}, else={self.else_branch}, line {self.line})"

class WhileStatement(ASTNode):
    def __init__(self, condition : ASTNode, body : ASTNode, line):
        self.condition = condition
        self.body = body
        self.line = line

    def str_indented(self, indent_level):
        indent = "    " * indent_level
        result = f"{indent}While:\n"
        result += self.condition.str_indented(indent_level + 1) + "\n"
        result += self.body.str_indented(indent_level + 1)
        return result
    
    def to_code(self, indent=""):
        result = f"{indent}while {self.condition.to_code()}:\n"
        result += self.body.to_code(indent + "    ")
        return result

    def __repr__(self):
        return f"WhileStmtNode({self.condition}, {self.body}, line {self.line})"

class ForStatement(ASTNode):
    def __init__(self, loop_variable : ASTNode, start : ASTNode, end : ASTNode, body : ASTNode, line):
        self.loop_variable = loop_variable
        self.start = start
        self.end = end
        self.body = body
        self.line = line
        
    def str_indented(self, indent_level):
        indent = "    " * indent_level
        result = f"{indent}For: \n"
        result += self.loop_variable.str_indented(indent_level + 1) + "\n"
        result += f"{indent}from: \n"
        result += self.start.str_indented(indent_level + 1) +"\n"
        result += f"{indent}to: \n"
        result += self.end.str_indented(indent_level + 1) + "\n"
        result += f"{indent}do:\n"
        result += self.body.str_indented(indent_level + 1)
        return result
    
    def to_code(self, indent=""):
        result = f"{indent}for {self.loop_variable.to_code()} in range({self.start.to_code()}, {self.end.to_code()} + 1):\n"
        result += self.body.to_code(indent + "    ")
        return result
    
    def __repr__(self):
        return f"ForStmtNode({self.loop_variable}, {self.start}, {self.end}, {self.body}, line {self.line})"

class Statements(ASTNode):
    def __init__(self, statements):
        self.statements = statements
    
    def str_indented(self, indent_level) -> str:
        result = ""
        for i, stmt in enumerate(self.statements):
            result += stmt.str_indented(indent_level)
            if i < len(self.statements) - 1:
                result += "\n"
        return result
    
    def to_code(self, indent=""):
        result = ""
        for stmt in self.statements:
            result += stmt.to_code(indent) + "\n"
        return result[:-1]  # Remove last newline

    def __repr__(self):
        return f"StatementsNode({self.statements})"

def print_ast(ast_node):
    """Print the AST in a human-readable format."""
    print(ast_node.str_indented(0))

if __name__ == "__main__":
    # Example tree with all node types
    ast = Statements(statements=[
        VariableDeclaration("integer", Variable("x"), line=1),
        AssignmentStatement(Variable("x"), Literal("integer", "10"), line=2),
        IfStatement(
            condition=BinaryExpression(Variable("x"), ">", Literal("integer", "5"), line=3),
            then_branch=OutputStatement(Variable("x"), line=4),
            else_branch=OutputStatement(Literal("integer", "0"), line=5)
        , line=3),
        ForStatement(
            loop_variable=Variable("i"),
            start=Literal("integer", "1"),
            end=Literal("integer", "10"),
            body= Statements(statements=[
                OutputStatement(Literal("string", "i = "), line=6),
                OutputStatement(Variable("i"), line=6)])
        , line=6),
        InputStatement(Variable("y"), line=7)
    ])

    print_ast(ast)