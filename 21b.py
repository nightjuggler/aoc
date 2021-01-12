import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def main():
	line_pattern = re.compile('^((?:[a-z]+ )+)\\(contains ([a-z]+(?:, [a-z]+)*)\\)$')
	line_number = 0
	allergens = {}

	for line in sys.stdin:
		line_number += 1
		m = line_pattern.match(line)
		if not m:
			err('Line {} doesn\'t match pattern!', line_number)

		ingredient_list = m.group(1)[:-1].split(' ')
		allergen_list = m.group(2).split(', ')

		for allergen in allergen_list:
			s = allergens.get(allergen)
			if s is None:
				allergens[allergen] = set(ingredient_list)
			else:
				s &= set(ingredient_list)

	d = []
	while allergens:
		for a, s in allergens.items():
			if len(s) == 1:
				allergen = a
				ingredient = s.pop()
				break
		else:
			err('Cannot determine ingredient for remaining allergens!')

		print('-', ingredient, 'contains', allergen)

		d.append((allergen, ingredient))
		del allergens[allergen]
		for s in allergens.values():
			s.discard(ingredient)

	print(','.join([ingredient for allergen, ingredient in sorted(d)]))

if __name__ == '__main__':
	main()
