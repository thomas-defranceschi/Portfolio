### Step 1: Removing unnecessary comments and whitespace ###

def is_blank_line(line : str) -> bool:
    """Returns true if the line is blank or contains only whitespace."""
    return len(line.strip()) == 0

def remove_comments_from_line(line: str) -> str:
    """Removes comments from a single line."""
    return line.split("//")[0].strip()

def remove_comments(lines : list[str]) -> list[str]:
    """Removes comments from a list of lines."""
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(remove_comments_from_line(line))
    return cleaned_lines

class clean_line:
    """Class representing a cleaned line of code."""
    def __init__(self, raw_line : str, line_number : int):
        self.raw_line = raw_line
        self.line_number = line_number
        self.content = raw_line.strip()

### Step 2: Tokens and symbol table ###

keywords = [
    "INTEGER", "REAL", "BOOLEAN", "STRING",
    "TRUE", "FALSE",
    "DECLARE",
    "IF", "THEN", "ELSE", "ENDIF",
    "WHILE", "DO", "ENDWHILE",
    "INPUT", "OUTPUT",
]

operators = {
    ":": "COLON", "<-": "ASSIGN",
    "+": "PLUS", "-": "MINUS", "*": "MULTIPLY", "/": "DIVIDE",
    "=": "EQ", "<>": "NEQ", "<": "LT", ">": "GT", "<=": "LTE", ">=": "GTE",
    "AND": "AND", "OR": "OR", "NOT": "NOT",
}

class Token:
    """Class representing a token."""
    def __init__(self, type : str, value : str, line_number : int):
        self.type = type
        self.value = value
        self.line_number = line_number

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value}, line {self.line_number})"

def is_first_keyword_or_identifier(words : list[str]) -> bool:
    """Checks if the first word is a keyword or identifier."""
    if not words:
        return False
    first_word = words[0]
    is_keyword = first_word in keywords
    if is_keyword:
        return True
    if not (first_word[0].isalpha() and all(c.isalnum() or c == '_' for c in first_word)):
        return False
    return True

def is_first_number_literal(words : list[str]) -> bool:
    """Checks if the first word is a number literal (integer or real)."""
    if not words:
        return False
    first_word = words[0]
    if first_word.count('.') > 1:
        return False
    parts = first_word.split('.')
    if all(part.isdigit() for part in parts):
        return True
    return False

def is_first_string_literal(words : list[str]) -> int:
    """Checks if the first word is a string literal."""
    if not words:
        return 0
    first_word = words[0]
    if not first_word.startswith('"'):
        return 0
    # empty string literal or one word string
    if first_word.startswith('"') and first_word.endswith('"') and len(first_word) > 1:
        return 1
    else:
        string = [first_word]
        for word in words[1:]:
            string.append(word)
            if word.endswith('"'):
                return len(string)
    raise ValueError("Unterminated string literal")

def is_first_operator(words : list[str]) -> bool:
    """Checks if the first word is an operator."""
    if not words:
        return False
    first_word = words[0]
    if first_word in operators.keys():
        return True
    return False
        

def tokenize_line(line : clean_line) -> list[Token]:
    """Tokenizes a cleaned line of code."""
    words = line.content.split()
    tokens = []
    
    while len(words) > 0:

        # Check for keywords and identifiers
        if is_first_keyword_or_identifier(words):
            first_word = words.pop(0)
            if first_word in keywords:
                tokens.append(Token(first_word, first_word, line.line_number))
            else:
                tokens.append(Token("IDENTIFIER", first_word, line.line_number))
            continue

        # Check for numbers
        if is_first_number_literal(words):
            first_word = words.pop(0)
            if '.' in first_word:
                tokens.append(Token("REAL", first_word, line.line_number))
            else:
                tokens.append(Token("INTEGER", first_word, line.line_number))
            continue

        # Check for strings
        str_length = is_first_string_literal(words)
        if str_length > 0:
            str_words = words[:str_length]
            words = words[str_length:]
            string_value = ' '.join(str_words).strip('"')
            tokens.append(Token("STRING", string_value, line.line_number))
            continue

        # Check for operators
        if is_first_operator(words):
            first_word = words.pop(0)
            tokens.append(Token(operators[first_word], first_word, line.line_number))
            continue

        raise ValueError(f"Unrecognized token '{words[0]}' on line {line.line_number}")

    return tokens

def lexical_analysis(lines : list[str], filename = "temp") -> list[list[Token]]:
    """Performs lexical analysis on a list of lines of code."""
    cleaned_lines = []
    for i, line in enumerate(remove_comments(lines)):
        if not is_blank_line(line):
            cleaned_lines.append(clean_line(line, i + 1))
    
    all_tokens = []

    with open(f"{filename}_tokens.txt", "w") as f:
        try:
            for cl in cleaned_lines:
                f.write(f"Line {cl.line_number}: {cl.content}\n")
                tokens = tokenize_line(cl)
                for token in tokens:
                    f.write(f"    {token.type}: {token.value}\n")
                    all_tokens.append(token)
        except ValueError as e:
            f.write(f"Lexical analysis error: {e}\n")
            print(f"Lexical analysis failed: {e}")
            return []
        all_tokens.append(Token("EOF", "", cleaned_lines[-1].line_number if cleaned_lines else 0))
        
        f.write("    EOF: \n")
    

    return all_tokens


if __name__ == "__main__":

    # test cases for is_first_string_literal
    test_cases = [
        ['"hello', 'world"'],
        ['"hello"'],
        ['"unterminated', 'string'],
        ['unstarted_string"'],
        ['not_a_string'],
        ['""'],
        ['"multi', 'word', 'string"'],
        ['"'],
    ]

    expected = [
        2,
        1,
        ValueError,
        0,
        0,
        1,
        3
    ]

    for i, test_case in enumerate(test_cases):
        try:
            print(f"Test case {i + 1}: {test_case}, expected {expected[i]}, got {is_first_string_literal(test_case)}")
        except ValueError as e:
            print(f"Test case {i + 1}: {test_case}, expected {expected[i]}, got ValueError: {e}")