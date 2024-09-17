from lexer import *
from astt import *

#VARTYPE = tuple[str, int]
#VARTYPE_LONG:VARTYPE = "long", 8

VARTYPEDICT:dict[str,int] = {
  "u64":8,
  "u32":4,
  "u16":2,
  "u8":1
}

class Parser:
  def __init__(self, tokens:list[Token]) -> None:
    self.tokens = tokens
    self.token = None
    self.index = -1
    self.nodes:list[ASTNode] = []
    self.next()
  
  def next(self) -> None:
    self.index += 1
    self.token = self.tokens[self.index] if self.index < len(self.tokens) else None
  
  def expect(self, type:str) -> None:
    self.next()
    if self.token is None or self.token.type != type:
      raise ValueError
  
  def parse(self) -> list[ASTNode]:
    while not self.token is None:
      if self.token is None:
        continue

      if self.token.value in ["reserve", "res"]:
        self.nodes.append(self.parse_reserve())
      elif self.token.value == "set":
        self.nodes.append(self.parse_set())
      elif self.token.value == "exit":
        self.nodes.append(self.parse_exit())
      elif self.token.value == "const":
        self.nodes.append(self.parse_const())
      else: raise ValueError

      self.next()
    return self.nodes

  def parse_num(self) -> ASTNum:
    return ASTNum(self.token.value)

  def parse_varcall(self) -> ASTVarcall:
    return ASTVarcall(self.token.value)
  
  def parse_pointer(self) -> ASTPointer:
    return ASTPointer(self.token.value)

  def parse_expr(self) -> ASTAdd|ASTSubtract:
    result = self.parse_term()

    while (not self.token is None) and (self.token.type in (TT_PLUS, TT_MINUS)):
      if self.token.type == TT_PLUS:
        self.next()
        result = ASTAdd(result, self.parse_term())
      elif self.token.type == TT_MINUS:
        self.next()
        result = ASTSubtract(result, self.parse_term())
      else: raise ValueError
    
    return result

  def parse_term(self) -> ASTMultiply|ASTDivide:
    result = self.parse_factor()
    self.next()
    
    while (not self.token is None) and (self.token.type in (TT_MULTIPLY, TT_DIVIDE)):
      if self.token.type == TT_MULTIPLY:
        self.next()
        result = ASTMultiply(result, self.parse_factor())
        self.next()
      elif self.token.type == TT_DIVIDE:
        self.next()
        result = ASTDivide(result, self.parse_factor())
        self.next()
      else: raise ValueError
    
    return result
        
  def parse_factor(self) -> ASTNum|ASTVarcall:
    if self.token.type == TT_LPAREN:
      self.next()
      result = self.parse_expr()

      if self.token.type != TT_RPAREN:
        raise ValueError
      
      return result

    elif self.token.type == TT_INT:
      return self.parse_num()
    elif self.token.type == TT_ID:
      return self.parse_varcall()
    elif self.token.type == TT_PLUS:
      self.next()
      return ASTPlussign(self.parse_factor())
    elif self.token.type == TT_MINUS:
      self.next()
      return ASTMinussign(self.parse_factor())
    elif self.token.type == TT_POINTER:
      self.next()
      return self.parse_pointer()
    else: raise ValueError

  def parse_reserve(self) -> ASTReserve:
    self.expect(TT_ID)

    varsize = VARTYPEDICT[self.token.value]

    self.expect(TT_COMMA)
    self.expect(TT_ID)

    varname = self.token.value

    self.expect(TT_SEMI)

    return ASTReserve(varname, varsize)

  def parse_set(self) -> ASTSet:
    self.expect(TT_ID)

    varname = self.token.value

    self.expect(TT_COMMA)
    self.next()

    value = self.parse_expr()

    return ASTSet(varname, value)

  def parse_exit(self) -> ASTExit:
    self.next()

    value = self.parse_expr()

    return ASTExit(value)

  def parse_const(self) -> ASTConst:
    self.expect(TT_ID)

    varsize = VARTYPEDICT[self.token.value]

    self.expect(TT_COMMA)
    self.expect(TT_ID)

    varname = self.token.value

    self.expect(TT_COMMA)
    self.expect(TT_INT)

    value = self.token.value

    self.expect(TT_SEMI)

    return ASTConst(varname, varsize, value)