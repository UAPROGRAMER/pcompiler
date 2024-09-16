sourcefilename = test.sourcecode
output = test
entrypoint = _start

$(output): assembley.asm
	nasm -f elf64 assembley.asm
	ld -e $(entrypoint) -o $(output) assembley.o

assembley.asm: $(sourcefilename)
	python3 compiler/main.py $(sourcefilename) -o assembley.asm

clear:
	rm assembley.asm assembley.o $(output)