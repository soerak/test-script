#[BEN, TODO]: Implement mathematical functions in seperate script

#######################################
# CONSTANTS
#######################################

DIGITS      = '0123456789'

#######################################
# ERRORS
#######################################

#[BEN]: Generate Error based on the cause, get position of the error
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    #[BEN]: Save the resulting error, cause and position as result
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File line {self.pos_start.ln + 1}'
        return result

#[BEN]: Post the error, define error, details in the super_init
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

#######################################
# POSITION
#######################################

#[BEN]: Save the current index, line, column, ftxt in variables
#       what does ftxt mean/store?
class Position:
    def __init__(self, idx, ln, col, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.ftxt = ftxt

    #[BEN]: Advance the current column, index to read the next Token
    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        #[BEN]: Check if the current character is a nextline
        #       If so, goto the next line and reset the column
        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    #[BEN]: Return the current cursor information
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.ftxt)

#######################################
# TOKENS
#######################################

#[BEN]: TT means Token Type -> stored in type_
TT_INT		= 'INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'

#[BEN]: Store Token information in initialisation
class Token:
    def __init__(self, type_, value=None):
        self.type = type_ #[BEN]: Token Type
        self.value = value #[BEN]: Token Value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# LEXER
#######################################

#[BEN]: Define a class that reads and processes the Token
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(-1, 0, -1, text)
        self.current_char = None #[BEN]: Store the current character in a variable
        self.advance() #[BEN]: Advance one character in the command 
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    #[BEN]: Define a empty list of tokens, to be filled below
    def make_tokens(self):
        tokens = []

        #[BEN]: Check what the current char is, store it as a Token in the tokens[] list
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            
            #[BEN]: If a character isn't in the list above, it is illegal.
            #       Return the character, where it is and the error
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        #[BEN]: Return the tokens to the shell.py script
        return tokens, None

    #[BEN]: idk
    def make_number(self):
        num_str = ''
        dot_count = 0

        #[BEN]: Check if the given number is a INT or a FLOAT             vvv
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.': #[BEN]: Check if there is a dot somewhere in the number
                if dot_count == 1: break #[BEN]: Abort if there are multiple dots in the number (ILLEGAL)
                dot_count += 1 #[BEN]: Increment the dot count
                num_str += '.' #[BEN]: Store the dot for maths later on
            else:
                num_str += self.current_char #[BEN]: If there's no dot -> continue
            self.advance() #[BEN]: Goto next char

        if dot_count == 0: #[BEN]: If there's no dot in the number, it's an INT
            return Token(TT_INT, int(num_str))
        else: #[BEN]: Else it's a FLOAT
            return Token(TT_FLOAT, float(num_str))

#######################################
# RUN
#######################################

#[BEN]: Define the function that makes the code function
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()

    return tokens, error
