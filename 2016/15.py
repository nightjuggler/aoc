import re
import sys

def read_input():
	n = '(0|[1-9][0-9]*)'
	pattern = re.compile(f'^Disc #{n} has {n} positions; at time=0, it is at position {n}\\.$')
	discs = []
	for line_num, line in enumerate(sys.stdin, start=1):
		m = pattern.match(line)
		if not m:
			sys.exit(f"Syntax error on input line {line_num}!")
		disc, num_pos, pos = map(int, m.groups())
		if not (disc == line_num and num_pos > 0 and 0 <= pos < num_pos):
			sys.exit(f"Syntax error on input line {line_num}!")
		discs.append((pos + disc, num_pos))
	return discs

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

def solve(discs):
	t = 0
	step = 1
	for pos, num_pos in discs:
		d = gcd(num_pos, step)
		if (pos + t) % d:
			return None
		while (pos + t) % num_pos:
			t += step
		step *= num_pos // d
	return t

if __name__ == '__main__':
	print(solve(read_input()))
