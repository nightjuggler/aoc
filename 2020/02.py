import sys
import re

def main():
	num_valid = 0
	line_number = 0
	line_pattern = re.compile('^([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)$')

	for line in sys.stdin:
		line_number += 1
		m = line_pattern.match(line)
		if not m:
			sys.exit('Line {} doesn\'t match pattern!'.format(line_number))

		min_count, max_count, letter, password = m.groups()
		min_count = int(min_count)
		max_count = int(max_count)
		count = 0
		for c in password:
			if c == letter:
				count += 1
		if min_count <= count <= max_count:
			num_valid += 1
			print(line[:-1], 'VALID')
		else:
			print(line[:-1], 'INVALID')

	print(num_valid, 'valid passwords')

if __name__ == '__main__':
	main()
