from math import prod
import sys

def opfn(op):
	if op == '+': return sum
	assert op == '*'
	return prod

def part1(lines):
	lines = [line.split() for line in lines]
	return sum(opfn(args[-1])(map(int, args[:-1])) for args in zip(*lines))

def part2(lines):
	result = 0
	op = None
	nums = []
	for col in map(''.join, zip(*lines)):
		if not col.strip():
			result += op(nums)
			op = None
			nums = []
		elif col[-1] == ' ':
			nums.append(int(col))
		else:
			assert not op
			op = opfn(col[-1])
			nums.append(int(col[:-1]))
	assert not (op or nums)
	return result

def main():
	lines = list(sys.stdin)
	print('Part 1:', part1(lines))
	print('Part 2:', part2(lines))
main()
