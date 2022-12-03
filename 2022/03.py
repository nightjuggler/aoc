import sys

def part1(lines, priority):
	total = 0
	for line in lines:
		assert not len(line) % 2
		n = len(line) // 2
		chars = set(line[:n])
		chars.intersection_update(line[n:])
		assert len(chars) == 1
		total += priority[chars.pop()]
	return total

def part2(lines, priority):
	assert not len(lines) % 3
	total = 0
	for i in range(0, len(lines), 3):
		chars = set(lines[i])
		chars.intersection_update(lines[i+1], lines[i+2])
		assert len(chars) == 1
		total += priority[chars.pop()]
	return total

def main():
	ord_a = ord('a')
	ord_A = ord('A')
	priority = {}
	for i in range(26):
		priority[chr(ord_a + i)] = i + 1
		priority[chr(ord_A + i)] = i + 27

	lines = list(map(str.strip, sys.stdin))

	print('Part 1:', part1(lines, priority))
	print('Part 2:', part2(lines, priority))

main()
