import sys

def part1(lines):
	symbols = set()
	numbers = []
	num_digits = 0

	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			if 48 <= ord(c) <= 57:
				num_digits += 1
			else:
				if num_digits:
					x1 = x - num_digits
					numbers.append((y, x1, x, int(line[x1:x])))
					num_digits = 0
				if c != '.':
					symbols.add((y, x))
		if num_digits:
			x = len(line)
			x1 = x - num_digits
			numbers.append((y, x1, x, int(line[x1:x])))
			num_digits = 0

	return sum(n for y, x1, x2, n in numbers
		if (y, x1-1) in symbols or (y, x2) in symbols or
			any((y-1, x) in symbols or (y+1, x) in symbols for x in range(x1-1, x2+1)))

def part2(lines):
	gears = set()
	digits = {}
	numbers = []
	num_index = 0
	num_digits = 0

	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			if 48 <= ord(c) <= 57:
				num_digits += 1
				digits[y, x] = num_index
			else:
				if num_digits:
					numbers.append(int(line[x-num_digits:x]))
					num_index += 1
					num_digits = 0
				if c == '*':
					gears.add((y, x))
		if num_digits:
			numbers.append(int(line[-num_digits:]))
			num_index += 1
			num_digits = 0

	sum_gear_ratios = 0
	for y, x in gears:
		adj_nums = set(digits.get((ay, ax))
			for ay in range(y-1, y+2)
			for ax in range(x-1, x+2))
		adj_nums.remove(None)
		if len(adj_nums) == 2:
			i, j = adj_nums
			sum_gear_ratios += numbers[i] * numbers[j]
	return sum_gear_ratios

def main():
	lines = [line.rstrip() for line in sys.stdin]
	print('Part 1:', part1(lines))
	print('Part 2:', part2(lines))
main()
