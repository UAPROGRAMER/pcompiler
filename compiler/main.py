from lexer import *
from parser import *
from translator import *
import sys
import os

def print_help() -> None:
  print("Help:\n  -o [str] : name of output file\n  -h : print help")
  sys.exit(0)

def parse_arguments(argv:list[str]) -> tuple[str,str]:
  inputfile:str = argv[1]
  outputfile:str
  for index, arg in enumerate(argv[2:].copy()):
    if arg == "-h":
      print_help()
    elif arg == "-o":
      outputfile = argv[index+3]
  
  if not (os.path.isfile(inputfile)):
    print("ERROR: first argument must be a valid input file.")
    exit(1)

  return inputfile, outputfile

def main(argc:int, argv:list[str]) -> int:
  if argc < 2:
    print("ERROR: not enough arguments. Use -h to show all flags and help.")
    exit(0)
  
  inputfile, outputfile = parse_arguments(argv)

  with open(inputfile, "r") as file:
    text:str = file.read()

  lexer:Lexer = Lexer(text)
  tokens:list[Token] = lexer.tokenize()

  parser:Parser = Parser(tokens)
  nodes:list[ASTNode] = parser.parse()

  translator:Translator = Translator(nodes)
  code:str = translator.translate()

  with open(outputfile, "w") as file:
    file.write(code)

  return 0

if __name__ == "__main__":
  sys.exit(main(len(sys.argv), sys.argv))