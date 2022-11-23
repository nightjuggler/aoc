import sys

def part1(digits):
	answer = 0
	previous = digits[-1]
	for current in digits:
		if previous == current:
			answer += current
		previous = current
	return answer

def part2(digits):
	n = len(digits)
	offset = n // 2
	return sum(x for i, x in enumerate(digits, start=offset) if x == digits[i % n])

def main(f):
	digits = f.readline().strip()
	f.close()
	if not digits:
		sys.exit('Please enter a string of digits!')
	if digits.strip('0123456789'):
		sys.exit('Please enter only decimal digits!')

	digits = list(map(int, digits))

	print('Part 1:', part1(digits))
	print('Part 2:', part2(digits))

if __name__ == '__main__':
	main(sys.stdin)
