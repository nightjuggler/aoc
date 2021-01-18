import sys
import re

def main(input_file):
	line_pattern = re.compile('^[1-9][0-9]*x[1-9][0-9]*x[1-9][0-9]*$')

	ribbon = 0
	for line_number, line in enumerate(input_file, start=1):
		if not line_pattern.match(line):
			sys.exit('Line {} doesn\'t match pattern!'.format(line_number))
		a, b, c = map(int, line.split('x'))
		ab = 2 * (a + b)
		ac = 2 * (a + c)
		bc = 2 * (b + c)
		ribbon += min(ab, ac, bc) + a * b * c

	print(ribbon)

if __name__ == '__main__':
	main(sys.stdin)
