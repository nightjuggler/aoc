import sys

def part1(rows):
	return sum(row[-1] - row[0] for row in rows)

def part2(rows):
	result_sum = 0
	for row_num, row in enumerate(rows):
		result = [a // b for i, a in enumerate(row[1:], start=1) for b in row[:i] if a % b == 0]
		if len(result) == 1:
			result_sum += result[0]
		else:
			sys.exit(f'Expected exactly one pair of evenly divisible numbers in row {row_num}!')
	return result_sum

def main():
	rows = [sorted(map(int, line.split())) for line in sys.stdin]
	print('Part 1:', part1(rows))
	print('Part 2:', part2(rows))

if __name__ == '__main__':
	main()
