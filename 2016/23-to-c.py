import sys

# Usage: python3 23-to-c.py < data/23.input > 23.c && clang -Ofast 23.c && ./a.out

# >>> TIMEFMT="%*E seconds"
# >>> time (python3 23-to-c.py < data/23.input > 23.c && clang -Ofast 23.c && ./a.out)
# Part 1: 14160
# Part 2: 479010720
# 1.589 seconds

# Note: See zshmisc(1) for the zsh time command and zshparam(1) for TIMEFMT

def valid_reg(x): return x in ('a', 'b', 'c', 'd')
def valid_int(x): return x == str(int(x))

def read_input():
	code = []
	toggles = []
	lines = list(sys.stdin)
	num_lines = len(lines)

	for i, line in enumerate(lines):
		op, *args = line.split()
		if op == 'cpy':
			x, y = args
			assert valid_reg(x) or valid_int(x)
			assert valid_reg(y)
			code.append(f'if (t[{i}]) {{ if ({x}) {{ i = {i} + {y}; goto top; }} }} else {y} = {x};')
		elif op == 'jnz':
			x, y = args
			assert valid_reg(x) or valid_int(x)
			j, e = ((f'{i} + {y}', f'if (t[{i}]) {y} = {x}; else')
				if valid_reg(y) else (i + int(y), f'if (!t[{i}])'))
			code.append(f'{e} if ({x}) {{ i = {j}; goto top; }}')
		elif op == 'inc':
			x, = args
			assert valid_reg(x)
			code.append(f'if (t[{i}]) {x} -= 1; else {x} += 1;')
		elif op == 'dec':
			x, = args
			assert valid_reg(x)
			code.append(f'if (t[{i}]) {x} += 1; else {x} -= 1;')
		elif op == 'tgl':
			x, = args
			j, e = ((f'{i} + {x}', f'\n\t\t\telse if (t[{i}]) {x} -= 1; else {x} += 1;')
				if valid_reg(x) else (i + int(x), ''))
			code.append(f'if (t[{i}] == 2) '
				f'{{ int j = {j}; if (j >= 0 && j < {num_lines}) t[j] = !t[j]; }}{e}')
			toggles.append(i)
		else:
			sys.exit(f'Unknown instruction on line {i+1}!')

	return code, toggles

def main():
	code, toggles = read_input()

	print('''#include <stdio.h>
int solve(int a)
{
	int b = 0;
	int c = 0;
	int d = 0;
	int i = 0;''')

	print(f'\tunsigned char t[{len(code)}] = {{0}};')

	for i in toggles:
		print(f'\tt[{i}] = 2;')

	print('top:\tswitch (i) {')

	for i, line in enumerate(code):
		print(f'\t\tcase {i}:', line)

	print('''\t}
	return a;
}
int main(int argc, char **argv)
{
	printf("Part 1: %d\\n", solve(7));
	printf("Part 2: %d\\n", solve(12));
	return 0;
}''')

if __name__ == '__main__':
	main()
