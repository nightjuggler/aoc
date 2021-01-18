import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def main(input):
	line_number = 0
	rule_pattern = re.compile('^([a-z][a-z]*(?: [a-z][a-z]*)*): '
		'([1-9][0-9]*)-([1-9][0-9]*) or '
		'([1-9][0-9]*)-([1-9][0-9]*)$')

	rules = []

	for line in input:
		line_number += 1
		m = rule_pattern.match(line)
		if not m:
			if line == '\n':
				break
			err('Line {} doesn\'t match rule pattern!', line_number)

		field, lo1, hi1, lo2, hi2 = m.groups()
		rules.append((field, ((int(lo1), int(hi1)), (int(lo2), int(hi2)))))

	line = next(input)
	line_number += 1
	if line != 'your ticket:\n':
		err('Expected "your ticket:" on line {}!', line_number)

	line = next(input)
	line_number += 1
	my_ticket = map(int, line.split(','))

	line = next(input)
	line_number += 1
	if line != '\n':
		err('Expected an empty line on line {}!', line_number)

	line = next(input)
	line_number += 1
	if line != 'nearby tickets:\n':
		err('Expected "nearby tickets:" on line {}!', line_number)

	invalid_sum = 0
	for line in input:
		line_number += 1
		ticket = map(int, line.split(','))
		for value in ticket:
			valid = False
			for field, ranges in rules:
				for lo, hi in ranges:
					if lo <= value <= hi:
						valid = True
						break
				if valid:
					break
			if not valid:
				invalid_sum += value
	print(invalid_sum)

if __name__ == '__main__':
	main(sys.stdin)
