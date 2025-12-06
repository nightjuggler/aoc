from math import prod
import sys

opfn = {'+': sum, '*': prod}

def part1(lines):
	lines = [line.split() for line in lines]
	return sum(opfn[args[-1]](map(int, args[:-1])) for args in zip(*lines))

def part2(lines):
	ops = lines.pop().split()
	problems = []
	numbers = []
	for col in zip(*lines):
		if col := ''.join(col).strip():
			numbers.append(int(col))
		else:
			problems.append(numbers)
			numbers = []
	return sum(opfn[op](numbers) for op, numbers in zip(ops, problems))

def main():
	lines = list(sys.stdin)
	print('Part 1:', part1(lines))
	print('Part 2:', part2(lines))
main()
