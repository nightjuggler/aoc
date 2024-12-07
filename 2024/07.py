from math import log10
import operator
import re
import sys

def read_equations():
	pattern = re.compile('^[1-9][0-9]*:(?: [1-9][0-9]*){2,}$')
	eqs = []
	for line_num, line in enumerate(sys.stdin, start=1):
		if not pattern.match(line):
			sys.exit(f'Input line {line_num} doesn\'t match expected pattern!')
		target, nums = line.split(':')
		eqs.append((int(target), *map(int, nums.split())))
	return eqs

def sum_possible(eqs, ops):
	result = 0
	for target, a, *nums in eqs:
		values = {a}
		for b in nums:
			values = {op(a, b) for a in values if a <= target for op in ops}
		if target in values:
			result += target
	return result

def concat(a, b):
	return a * 10**(int(log10(b)) + 1) + b

def main():
	eqs = read_equations()
	print('Part 1:', sum_possible(eqs, (operator.add, operator.mul)))
	print('Part 2:', sum_possible(eqs, (operator.add, operator.mul, concat)))

main()
