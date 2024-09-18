from lexer import *
from parser import *

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
    else: raise ValueError
  
  def translate_pointer(self, node:ASTPointer) -> None:
    if not node.name in self.scope.labels:
      raise ValueError
    
    if node.name in self.scope.reservedVarLabels or node.name in self.scope.constLabels:
      self.start += f"mov rax, {node.name}\n"
    else: raise ValueError
  
  def translate_load_op_arg(self, node:ASTNode) -> None:
    self.translate_expr(node.b)
    self.start += "push rax\n"
    self.translate_expr(node.a)
  
  def translate_add(self, node:ASTAdd) -> None:
    self.translate_load_op_arg(node)
    self.start += "pop rbx\nadd rax, rbx\n"

  def translate_subtract(self, node:ASTSubtract) -> None:
    self.translate_load_op_arg(node)
    self.start += "pop rbx\nsub rax, rbx\n"

  def translate_multiply(self, node:ASTMultiply) -> None:
    self.translate_load_op_arg(node)
    self.start += "pop rbx\nmul rbx\n"

  def translate_divide(self, node:ASTDivide) -> None:
    self.translate_load_op_arg(node)
    self.start += "pop rbx\ndiv rbx\n"

  def translate_plussign(self, node:ASTPlussign) -> None:
    self.translate_expr(node.a)

  def translate_minussign(self, node:ASTMinussign) -> None:
    self.translate_expr(node.a)
    self.start += "neg eax\n"
  
  def translate_and(self, node:ASTAnd) -> None:
    self.translate_load_op_arg(node)
    self.start += "pop rbx\nand rax, rbx\n"
  
  def translate_or(self, node:ASTAnd) -> None:
    self.translate_load_op_arg(node)
    self.start += "pop rbx\nor rax, rbx\n"
  
  def translate_xor(self, node:ASTAnd) -> None:
    self.translate_load_op_arg(node)
    self.start += "pop rbx\nxor rax, rbx\n"

  def translate_not(self, node:ASTNot) -> None:
    self.translate_expr(node.a)
    self.start += "not rax\n"

  def translate_expr(self, node:ASTNode) -> None:
    if node.asttype == ASTT_ADD:
      self.translate_add(node)
    elif node.asttype == ASTT_SUBTRACT:
      self.translate_subtract(node)
    elif node.asttype == ASTT_MULTIPLY:
      self.translate_multiply(node)
    elif node.asttype == ASTT_DIVIDE:
      self.translate_divide(node)
    elif node.asttype == ASTT_PLUSSIGN:
      self.translate_plussign(node)
    elif node.asttype == ASTT_MINUSSIGN:
      self.translate_minussign(node)
    elif node.asttype == ASTT_NUM:
      self.translate_num(node)
    elif node.asttype == ASTT_VARCALL:
      self.translate_varcall(node)
    elif node.asttype == ASTT_POINTER:
      self.translate_pointer(node)
    elif node.asttype == ASTT_NOT:
      self.translate_not(node)
    elif node.asttype == ASTT_AND:
      self.translate_and(node)
    elif node.asttype == ASTT_OR:
      self.translate_or(node)
    elif node.asttype == ASTT_XOR:
      self.translate_xor(node)
    else: raise ValueError

  def translate_reserve(self, node:ASTReserve) -> None:
    if node.name in self.scope.labels:
      raise ValueError
    
    self.scope.labels.append(node.name)
    self.scope.reservedVarLabels.append(node.name)
    self.scope.reservedVars[node.name] = node.size

    self.sectionBss += f"{node.name}: resb {node.size}\n"

  def translate_set(self, node:ASTSet) -> None:
    if not node.name in self.scope.labels:
      raise ValueError
    
    self.translate_expr(node.value)
    
    if node.name in self.scope.reservedVarLabels:
      self.start += f"mov {SIZEATRIBUTES[self.scope.reservedVars[node.name]][2]} [{node.name}], {SIZEATRIBUTES[self.scope.reservedVars[node.name]][0]}\n"

  def translate_exit(self, node:ASTExit) -> None:
    self.translate_expr(node.value)

    self.start += f"mov rdi, rax\nmov rax, 60\nsyscall\n"
  
  def translate_const(self, node:ASTConst) -> None:
    if node.name in self.scope.labels:
      raise ValueError
    
    self.scope.labels.append(node.name)
    self.scope.constLabels.append(node.name)
    self.scope.consts[node.name] = node.size

    self.sectionData += f"{node.name}: {SIZEATRIBUTES[node.size][1]} {node.value}\n"