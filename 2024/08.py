from collections import defaultdict
import re
import sys

def part1(antennas, size):
	antinodes = set()
	for locations in antennas.values():
		for i, (x, y) in enumerate(locations):
			for x2, y2 in locations[i+1:]:
				dx = x2 - x
				dy = y2 - y
				antinodes.add((x2 + dx, y2 + dy))
				antinodes.add((x - dx, y - dy))
	return sum(1 for x, y in antinodes if 0 <= x < size and 0 <= y < size)

def part2(antennas, size):
	antinodes = set()
	for locations in antennas.values():
		for i, (x, y) in enumerate(locations):
			for x2, y2 in locations[i+1:]:
				a = dx = x2 - x
				b = dy = y2 - y
				while b:
					a, b = b, a % b
				dx //= a
				dy //= a
				x2 = x
				y2 = y
				while True:
					antinodes.add((x2, y2))
					x2 += dx
					if not 0 <= x2 < size: break
					y2 += dy
					if not 0 <= y2 < size: break
				x2 = x
				y2 = y
				while True:
					x2 -= dx
					if not 0 <= x2 < size: break
					y2 -= dy
					if not 0 <= y2 < size: break
					antinodes.add((x2, y2))
	return len(antinodes)

def main():
	lines = [line.strip() for line in sys.stdin]
	size = len(lines)
	assert size and all(len(line) == size for line in lines)
	pattern = re.compile('^[.0-9A-Za-z]+$')
	assert all(pattern.match(line) for line in lines)

	antennas = defaultdict(list)
	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			if c != '.':
				antennas[c].append((x, y))
	print('Part 1:', part1(antennas, size))
	print('Part 2:', part2(antennas, size))

main()
