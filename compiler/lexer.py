TT_ID = "id"
TT_INT = "int"
TT_LPAREN = "left_paren"
TT_RPAREN = "right_paren"
TT_LCURLY = "left_curly"
TT_RCURLY = "right_curly"
TT_COLUMN = "column"
TT_SEMI = "semi"
TT_PLUS = "plus"
TT_MINUS = "minus"
TT_MULTIPLY = "multiply"
TT_DIVIDE = "divide"
TT_COMMA = "coma"
TT_ANP = "anp"
TT_OR = "or"
TT_NOT = "not"
TT_XOR = "xor"
TT_MODULUS = "modulus"
TT_GREATER = "bigger"
TT_LOWER = "lower"
TT_EQUAL = "equal"

class Token:
  type:int
  value:str|int
  def __init__(self, type:str, value:str = None) -> None:
    self.type = type
    self.value = value

  def __repr__(self) -> str:
    return f"({self.type},{self.value})"

class Lexer:
  text:str
  index:int
  char:str
  def __init__(self, text:str) -> None:
    self.text = text
    self.index = -1
    self.char = None

    self.next()

  def next(self) -> None:
    self.index += 1
    self.char = self.text[self.index] if self.index < len(self.text) else None
  
  def tokenize(self) -> list[Token]:
    tokens:list[Token] = []

    while self.char != None:
      if self.char in " \n":
        self.next()
        continue

      if self.char.isalpha():
        tokens.append(self.id())
        continue
      elif self.char.isnumeric():
        tokens.append(self.num())
        continue
      
      match self.char:
        case "(":
          tokens.append(Token(TT_LPAREN))
        case ")":
          tokens.append(Token(TT_RPAREN))
        case "{":
          tokens.append(Token(TT_LCURLY))
        case "}":
          tokens.append(Token(TT_RCURLY))
        case ":":
          tokens.append(Token(TT_COLUMN))
        case ";":
          tokens.append(Token(TT_SEMI))
        case "+":
          tokens.append(Token(TT_PLUS))
        case "-":
          tokens.append(Token(TT_MINUS))
        case "*":
          tokens.append(Token(TT_MULTIPLY))
        case "/":
          tokens.append(Token(TT_DIVIDE))
        case ",":
          tokens.append(Token(TT_COMMA))
        case "'":
          tokens.append(self.character())
        case "&":
          tokens.append(Token(TT_ANP))
        case "|":
          tokens.append(Token(TT_OR))
        case "!":
          tokens.append(Token(TT_NOT))
        case "^":
          tokens.append(Token(TT_XOR))
        case "%":
          tokens.append(Token(TT_MODULUS))
        case ">":
          tokens.append(Token(TT_GREATER))
        case "<":
          tokens.append(Token(TT_LOWER))
        case "=":
          tokens.append(Token(TT_EQUAL))
      self.next()
    return tokens
  
  def skip_white_space(self) -> None:
    while self.char in " \n":
      self.next()

  def id(self) -> Token:
    value:str = ""
    while self.char.isalnum() or self.char == "_":
      value += self.char
      self.next()
    return Token(TT_ID, value)

  def num(self) -> Token:
    value:str = ""
    while self.char.isnumeric():
      value += self.char
      self.next()
    return Token(TT_INT, value)
  
  def character(self) -> Token:
    self.next()
    value:str = str(ord(self.char))
    self.next()

    if self.char != "'":
      raise ValueError

    return Token(TT_INT, value)