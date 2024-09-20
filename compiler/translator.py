from lexer import *
from parser import *

ASTExpr = ASTAdd|ASTSubtract|ASTMultiply|ASTDivide|ASTPlussign|ASTMinussign|ASTAnd|ASTOr|ASTXor|ASTNot|ASTNum|ASTVarcall|ASTPointer

SIZEATRIBUTES:dict[int,tuple[str, str]] = {
  1:("al", "db", "byte"),
  2:("ax", "dw", "word"),
  4:("eax", "dd", "dword"),
  8:("rax", "dq", "qword")
}

class Scope:
  labels:list[str] = ["_start"]
  reservedVarLabels:list[str] = []
  reservedVars:dict[str,int] = {}
  constLabels:list[str] = []
  consts:dict[str,int] = {}

  def __repr__(self) -> str:
    return f"{self.labels}, {self.reservedVarLabels}, {self.reservedVars}, {self.constLabels}, {self.consts}"

###

class Translator:
  def __init__(self, nodes:list[ASTNode]) -> None:
    self.nodes = nodes

    self.sectionData = "section .data\n"
    self.sectionBss = "section .bss\n"
    self.sectionText = "section .text\nglobal _start\n"
    self.start = "_start:\n"
    self.end = "mov rax, 60\nmov rdi, 0\nsyscall\n"

    self.cmptime = 0

    self.scope:Scope = Scope()

  def compile(self) -> str:
    return f"{self.sectionData}\n{self.sectionBss}\n{self.sectionText}\n{self.start}\n{self.end}\n"
  
  def translate(self) -> str:
    for node in self.nodes:
      if node.asttype == ASTT_RESERVE:
        self.translate_reserve(node)
      elif node.asttype == ASTT_SET:
        self.translate_set(node)
      elif node.asttype == ASTT_EXIT:
        self.translate_exit(node)
      elif node.asttype == ASTT_CONST:
        self.translate_const(node)
    return self.compile()
  
  def translate_num(self, node:ASTNum) -> None:
    self.start += f"mov rax, {node.value}\n"

  def translate_varcall(self, node:ASTVarcall) -> None:
    if not node.name in self.scope.labels:
      raise ValueError
    
    if node.name in self.scope.reservedVarLabels:
      self.start += f"xor rax, rax\nmov {SIZEATRIBUTES[self.scope.reservedVars[node.name]][0]}, {SIZEATRIBUTES[self.scope.reservedVars[node.name]][2]} [{node.name}]\n"
    elif node.name in self.scope.constLabels:
      self.start += f"xor rax, rax\nmov {SIZEATRIBUTES[self.scope.consts[node.name]][0]}, {SIZEATRIBUTES[self.scope.consts[node.name]][2]} [{node.name}]\n"
    else:
      raise ValueError

  def translate_pointer(self, node:ASTPointer) -> None:
    if not node.name in self.scope.labels:
      raise ValueError
    
    if node.name in self.scope.reservedVarLabels or node.name in self.scope.constLabels:
      self.start += f"mov rax, {node.name}\n"
    else:
      raise ValueError

  def load_operands(self, node:ASTAdd|ASTSubtract|ASTMultiply|ASTDivide|ASTModulus|ASTAnd|ASTOr|ASTXor) -> None:
    self.translate_expr(node.b)
    self.start += "push rax\n"
    self.translate_expr(node.a)
    self.start += "pop rbx\n"

  def translate_plussign(self, node:ASTPlussign) -> None:
    self.translate_expr(node.a)

  def translate_minussign(self, node:ASTMinussign) -> None:
    self.translate_expr(node.a)
    self.start += "neg rax\n"

  def translate_not(self, node:ASTNot) -> None:
    self.translate_expr(node.a)
    self.start += "not arx\n"

  def translate_add(self, node:ASTAdd) -> None:
    self.load_operands(node)
    self.start += "add rax, rbx\n"
  
  def translate_subtract(self, node:ASTSubtract) -> None:
    self.load_operands(node)
    self.start += "sub rax, rbx\n"

  def translate_multiply(self, node:ASTMultiply) -> None:
    self.load_operands(node)
    self.start += "mul rbx\n"

  def translate_divide(self, node:ASTDivide) -> None:
    self.load_operands(node)
    self.start += "div rbx\n"

  def translate_modulus(self, node:ASTModulus) -> None:
    self.load_operands(node)
    self.start += "xor rdx, rdx\ndiv rbx\nmov rax, rdx\n"

  def translate_and(self, node:ASTAnd) -> None:
    self.load_operands(node)
    self.start += "and rax, rbx\n"

  def translate_or(self, node:ASTOr) -> None:
    self.load_operands(node)
    self.start += "or rax, rbx\n"

  def translate_xor(self, node:ASTXor) -> None:
    self.load_operands(node)
    self.start += "xor rax, rbx\n"

  def translate_equal(self, node:ASTEqual) -> None:
    self.load_operands(node)
    self.start += f"cmp rax, rbx\nje cmptrue{self.cmptime}\nxor rax, rax\njmp cmpend{self.cmptime}\ncmptrue{self.cmptime}:\nmov rax, 1\ncmpend{self.cmptime}:\n"
    self.cmptime += 1
  
  def translate_not_equal(self, node:ASTEqual) -> None:
    self.load_operands(node)
    self.start += f"cmp rax, rbx\njne cmptrue{self.cmptime}\nxor rax, rax\njmp cmpend{self.cmptime}\ncmptrue{self.cmptime}:\nmov rax, 1\ncmpend{self.cmptime}:\n"
    self.cmptime += 1
  
  def translate_greater(self, node:ASTEqual) -> None:
    self.load_operands(node)
    self.start += f"cmp rax, rbx\njg cmptrue{self.cmptime}\nxor rax, rax\njmp cmpend{self.cmptime}\ncmptrue{self.cmptime}:\nmov rax, 1\ncmpend{self.cmptime}:\n"
    self.cmptime += 1
  
  def translate_lower(self, node:ASTEqual) -> None:
    self.load_operands(node)
    self.start += f"cmp rax, rbx\njl cmptrue{self.cmptime}\nxor rax, rax\njmp cmpend{self.cmptime}\ncmptrue{self.cmptime}:\nmov rax, 1\ncmpend{self.cmptime}:\n"
    self.cmptime += 1
  
  def translate_greaterequal(self, node:ASTEqual) -> None:
    self.load_operands(node)
    self.start += f"cmp rax, rbx\njge cmptrue{self.cmptime}\nxor rax, rax\njmp cmpend{self.cmptime}\ncmptrue{self.cmptime}:\nmov rax, 1\ncmpend{self.cmptime}:\n"
    self.cmptime += 1
  
  def translate_lowerequal(self, node:ASTEqual) -> None:
    self.load_operands(node)
    self.start += f"cmp rax, rbx\njle cmptrue{self.cmptime}\nxor rax, rax\njmp cmpend{self.cmptime}\ncmptrue{self.cmptime}:\nmov rax, 1\ncmpend{self.cmptime}:\n"
    self.cmptime += 1

  def translate_expr(self, node:ASTExpr) -> None:
    type = node.asttype
    if type == ASTT_NUM:
      self.translate_num(node)
    elif type == ASTT_VARCALL:
      self.translate_varcall(node)
    elif type == ASTT_POINTER:
      self.translate_pointer(node)
    elif type == ASTT_ADD:
      self.translate_add(node)
    elif type == ASTT_SUBTRACT:
      self.translate_subtract(node)
    elif type == ASTT_MULTIPLY:
      self.translate_multiply(node)
    elif type == ASTT_DIVIDE:
      self.translate_divide(node)
    elif type == ASTT_PLUSSIGN:
      self.translate_plussign(node)
    elif type == ASTT_MINUSSIGN:
      self.translate_minussign(node)
    elif type == ASTT_AND:
      self.translate_and(node)
    elif type == ASTT_OR:
      self.translate_or(node)
    elif type == ASTT_XOR:
      self.translate_xor(node)
    elif type == ASTT_NOT:
      self.translate_not(node)
    elif type == ASTT_MODULUS:
      self.translate_modulus(node)
    elif type == ASTT_EQUAL:
      self.translate_equal(node)
    elif type == ASTT_NOT_EQUAL:
      self.translate_not_equal(node)
    elif type == ASTT_GREATER:
      self.translate_greater(node)
    elif type == ASTT_LOWER:
      self.translate_lower(node)
    elif type == ASTT_GREATER_EQUAL:
      self.translate_greaterequal(node)
    elif type == ASTT_LOWER_EQUAL:
      self.translate_lowerequal(node)
    else:
      raise ValueError

  def translate_reserve(self, node:ASTReserve) -> None:
    if node.name in self.scope.labels:
      raise ValueError
    
    self.scope.labels.append(node.name)
    self.scope.reservedVarLabels.append(node.name)
    self.scope.reservedVars[node.name] = node.size

    self.sectionBss += f"{node.name}: resb {node.size}\n"
  
  def translate_set(self, node:ASTSet) -> None:
    if not (node.name in self.scope.labels):
      raise ValueError
    
    self.translate_expr(node.value)
    
    if node.name in self.scope.reservedVarLabels:
      self.start += f"mov {SIZEATRIBUTES[self.scope.reservedVars[node.name]][2]} [{node.name}], {SIZEATRIBUTES[self.scope.reservedVars[node.name]][0]}\n"
    else:
      raise ValueError
  
  def translate_const(self, node:ASTConst) -> None:
    if node.name in self.scope.labels:
      raise ValueError
    
    self.scope.labels.append(node.name)
    self.scope.constLabels.append(node.name)
    self.scope.consts[node.name] = node.size

    self.sectionData += f"{node.name}: {SIZEATRIBUTES[node.size][1]} {node.value}\n"
  
  def translate_exit(self, node:ASTExit) -> None:
    self.translate_expr(node.value)

    self.start += f"mov rdi, rax\nmov rax, 60\nsyscall\n"