# from lark import Lark, UnexpectedCharacters, UnexpectedEOF, UnexpectedToken, ParseError

# ebnf = """
# program: clause_list [query]

# clause_list: clause+

# clause: predicate ("." | ":-" predicate_list ".")

# query: "?-" predicate_list "."

# predicate_list: predicate ("," predicate)*

# predicate: atom ["(" term_list ")"]

# term_list: term ("," term)*

# term: atom | variable | structure | numeral

# structure: atom "(" term_list ")"

# atom: small_atom | "'"string"'"

# small_atom: lowercase_char [character_list]

# variable: uppercase_char [character_list]

# character_list: (alphanumeric)+

# alphanumeric: lowercase_char | uppercase_char | digit

# lowercase_char: "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"

# uppercase_char: "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "_"

# numeral: (digit)+

# digit: "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

# string: (character)+

# character: alphanumeric | special

# special: "+" | "-" | "*" | "/" | "\\\\" | "^" | "~" | ":" | "." | "?" | "\\|" | "#" | "$" | "&" | " "

# %import common.WS
# %ignore WS
# """

# def parse_file(file_content):
#     try:
#         parser.parse(file_content)
#         return "No errors found."
#     except UnexpectedCharacters as e:
#         return f"Unexpected character {e.char} at line {e.line}, column {e.column}."
#     except UnexpectedToken as e:
#         return f"Unexpected token {e.token} at line {e.line}, column {e.column}. Expecting one of {', '.join(e.expected)}."
#     except UnexpectedEOF as e:
#         return f"Unexpected end of file. Expecting one of {', '.join(e.expected)}."
#     except SyntaxError as e:
#         return str(e)
#     except Exception as e:
#         return str(e)


# # def parse_file(file_content):
# #     try:
# #         parser.parse(file_content)
# #         print( "No errors found.")
# #     except UnexpectedCharacters as e:
# #         print( f"Unexpected character {e.char} at line {e.line}, column {e.column}.")
# #     except UnexpectedToken as e:
# #         if str(type(e.token)) == "str":
# #             print( f"Unexpected string '{e.token.value}' at line {e.line}, column {e.column}.")
# #         elif str(type(e.token)) == 'int':
# #             print( f"Unexpected number'{e.token.value}' at line {e.line}, column {e.column}.")
# #         else:
# #             print( f"Unexpected token {e.token} at line {e.line}, column {e.column}. Expecting one of {', '.join(e.expected)}.")
# #     except UnexpectedEOF as e:
# #         print( f"Unexpected end of file. Expecting one of {', '.join(e.expected)}.")
# #     except SyntaxError as e:
# #         print( str(e))
# #     except Exception as e:
# #         print( str(e))
    
# parser = Lark(ebnf, start='program')

# i = 1
# contents = []
# while True:
#     try:
#         with open(f'{i}.txt', 'r') as file:
#             file_content = file.read()
#             result = parse_file(file_content)
#             print(f"File {i}.txt: {result}")
#         i += 1
#     except FileNotFoundError:
#         if i == 1:
#             raise FileNotFoundError(f'Missing file: {i}.txt')
#         break

from lark import Lark, UnexpectedInput, UnexpectedCharacters, UnexpectedEOF, UnexpectedToken, ParseError

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

parser = Lark(ebnf, start='program')

# def parse_file(file_content):
#     offset = 0
#     errors = []
#     while offset < len(file_content):
#         print(f"{offset} : {len(file_content)}")
#         try:
#             # Parse starting from the current offset
#             parser.parse(file_content[offset:])
#             offset += 1
#         except (UnexpectedCharacters, UnexpectedToken, UnexpectedInput) as e:
#             error_message = f"4.txt: {type(e)} error at line {e.line}, column {e.column}"
#             print(error_message)
#             errors.append(error_message)
#             offset 
#          # Custom error recovery based on the type of error
#             if isinstance(e, UnexpectedToken):
#                 print(e)
#             else:
#                 # Skip to the next line or a few characters ahead
#                 if '\n' in file_content[offset:]:
#                     offset += file_content[offset:].index('\n') + 1
#                 else:
#                     offset = len(file_content)

# def parse_file(file_content):
#     offset = 0
#     while offset < len(file_content):
#         try:
#             print(parser.parse(file_content).pretty())
#             offset += 1
#             print( "No errors found.")
#         except UnexpectedCharacters as e:
#             print( f"Unexpected character {e.char} at line {e.line}, column {e.column}.")
#             offset += e.column
#         except UnexpectedToken as e:
#             if str(type(e.token)) == "str":
#                 print( f"Unexpected string '{e.token.value}' at line {e.line}, column {e.column}.")
#             elif str(type(e.token)) == 'int':
#                 print( f"Unexpected number'{e.token.value}' at line {e.line}, column {e.column}.")
#             else:
#                 print( f"Unexpected token {e.token} at line {e.line}, column {e.column}. Expecting one of {', '.join(e.expected)}.")
#             offset += e.column
#         except UnexpectedEOF as e:
#             print( f"Unexpected end of file. Expecting one of {', '.join(e.expected)}.")
#             offset += e.column
#         except SyntaxError as e:
#             print( str(e))
#         except Exception as e:
#             print( str(e))

# i = 1
# # while True:
# try:
#     with open(f'4.txt', 'r') as file:
#         file_content = file.read()
#         result = parse_file(file_content)
#         print(f"File 4.txt: {result}")
# except FileNotFoundError:
#     if i == 1:
#         raise FileNotFoundError(f'Missing file: 4.txt')
# except EOFError:
#     print(f"End of file reached for file {i}.txt.")
#     #continue
# finally:
#     i += 1

