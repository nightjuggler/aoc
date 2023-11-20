import sys

# Usage: python3 18a-to-c.py < data/18.input > 18.c && clang -Ofast 18.c && ./a.out

def is_int(x): return x == str(int(x))
def is_reg(x): return len(x) == 1 and 97 <= ord(x) <= 122

def read_input():
	code = []
	regs = set()
	ops_no_y = ('snd', 'rcv')
	ops_int_x = ('snd', 'jgz')

	for i, line in enumerate(sys.stdin):
		op, x, *y = line.split()
		assert len(op) == 3
		if is_reg(x):
			regs.add(x)
		else:
			assert is_int(x)
			assert op in ops_int_x
		if not y:
			assert op in ops_no_y
		else:
			assert len(y) == 1
			assert op not in ops_no_y
			y, = y
			if is_reg(y):
				regs.add(y)
			else:
				assert is_int(y)

		if   op == 'snd': code.append(f'freq = {x};')
		elif op == 'set': code.append(f'{x} = {y};')
		elif op == 'add': code.append(f'{x} += {y};')
		elif op == 'mul': code.append(f'{x} *= {y};')
		elif op == 'mod': code.append(f'{x} %= {y};')
		elif op == 'rcv': code.append(f'if ({x}) break;')
		elif op == 'jgz': code.append(f'if ({x} > 0) {{ ip = {i} + {y}; goto top; }}')
		else:
			sys.exit(f'Unknown instruction on line {i+1}!')

	return code, regs

def main():
	code, regs = read_input()

	print('#include <stdio.h>')
	print('typedef long long int64;')
	print('int64 play()\n{')
	print('\tint ip = 0;')
	print('\tint64 freq = 0;')
	for reg in sorted(regs):
		print(f'\tint64 {reg} = 0;')

	print('top:\tswitch (ip) {')

	for i, line in enumerate(code):
		print(f'\t\tcase {i}:', line)

	print('\t}')
	print('\tprintf("ip = %d\\n", ip);')
	print('\treturn freq;\n}')
	print('int main(int argc, char *argv[])\n{')
	print('\tprintf("Part 1: %lld\\n", play());')
	print('\treturn 0;\n}')
main()
