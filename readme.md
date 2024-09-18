# Pcompiler
Compile source code into x86_64 linux assembley and assemble with NASM assembler. Made for linux.

# keywords
- res/reserve [size], [name];
- const [size], [name], [const value];
- set [name], [expr];
- exit [expr];
# var sizes
- u8
- u16
- u32
- u64
# operations
## low priority
- a + b : add
- a - b : subtract
## normal priority
- a * b : multiply
- a / b : divide
- a & b : and
- a | b : or
- a ^ b : xor
## high priority
- -a : minus sign
- +a : plus sign
- !a : not
- &[name] : pointer
