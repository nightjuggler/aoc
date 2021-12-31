from collections import deque
import re
import sys

def read_input():
	n = '([1-9A-Z]{1,3})'
	line_pattern = re.compile(f'^{n}\\){n}$')

	orbits = {}
	for line_num, line in enumerate(sys.stdin, start=1):
		m = line_pattern.match(line)
		if not m:
			print(f"Input line {line_num} doesn't match the expected pattern!")
			return None
		a, b = m.groups()
		if b in orbits:
			print(f"Input line {line_num}: Object {b} already orbits {orbits[b]}!")
			return None
		orbits[b] = a
	return orbits

def part1(orbits):
	orbiters = {}
	for b, a in orbits.items():
		orbiters.setdefault(a, []).append(b)

	total_orbits = 0
	q = deque()
	q.append(('COM', 1))

	while q:
		a, n = q.popleft()
		for b in orbiters.get(a, ()):
			total_orbits += n
			q.append((b, n + 1))

	print('Part 1:', total_orbits)

def path_to_com(orbits, b):
	path = []
	while b != 'COM':
		b = orbits[b]
		path.append(b)
	return path

def part2(orbits):
	if 'YOU' not in orbits: return
	if 'SAN' not in orbits: return

	you_path = path_to_com(orbits, 'YOU')
	santa_path = path_to_com(orbits, 'SAN')
	santa_path = {a: d for d, a in enumerate(santa_path)}

	for d, a in enumerate(you_path):
		if a in santa_path:
			print('Part 2:', d + santa_path[a])
			break

def main():
	orbits = read_input()
	if not orbits: return

	part1(orbits)
	part2(orbits)

if __name__ == '__main__':
	main()
