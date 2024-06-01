from lark import Lark, UnexpectedCharacters, UnexpectedEOF, UnexpectedToken, ParseError

ebnf = """
program: clause_list [query]

clause_list: clause+

clause: predicate ("." | ":-" predicate_list ".")

query: "?-" predicate_list "."

predicate_list: predicate ("," predicate)*

predicate: atom ["(" term_list ")"]

term_list: term ("," term)*

term: atom | variable | structure | numeral

structure: atom "(" term_list ")"

atom: small_atom | "'"string"'"

small_atom: lowercase_char [character_list]

variable: uppercase_char [character_list]

character_list: (alphanumeric)+

alphanumeric: lowercase_char | uppercase_char | digit

lowercase_char: "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"

uppercase_char: "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "_"

numeral: (digit)+

digit: "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

string: (character)+

character: alphanumeric | special

special: "+" | "-" | "*" | "/" | "\\\\" | "^" | "~" | ":" | "." | "?" | "\\|" | "#" | "$" | "&" | " "

%import common.WS
%ignore WS
"""

#%%
def parse_file(file_content):
    try:
        parser.parse(file_content)
        return "No errors found."
    except UnexpectedCharacters as e:
        return f"Unexpected character {e.char} at line {e.line}, column {e.column}."
    except UnexpectedToken as e:
        if e.token.type == "STRING":
            return f"Unexpected string '{e.token.value}' at line {e.line}, column {e.column}."
        elif e.token.type == 'NUMBER':
            return f"Unexpected number'{e.token.value}' at line {e.line}, column {e.column}."
        else:
            return f"Unexpected token {e.token} at line {e.line}, column {e.column}. Expecting one of {', '.join(e.expected)}."
    except UnexpectedEOF as e:
        return f"Unexpected end of file. Expecting one of {', '.join(e.expected)}."
    except SyntaxError as e:
        return str(e)
    except Exception as e:
        return str(e)
    
parser = Lark(ebnf, start='program')

i = 1
contents = []
while True:
    try:
        with open(f'{i}.txt', 'r') as file:
            file_content = file.read()
            result = parse_file(file_content)
            print(f"File {i}.txt: {result}")
    except FileNotFoundError:
        if i == 1:
            raise FileNotFoundError(f'Missing file: {i}.txt')
        break
    except EOFError:
        print(f"End of file reached for file {i}.txt.")
        i += 1
        continue
    

#%%
import lark

def parse_file(file_content):
    errors = []
    try:
        parser.parse(file_content)
    except UnexpectedCharacters as e:
        errors.append(f"Unexpected character '{e.char}' at line {line_number}, column {e.column}.")
    except UnexpectedToken as e:
        if e.token.type == "STRING":
            errors.append(f"Unexpected string '{e.token.value}' at line {line_number}, column {e.column}.")
        elif e.token.type == 'NUMBER':
            errors.append(f"Unexpected number '{e.token.value}' at line {line_number}, column {e.column}.")
        else:
            errors.append(f"Unexpected token {e.token} at line {line_number}, column {e.column}. Expecting one of {', '.join(e.expected)}.")
    except UnexpectedEOF as e:
        errors.append(f"Unexpected end of file at line {line_number}, column {e.column}.")
    except lark.exceptions.UnexpectedInput as e:
        errors.append(f"Unexpected input at line {line_number}, column {e.column}: {e.error_info}")
    except lark.exceptions.VisitError as e:
        errors.append(f"Visit error: {str(e)}")
    except lark.exceptions.LarkError as e:
        errors.append(f"Lark error: {str(e)}")
    except lark.exceptions.ParseError as e:
        errors.append(f"Parse error: {str(e)}")
    except lark.exceptions.GrammarError as e:
        errors.append(f"Grammar error: {str(e)}")
    except Exception as e:
        errors.append(str(e))

    return errors

def error_handle(e):
    pass#if e.token == ''
parser = Lark(ebnf, start='program', parser = 'lalr')

i = 1
while True and i < 7:
    try:
        with open(f'{i}.txt', 'r') as file:
            file_content = file.read()
            if not file_content.strip():
                print(f"File {i}.txt: Empty file.")
            else:
                errors = parse_file(file_content)
                if errors:
                    print(f"File {i}.txt: {len(errors)} found")
                    for error in errors:
                        print(error)
                    print('\n')
                else:
                    print(f"File {i}.txt: No errors found.")
            i += 1
    except (IOError, OSError) as e:
        print(f"Error reading file {i}.txt: {str(e)}")
        i += 1
    except FileNotFoundError:
        if i == 1:
            raise FileNotFoundError(f'Missing file: {i}.txt')
        break

#%%
from lark import Lark

# Create the Lark parser
parser = Lark(ebnf, start='program')

# Parse a text file
def parse_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        return parser.parse(text)

# Example usage
parsed_tree = parse_file('4.txt')
print(parsed_tree)