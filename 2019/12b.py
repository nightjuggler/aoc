import re
import sys

def read_input():
	n = '(0|-?[1-9][0-9]*)'
	pattern = re.compile(f'^<x={n}, y={n}, z={n}>$')
	moons = []
	for line_num, line in enumerate(sys.stdin, start=1):
		if m := pattern.match(line):
			moons.append(list(map(int, m.groups())))
		else:
			sys.exit(f"Input line {line_num} doesn't match pattern!")
	return moons

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

def solve(moons):
	steps = 1
	for xs in zip(*moons):
		xvs = tuple((x, 0) for x in xs)
		seen = {}
		step = 0
		while xvs not in seen:
			seen[xvs] = step
			new_xvs = []
			for x, v in xvs:
				v += sum(d // abs(d) for x2, v2 in xvs if (d := x2 - x))
				new_xvs.append((x + v, v))
			xvs = tuple(new_xvs)
			step += 1
		assert seen[xvs] == 0
		steps *= step // gcd(steps, step)
	return steps

if __name__ == '__main__':
	print('Part 2:', solve(read_input()))
