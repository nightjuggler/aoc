import sys

def sum_values(lines, digits):
	def find_digit(line, irange):
		for i in irange:
			for s, slen, value in digits:
				if line[i:i+slen] == s:
					return value
		return None

	answer = 0
	for linenum, line in enumerate(lines, start=1):
		linelen = len(line)
		digit1 = find_digit(line, range(linelen))
		if digit1 is None:
			print(f'No digit on line {linenum} ({line})!')
			return None
		digit2 = find_digit(line, range(linelen-1, -1, -1))
		answer += digit1*10 + digit2
	return answer

def main():
	digits = [(s, 1, i) for i, s in enumerate('123456789', start=1)]
	words = 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'
	words = [(s, len(s), i) for i, s in enumerate(words, start=1)]
	lines = [line.strip() for line in sys.stdin]
	print('Part 1:', sum_values(lines, digits))
	print('Part 2:', sum_values(lines, digits + words))
main()
