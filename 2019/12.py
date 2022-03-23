import argparse
from itertools import combinations
import re
import sys

def read_input():
	n = '(0|-?[1-9][0-9]*)'
	pattern = re.compile(f'^<x={n}, y={n}, z={n}>$')
	moons = []
	for line_num, line in enumerate(sys.stdin, start=1):
		if m := pattern.match(line):
			moons.append((list(map(int, m.groups())), [0, 0, 0]))
		else:
			sys.exit(f"Input line {line_num} doesn't match pattern!")
	return moons

def solve(moons, steps):
	combos = tuple(combinations(moons, 2))

	for step in range(steps):
		for (p1, v1), (p2, v2) in combos:
			for i, (x1, x2) in enumerate(zip(p1, p2)):
				if x1 < x2:
					v1[i] += 1
					v2[i] -= 1
				elif x2 < x1:
					v2[i] += 1
					v1[i] -= 1
		for p, v in moons:
			for i, vx in enumerate(v):
				p[i] += vx

	return sum(sum(map(abs, p)) * sum(map(abs, v)) for p, v in moons)

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('steps', nargs='?', type=int, default=1000)
	parser.add_argument('-v', '--verbose', action='store_true')
	args = parser.parse_args()

	steps = args.steps
	verbose = args.verbose

	moons = read_input()
	energy = solve(moons, steps)
	if verbose:
		def str_len(f):
			return len(str(f(f(f(p), f(v)) for p, v in moons)))
		width = max(str_len(min), str_len(max))
		def xyz_str(xyz):
			return ', '.join([f'{label}={value:{width}}' for label, value in zip('xyz', xyz)])
		print('After', steps, 'steps:')
		for p, v in moons:
			print(f'pos=<{xyz_str(p)}>, vel=<{xyz_str(v)}>')

	print('Part 1:', energy)

if __name__ == '__main__':
	main()
