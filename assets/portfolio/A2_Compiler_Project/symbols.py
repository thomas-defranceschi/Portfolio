class symbol:
    def __init__(self, name, line):
        self.name = name
        self.line = line

class symbol_table:
    def __init__(self):
        self.symbols = {}
    
    def declare(self, name, line):
        if name in self.symbols:
            if self.symbols[name].line < line:
                raise Exception(f"{line=} Semantic Error: Variable '{name}' already declared on line {self.symbols[name].line})")
            else:
                raise Exception(f"{line=} Semantic Error: Variable '{name}' declared on lines {self.symbols[name].line}) and {line})")
        self.symbols[name] = symbol(name, line)
    
    def already_defined(self, name, line):
        if name in self.symbols:
            return self.symbols[name].line < line
        return False

    def lookup(self, name, line):
        if not self.already_defined(name, line):
            raise Exception(f"{line=} Semantic Error: Variable '{name}' not declared before use")
        return self.symbols[name]
    
    def __str__(self) -> str:
        result = "Symbol Table:\n"
        for name, sym in self.symbols.items():
            result += f"  {name}: declared on line {sym.line}\n"
        return result