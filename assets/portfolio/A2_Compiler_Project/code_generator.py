from AST import *

### Generates code from the AST. ###

def generate_code(ast_node, filename = "temp"):
    """Generates a string representation of the AST with indentation."""
    
    with open(f"{filename}.py", "w") as f:
        if ast_node is None:
            return False
        result = ast_node.to_code()
        f.write(result)
    
    return True