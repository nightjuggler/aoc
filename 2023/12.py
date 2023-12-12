from functools import cache
import sys

@cache
def recurse(springs, groups):
	if not groups:
		return '#' not in springs
	n = len(springs)
	m = sum(groups) + len(groups) - 1
	j = groups[0]
	groups = groups[1:]
	result = 0
	for i in range(n - m + 1):
		if not ('.' in springs[i:j] or j < n and springs[j] == '#'):
			result += recurse(springs[j+1:], groups)
		if springs[i] == '#':
			break
		j += 1
	return result

def part1(data):
	springs, groups = data
	return recurse(springs, groups)

def part2(data):
	springs, groups = data
	return recurse('?'.join([springs]*5), groups*5)

def tuplify(line):
	springs, groups = line.split()
	return springs, tuple(map(int, groups.split(',')))

def main():
	conditions = list(map(tuplify, sys.stdin))
	print('Part 1:', sum(map(part1, conditions)))
	print('Part 2:', sum(map(part2, conditions)))
main()
