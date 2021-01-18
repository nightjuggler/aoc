import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def main():
	line_pattern = re.compile('^((?:[a-z]+ )+)\\(contains ([a-z]+(?:, [a-z]+)*)\\)$')
	line_number = 0

	ingredients = {}
	allergens = {}

	for line in sys.stdin:
		line_number += 1
		m = line_pattern.match(line)
		if not m:
			err('Line {} doesn\'t match pattern!', line_number)

		ingredient_list = m.group(1)[:-1].split(' ')
		allergen_list = m.group(2).split(', ')

		for ingredient in ingredient_list:
			ingredients[ingredient] = ingredients.get(ingredient, 0) + 1

		for allergen in allergen_list:
			s = allergens.get(allergen)
			if s is None:
				allergens[allergen] = set(ingredient_list)
			else:
				s &= set(ingredient_list)

	a = set()
	for s in allergens.values():
		a |= s

	s = 0
	for ingredient in sorted(set(ingredients) - a):
		n = ingredients[ingredient]
		print(n, 'x', ingredient)
		s += n
	print(s)

if __name__ == '__main__':
	main()
