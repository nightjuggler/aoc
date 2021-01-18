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

		i, j, letter, password = m.groups()
		i = int(i)
		j = int(j)
		assert i > 0 and j > i and len(password) >= j
		if (password[i-1] == letter) ^ (password[j-1] == letter):
			num_valid += 1
			print(line[:-1], 'VALID')
		else:
			print(line[:-1], 'INVALID')

	print(num_valid, 'valid passwords')

if __name__ == '__main__':
	main()
