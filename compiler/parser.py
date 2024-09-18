from lexer import *
from astt import *

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
    while not (self.token is None):
      if self.token.type != TT_ID:
        raise ValueError
      if self.token.value == "res":
        self.nodes.append(self.parse_reserve())
      elif self.token.value == "const":
        self.nodes.append(self.parse_const())
      elif self.token.value == "set":
        self.nodes.append(self.parse_set())
      elif self.token.value == "exit":
        self.nodes.append(self.parse_exit())
      else:
        raise ValueError
    return self.nodes
  
  def parse_expr(self) -> ASTAdd|ASTSubtract:
    result = self.parse_term()

    while (not (self.token is None)) and (self.token.type in (TT_PLUS, TT_MINUS)):
      if self.token.type == TT_PLUS:
        self.next()
        result = ASTAdd(result, self.parse_term())
      elif self.token.type == TT_MINUS:
        self.next()
        result = ASTSubtract(result, self.parse_term())
      else:
        raise ValueError
    return result

  def parse_term(self) -> ASTMultiply|ASTDivide|ASTModulus:
    result = self.parse_bitwise()

    while (not (self.token is None)) and (self.token.type in (TT_MULTIPLY, TT_DIVIDE, TT_MODULUS)):
      if self.token.type == TT_MULTIPLY:
        self.next()
        result = ASTMultiply(result, self.parse_bitwise())
      elif self.token.type == TT_DIVIDE:
        self.next()
        result = ASTDivide(result, self.parse_bitwise())
      elif self.token.type == TT_MODULUS:
        self.next()
        result = ASTModulus(result, self.parse_bitwise())
      else:
        raise ValueError
    
    return result

  def parse_bitwise(self) -> ASTAnd|ASTOr|ASTXor:
    result = self.parse_factor()

    while (not (self.token is None)) and (self.token.type in (TT_ANP, TT_OR, TT_XOR)):
      if self.token.type == TT_ANP:
        self.next()
        result = ASTAnd(result, self.parse_factor())
      elif self.token.type == TT_OR:
        self.next()
        result = ASTOr(result, self.parse_factor())
      elif self.token.type == TT_XOR:
        self.next()
        result = ASTXor(result, self.parse_factor())
      else:
        raise ValueError
    
    return result

  def parse_factor(self) -> ASTNum|ASTVarcall|ASTPointer|ASTPlussign|ASTMinussign|ASTNot:
    if self.token is None:
      raise ValueError
    elif self.token.type == TT_LPAREN:
      self.next()
      result = self.parse_expr()
      if self.token.type != TT_RPAREN:
        raise ValueError
      self.next()
      
      return result
    elif self.token.type == TT_INT:
      result = ASTNum(self.token.value)
      self.next()
      return result
    elif self.token.type == TT_ID:
      result = ASTVarcall(self.token.value)
      self.next()
      return result
    elif self.token.type == TT_ANP:
      self.next()
      result = ASTPointer(self.parse_factor())
      return result
    elif self.token.type == TT_PLUS:
      self.next()
      result = ASTPlussign(self.parse_factor())
      return result
    elif self.token.type == TT_MINUS:
      self.next()
      result = ASTMinussign(self.parse_factor())
      return result
    elif self.token.type == TT_NOT:
      self.next()
      result = ASTNot(self.parse_factor())
      return result
    else:
      raise ValueError
  
  def parse_reserve(self) -> ASTReserve:
    self.expect(TT_ID)
    varsize = VARTYPEDICT[self.token.value]

    self.expect(TT_COMMA)
    self.expect(TT_ID)

    varname = self.token.value
    self.expect(TT_SEMI)
    self.next()

    return ASTReserve(varname, varsize)
  
  def parse_const(self) -> ASTConst:
    self.expect(TT_ID)
    varsize = VARTYPEDICT[self.token.value]

    self.expect(TT_COMMA)
    self.expect(TT_ID)

    varname = self.token.value
    self.expect(TT_COMMA)
    self.next()

    if self.token.type == TT_INT:
      value = self.token.value
    else:
      raise ValueError
    
    self.expect(TT_SEMI)
    self.next()
    return ASTConst(varname, varsize, value)
  
  def parse_set(self) -> ASTSet:
    self.expect(TT_ID)
    varname = self.token.value

    self.expect(TT_COMMA)
    self.next()
    value = self.parse_expr()
    self.next()

    return ASTSet(varname, value)

  def parse_exit(self) -> ASTExit:
    self.next()
    value = self.parse_expr()
    self.next()
    
    return ASTExit(value)