import lexer
import parser
import semantic_analyser
import code_generator

if __name__ == "__main__":

    filename = input("Enter the source code filename (default value: example.txt): ") or "example"
    code = []
    if filename:
        with open(filename + ".txt", "r") as f:
            code = f.readlines()
    tokens = lexer.lexical_analysis(code, filename)
    if tokens:
        ast_root = parser.parse(tokens, filename)
        semantic_analyser.semantic_analysis(ast_root, filename)
        if not code_generator.generate_code(ast_root, filename):
            print("Code generation failed.")
