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
      self.next()
    return tokens
  
  def skip_white_space(self) -> None:
    while self.char in " \n":
      self.next()

  def id(self) -> Token:
    value:str = ""
    while self.char.isalnum():
      value += self.char
      self.next()
    return Token(TT_ID, value)

  def num(self) -> Token:
    value:str = ""
    while self.char.isnumeric():
      value += self.char
      self.next()
    return Token(TT_INT, value)