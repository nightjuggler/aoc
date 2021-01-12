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
		rules.append((field, int(lo1), int(hi1), int(lo2), int(hi2)))

	line = next(input)
	line_number += 1
	if line != 'your ticket:\n':
		err('Expected "your ticket:" on line {}!', line_number)

	line = next(input)
	line_number += 1
	my_ticket = list(map(int, line.split(',')))
	num_fields = len(my_ticket)

	line = next(input)
	line_number += 1
	if line != '\n':
		err('Expected an empty line on line {}!', line_number)

	line = next(input)
	line_number += 1
	if line != 'nearby tickets:\n':
		err('Expected "nearby tickets:" on line {}!', line_number)

	possible_rules = None

	for line in input:
		line_number += 1
		ticket = list(map(int, line.split(',')))
		if len(ticket) != num_fields:
			err('Expected {} fields (got {}) on line {}!', num_fields, len(ticket), line_number)

		possible = [set([i for i, (field, lo1, hi1, lo2, hi2) in enumerate(rules)
			if (lo1 <= value <= hi1) or (lo2 <= value <= hi2)]) for value in ticket]
		if not all(possible):
			continue

		if possible_rules is None:
			possible_rules = possible
			continue

		for i, (p, q) in enumerate(zip(possible_rules, possible)):
			p &= q
			if not p:
				err('Field {} has no possibilities!', i)

	possible_fields = [set() for r in rules]
	for field_index, p in enumerate(possible_rules):
		for rule_index in p:
			possible_fields[rule_index].add(field_index)

#	for i, p in enumerate(possible_fields):
#		print('Rule', i, '=>', p)
#	for i, p in enumerate(possible_rules):
#		print('Field', i, '=>', p)

	field_rules = [None] * num_fields
	changed = True
	while changed:
		changed = False
		for field_index, p in enumerate(possible_rules):
			if len(p) == 1:
				rule_index = p.pop()
				if field_rules[field_index] is not None:
					err('A rule for field {} was already determined!', field_index)
				field_rules[field_index] = rule_index
				q = possible_fields[rule_index]
				q.remove(field_index)
				for field_index in q:
					p = possible_rules[field_index]
					p.remove(rule_index)
					if not p:
						err('Removed the last possible rule ({}) for field {}!',
							rule_index, field_index)
				q.clear()
				changed = True

	assert not any(possible_rules)
	assert not any(possible_fields)
	assert None not in field_rules

	product = 1
	for rule_index, value in zip(field_rules, my_ticket):
		name = rules[rule_index][0]
		if name.startswith('departure'):
			print(name, value)
			product *= value
	print(product)

if __name__ == '__main__':
	main(sys.stdin)
