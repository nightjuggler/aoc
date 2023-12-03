import sys

def read_input():
	digits = {}
	symbols = {}
	numbers = []
	num_index = 0
	num_digits = 0

	for y, line in enumerate(sys.stdin):
		line = line.rstrip()
		for x, c in enumerate(line):
			if 48 <= ord(c) <= 57:
				num_digits += 1
				digits[x, y] = num_index
			else:
				if num_digits:
					numbers.append(int(line[x-num_digits:x]))
					num_index += 1
					num_digits = 0
				if c != '.':
					symbols[x, y] = c
		if num_digits:
			numbers.append(int(line[-num_digits:]))
			num_index += 1
			num_digits = 0

	return numbers, digits, symbols

def part1(numbers, digits, symbols):
	nums = set(digits.get((ax, ay))
		for x, y in symbols
		for ay in range(y-1, y+2)
		for ax in range(x-1, x+2))
	nums.discard(None)
	return sum(numbers[i] for i in nums)

def part2(numbers, digits, symbols):
	def gear_ratio(x, y):
		nums = set(digits.get((ax, ay))
			for ay in range(y-1, y+2)
			for ax in range(x-1, x+2))
		nums.discard(None)
		if len(nums) == 2:
			i, j = nums
			return numbers[i] * numbers[j]
		return 0

	return sum(gear_ratio(x, y) for (x, y), c in symbols.items() if c == '*')

def main():
	data = read_input()
	print('Part 1:', part1(*data))
	print('Part 2:', part2(*data))
main()
