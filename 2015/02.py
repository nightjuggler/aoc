import sys
import re

def main(input_file):
	line_pattern = re.compile('^[1-9][0-9]*x[1-9][0-9]*x[1-9][0-9]*$')

	area = 0
	for line_number, line in enumerate(input_file, start=1):
		if not line_pattern.match(line):
			sys.exit('Line {} doesn\'t match pattern!'.format(line_number))
		a, b, c = map(int, line.split('x'))
		ab = a * b
		ac = a * c
		bc = b * c
		area += 2 * (ab + ac + bc) + min(ab, ac, bc)

	print(area)

if __name__ == '__main__':
	main(sys.stdin)
