import sys

# Usage: python3 25-to-c.py < data/25.input > 25.c && clang -Ofast 25.c && ./a.out

# >>> TIMEFMT="%*E seconds"
# >>> time (python3 25-to-c.py < data/25.input > 25.c && clang -Ofast 25.c && ./a.out)
# 182
# 0.185 seconds

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
			assert 0 <= y
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
		elif op == 'out':
			x, = args
			assert valid_reg(x) or valid_int(x)
			code.append(f'if ({x} != x) return 0;' '''
	x = !x;
	for (int i = 0; i < num_states; ++i) {
		int *state = states[i];
		if (a == state[0] && b == state[1] && c == state[2] && d == state[3])
			return 1;
	}
	if (num_states < 64) {
		int *state = states[num_states++];
		state[0] = a;
		state[1] = b;
		state[2] = c;
		state[3] = d;
	} else {
		printf("Increase the maximum number of states!\\n");
		return 1;
	}''')
		else:
			sys.exit(f'Unknown instruction on line {i+1}!')

	return code, jump_targets

def main():
	code, jump_targets = read_input()

	print('''#include <stdio.h>
int solve(int a)
{
	int x = 0;
	int b = 0;
	int c = 0;
	int d = 0;

	int states[64][4];
	int num_states = 0;
''')
	for i, line in enumerate(code):
		if i in jump_targets:
			print(f'l{i}:', end='')
		print('\t', line, sep='')
	i += 1
	if i in jump_targets:
		print(f'l{i}:', end='')
	print('''
	return 0;
}
int main(int argc, char **argv)
{
	int n = 0;
	while (!solve(++n));
	printf("%d\\n", n);
	return 0;
}''')

if __name__ == '__main__':
	main()
