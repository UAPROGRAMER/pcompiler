from lexer import *
from parser import *

SIZEATRIBUTES:dict[int,tuple[str, str]] = {
  1:("al", "bl"),
  2:("ax", "bx"),
  4:("eax", "ebx"),
  8:("rax", "rbx")
}

class Scope:
  labels:list[str] = ["_start"]
  reservedVarLabels:list[str] = []
  reservedVars:dict[str,int] = {}

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
    return self.compile()

  def translate_num(self, node:ASTNum) -> None:
    self.start += f"mov rax, {node.value}\n"

  def translate_varcall(self, node:ASTVarcall) -> None:
    if not node.name in self.scope.labels:
      raise ValueError
    
    if node.name in self.scope.reservedVarLabels:
      self.start += f"xor rax, rax\nmov rax, [{node.name}]\n"
    else: raise ValueError
  
  def translate_add(self, node:ASTAdd) -> None:
    self.translate_expr(node.a)
    self.start += "push rax\n"
    self.translate_expr(node.b)
    self.start += "pop rbx\nadd rax, rbx\n"

  def translate_subtract(self, node:ASTSubtract) -> None:
    self.translate_expr(node.b)
    self.start += "push rax\n"
    self.translate_expr(node.a)
    self.start += "pop rbx\nsub rax, rbx\n"

  def translate_multiply(self, node:ASTMultiply) -> None:
    self.translate_expr(node.a)
    self.start += "push rax\n"
    self.translate_expr(node.b)
    self.start += "pop rbx\nmul rbx\n"

  def translate_divide(self, node:ASTDivide) -> None:
    self.translate_expr(node.b)
    self.start += "push rax\n"
    self.translate_expr(node.a)
    self.start += "pop rbx\ndiv rbx\n"

  def translate_plussign(self, node:ASTPlussign) -> None:
    self.translate_expr(node.a)

  def translate_minussign(self, node:ASTMinussign) -> None:
    self.translate_expr(node.a)
    self.start += "neg eax\n"

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
      self.start += f"mov [{node.name}], {SIZEATRIBUTES[self.scope.reservedVars[node.name]][0]}\n"

  def translate_exit(self, node:ASTExit) -> None:
    self.translate_expr(node.value)

    self.start += f"mov rdi, rax\nmov rax, 60\nsyscall\n"