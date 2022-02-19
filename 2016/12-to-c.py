import sys

# Usage: python3 12-to-c.py < data/12.input > 12.c && clang -Ofast 12.c && ./a.out

# >>> TIMEFMT="%*E seconds"
# >>> time (python3 12-to-c.py < data/12.input > 12.c && clang -Ofast 12.c && ./a.out)
# Part 1: 318007
# Part 2: 9227661
# 0.169 seconds

# Note: See zshmisc(1) for the zsh time command and zshparam(1) for TIMEFMT

def valid_reg(x): return x in ('a', 'b', 'c', 'd')
def valid_int(x): return x == str(int(x))

def read_input():
	code = []
	jump_targets = set()
	lines = list(sys.stdin)
	num_lines = len(lines)

	for i, line in enumerate(lines):
		op, *args = line.split()
		if op == 'cpy':
			y, x = args
			assert valid_reg(x)
			assert valid_reg(y) or valid_int(y)
			code.append(f'{x} = {y};')
		elif op == 'jnz':
			x, y = args
			assert valid_reg(x) or valid_int(x)
			assert valid_int(y)
			y = i + int(y)
			assert 0 <= y != i
			if y > num_lines:
				y = num_lines
			code.append(f'if ({x}) goto l{y};')
			jump_targets.add(y)
		elif op == 'inc':
			x, = args
			assert valid_reg(x)
			code.append(f'{x} += 1;')
		elif op == 'dec':
			x, = args
			assert valid_reg(x)
			code.append(f'{x} -= 1;')
		else:
			sys.exit(f'Unknown instruction on line {i+1}!')

	return code, jump_targets

def main():
	code, jump_targets = read_input()

	print('''#include <stdio.h>
int solve(int c)
{
	int a = 0;
	int b = 0;
	int d = 0;
''')
	for i, line in enumerate(code):
		if i in jump_targets:
			print(f'l{i}:', end='')
		print('\t', line, sep='')
	i += 1
	if i in jump_targets:
		print(f'l{i}:', end='')
	print('''
	return a;
}
int main(int argc, char **argv)
{
	printf("Part 1: %d\\n", solve(0));
	printf("Part 2: %d\\n", solve(1));
	return 0;
}''')

if __name__ == '__main__':
	main()