#%%

from lark import Lark, UnexpectedInput, UnexpectedCharacters, UnexpectedEOF, UnexpectedToken, ParseError

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


# def parse_file(file_content):
#     errors = []
#     try:
#         parser.parse(file_content)
#     except UnexpectedCharacters as e:
#         errors.append(f"Unexpected character {e.char} at line {e.line}, column {e.column}.")
#     except UnexpectedToken as e:
#         if e.token.type == "STRING":
#             errors.append(f"Unexpected string '{e.token.value}' at line {e.line}, column {e.column}.")
#         elif e.token.type == 'NUMBER':
#             errors.append(f"Unexpected number '{e.token.value}' at line {e.line}, column {e.column}.")
#         else:
#             errors.append(f"Unexpected token {e.token} at line {e.line}, column {e.column}. Expecting one of {', '.join(e.expected)}.")
#     except UnexpectedEOF as e:
#         errors.append(f"Unexpected end of file. Expecting one of {', '.join(e.expected)}.")
#     except SyntaxError as e:
#         errors.append(str(e))
#     except Exception as e:
#         errors.append(str(e))
#     if errors:
#         return "\n".join(errors)
#     else:
#         return "No errors found."

def parse_file(file_content):
    errors = []
    try:
        parser.parse(file_content)
    except UnexpectedCharacters as e:
        errors.append(f"Unexpected character {e.char} at line {e.line}, column {e.column}.")
    except UnexpectedToken as e:
        if e.token.type == "STRING":
            errors.append(f"Unexpected string '{e.token.value}' at line {e.line}, column {e.column}.")
        elif e.token.type == 'NUMBER':
            errors.append(f"Unexpected number '{e.token.value}' at line {e.line}, column {e.column}.")
        else:
            errors.append(f"Unexpected token {e.token} at line {e.line}, column {e.column}. Expecting one of {', '.join(e.expected)}.")
    except UnexpectedEOF as e:
        errors.append(f"Unexpected end of file. Expecting one of {', '.join(e.expected)}.")
    except ParseError as e:
        errors.append(f"Parse error: {str(e)}")
    except Exception as e:
        errors.append(str(e))
    if errors:
        return "\n".join(errors)
    else:
        return "No errors found."
    
parser = Lark(ebnf, start='program', ambiguity='explicit')

i = 1
while True:
    try:
        with open(f'{i}.txt', 'r') as file:
            file_content = file.read()
            errors = parse_file(file_content)
            print(f"File {i}.txt: {errors}")
            # if errors != "No errors found.":
            #     print(f"File {i}.txt: {errors}")
            # else:
            #     print(f"File {i}.txt: {errors}")
            i += 1
    except FileNotFoundError:
        if i == 1:
            raise FileNotFoundError(f'Missing file: {i}.txt')
        break
#%%
from lark import Lark, UnexpectedInput, UnexpectedCharacters, UnexpectedEOF, UnexpectedToken, ParseError

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

def parse_program(input_text):
    try:
        # Parse the input text through Lark
        parser.parse(input_text)
        return "Syntactically correct"
    except UnexpectedCharacters as e:
        return f"Syntax error: Unexpected character {e.char} at line {e.line}, column {e.column}."
    except UnexpectedEOF as e:
        return f"Syntax error: Unexpected end of file. Expected one of {', '.join(e.expected)}."
    except exceptions.LarkError as e:
        # General LarkError if something else goes wrong
        return str(e)
    
input_text = """criminal(X :- american(X), weapon(Y), nation(Z),
 hostile(Z), sells(X,Z,Y).
owns(nono,msl(nono)). missile(msl(nono)).
sells(west,nono,M) :- owns(nono,M), missile(M).
weapon(W) :- missile(W).
hostile(H) :- enemy(H,america).
american(west).
nation(nono). enemy(nono,america).
nation(america).
?- criminal(Who).
"""
result = parse_program(input_text)
print(result)

#%%

from lark import Lark, UnexpectedCharacters, UnexpectedEOF, exceptions

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

parser = Lark(ebnf, start='program', ambiguity='explicit')

def custom_error_message(e, context):
    if '(' in context and ')' not in context:
        return f"Syntax error: Missing ')' near '{context}'"
    if ')' in context and '(' not in context:
        return f"Syntax error: Missing '(' before '{context}'"
    if hasattr(e, 'state'):
        rule = str(e.state)
    else:
        rule = "unknown"
    #return f"Syntax error: Unexpected character {e.char} at line {e.line}, column {e.column} near '{context}'."
    return f"Syntax error at rule '{rule}': Unexpected character '{e.char}' at line {e.line}, column {e.column} near '{context}'."

def parse_program(input_text):
    try:
        parser.parse(input_text)
        return "Syntactically correct"
    except UnexpectedCharacters as e:
        context_start = max(0, e.pos_in_stream - 10)
        context_end = min(len(input_text), e.pos_in_stream + 10)
        context = input_text[context_start:context_end]
        return custom_error_message(e, context)
    except UnexpectedEOF as e:
        return f"Syntax error: Unexpected end of file. Expected one of {', '.join(e.expected)}."
    except exceptions.LarkError as e:
        return str(e)


# Example usage
input_text = """say(N, From, To) :- write('move disc '), write(N), write(' from '),
 write(From), write(' to '), write(To), nl.
hanoi(N) :- move(N, left, center, right).
move(0, _, _, _).
move(N, From, To, Using) :- is(M, N-1), move(M, From, Using, To),
 say(N, From, To), move(M, Using, To, From).
?- hanoi(3).
"""
result = parse_program(input_text)
print(result)

