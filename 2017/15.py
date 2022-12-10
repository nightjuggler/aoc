import re
import sys

# This is much slower than the C version (15.c) (~18 seconds vs. ~0.5 seconds)!

line_pattern = re.compile('^Generator (A|B) starts with ([1-9][0-9]*)$')

def readline(f, label):
	m = line_pattern.match(f.readline().strip())
	if not m or m.group(1) != label:
		sys.exit(f'Could not read starting value for generator {label}!')
	return int(m.group(2))

def part1(a, b):
	m = 1<<16
	n = 0
	for _ in range(40_000_000):
		a = a * 16807 % 2147483647
		b = b * 48271 % 2147483647
		if a % m == b % m: n += 1
	return n

def part2(a, b):
	m = 1<<16
	n = 0
	for _ in range(5_000_000):
		while (a := a * 16807 % 2147483647) % 4: pass
		while (b := b * 48271 % 2147483647) % 8: pass
		if a % m == b % m: n += 1
	return n

def main(f):
	a = readline(f, 'A')
	b = readline(f, 'B')
	print('Part 1:', part1(a, b))
	print('Part 2:', part2(a, b))

main(sys.stdin)
