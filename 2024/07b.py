from math import log10
import re
import sys

def read_equations():
	pattern = re.compile('^[1-9][0-9]*:(?: [1-9][0-9]*){2,}$')
	eqs = []
	for line_num, line in enumerate(sys.stdin, start=1):
		if not pattern.match(line):
			sys.exit(f'Input line {line_num} doesn\'t match expected pattern!')
		target, nums = line.split(':')
		eqs.append((int(target), list(map(int, nums.split()))))
	return eqs

def main():
	sum1 = sum2 = 0
	for target, nums in read_equations():
		values = [nums[0]]
		for b in nums[1:]:
			new_values = []
			for a in values:
				if a > target: continue
				new_values.append(a + b)
				new_values.append(a * b)
			values = new_values
		if target in values:
			sum1 += target
			continue
		values = [nums[0]]
		for b in nums[1:]:
			new_values = []
			for a in values:
				if a > target: continue
				new_values.append(a + b)
				new_values.append(a * b)
				new_values.append(a * 10**(int(log10(b)) + 1) + b)
			values = new_values
		if target in values:
			sum2 += target

	print('Part 1:', sum1)
	print('Part 2:', sum1 + sum2)

main()
