ASTT_RESERVE = "reserve"
ASTT_SET = "set"
ASTT_EXIT = "exit"
ASTT_NUM = "num"
ASTT_VARCALL = "varcall"
ASTT_CONST = "const"
ASTT_POINTER = "pointer"

ASTT_ADD = "add"
ASTT_SUBTRACT = "subtract"
ASTT_MULTIPLY = "multiply"
ASTT_DIVIDE = "divide"
ASTT_PLUSSIGN = "plussign"
ASTT_MINUSSIGN = "minussigns"
ASTT_AND = "and"
ASTT_OR = "or"
ASTT_NOT = "not"
ASTT_XOR = "xor"
ASTT_MODULUS = "modulus"
ASTT_EQUAL = "equal"
ASTT_GREATER = "greater"
ASTT_LOWER = "lower"
ASTT_GREATER_EQUAL = "greater_equal"
ASTT_LOWER_EQUAL = "lower_equal"
ASTT_NOT_EQUAL = "not_equal"

class ASTNode:
  asttype:str

class ASTNum(ASTNode):
  asttype:str = ASTT_NUM
  def __init__(self, value:str) -> None:
    self.value:str = value

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.value})"

class ASTVarcall(ASTNode):
  asttype:str = ASTT_VARCALL
  def __init__(self, name:str) -> None:
    self.name:str = name

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.name})"

class ASTReserve(ASTNode):
  asttype:str = ASTT_RESERVE
  def __init__(self, name:str, size:int) -> None:
    self.name:str = name
    self.size:int = size

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.name}, {self.size})"

class ASTSet(ASTNode):
  asttype:str = ASTT_SET
  def __init__(self, name:str, value) -> None:
    self.name:str = name
    self.value = value

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.name}, {self.value})"

class ASTExit(ASTNode):
  asttype:str = ASTT_EXIT
  def __init__(self, value) -> None:
    self.value = value
  
  def __repr__(self) -> str:
    return f"({self.asttype}, {self.value})"

class ASTConst(ASTNode):
  asttype:str = ASTT_CONST
  def __init__(self, name:str, size:int, value:str) -> None:
    self.name = name
    self.size = size
    self.value = value
  
  def __repr__(self) -> str:
    return f"({self.asttype}, {self.name}, {self.size}, {self.value})"

class ASTPointer(ASTNode):
  asttype:str = ASTT_POINTER
  def __init__(self, name:str) -> None:
    self.name = name
  
  def __repr__(self) -> str:
    return f'({self.asttype}, {self.name})'

###

class ASTAdd(ASTNode):
  asttype:str = ASTT_ADD
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"

class ASTSubtract(ASTNode):
  asttype:str = ASTT_SUBTRACT
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"

class ASTMultiply(ASTNode):
  asttype:str = ASTT_MULTIPLY
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"

class ASTDivide(ASTNode):
  asttype:str = ASTT_DIVIDE
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"

class ASTPlussign(ASTNode):
  asttype:str = ASTT_PLUSSIGN
  def __init__(self, a) -> None:
    self.a = a

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a})"

class ASTMinussign(ASTNode):
  asttype:str = ASTT_MINUSSIGN
  def __init__(self, a) -> None:
    self.a = a

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a})"

class ASTAnd(ASTNode):
  asttype:str = ASTT_AND
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b
  
  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"
  
class ASTOr(ASTNode):
  asttype:str = ASTT_OR
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b
  
  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"

class ASTNot(ASTNode):
  asttype:str = ASTT_NOT
  def __init__(self, a) -> None:
    self.a = a
  
  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a})"

class ASTXor(ASTNode):
  asttype:str = ASTT_XOR
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b
  
  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"

class ASTModulus(ASTNode):
  asttype:str = ASTT_MODULUS
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b
  
  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"

class ASTEqual(ASTNode):
  asttype:str = ASTT_EQUAL
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"

class ASTGreater(ASTNode):
  asttype:str = ASTT_GREATER
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"

class ASTLower(ASTNode):
  asttype:str = ASTT_LOWER
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"

class ASTGreaterequal(ASTNode):
  asttype:str = ASTT_GREATER_EQUAL
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"

class ASTLowerequal(ASTNode):
  asttype:str = ASTT_LOWER_EQUAL
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"

class ASTNotequal(ASTNode):
  asttype:str = ASTT_NOT_EQUAL
  def __init__(self, a, b) -> None:
    self.a = a
    self.b = b

  def __repr__(self) -> str:
    return f"({self.asttype}, {self.a}, {self.b})"