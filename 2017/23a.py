import sys

# Usage: python3 23a.py < data/23.input > 23.c && clang -Ofast 23.c && ./a.out

def is_int(x): return x == str(int(x))
def is_reg(x): return len(x) == 1 and 97 <= ord(x) <= 104 # a through h

def read_input():
	code = []
	regs = set()

	for i, line in enumerate(sys.stdin):
		op, x, y = line.split()
		if is_reg(x):
			regs.add(x)
		else:
			assert is_int(x) and op == 'jnz'
		if is_reg(y):
			regs.add(y)
		else:
			assert is_int(y)

		if   op == 'set': code.append(f'{x} = {y};')
		elif op == 'sub': code.append(f'{x} -= {y};')
		elif op == 'mul': code.append(f'{x} *= {y}; mul++;')
		elif op == 'jnz': code.append(f'if ({x}) {{ ip = {i} + {y}; goto top; }}')
		else:
			sys.exit(f'Unknown instruction on line {i+1}!')

	return code, regs

def main():
	code, regs = read_input()

	print('#include <stdio.h>')
	print('typedef long long int64;')
	print('typedef unsigned int uint;')
	print('uint run()\n{')
	print('\tint ip = 0;')
	print('\tuint mul = 0;')

	for reg in sorted(regs):
		print(f'\tint64 {reg} = 0;')

	print('top:\tswitch (ip) {')

	for i, line in enumerate(code):
		print(f'\t\tcase {i}:', line)

	print('\t}')
	print('\treturn mul;\n}')
	print('int main(int argc, char *argv[])\n{')
	print('\tprintf("Part 1: %u\\n", run());')
	print('\treturn 0;\n}')
main()
