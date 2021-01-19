import re
import sys

def max_score(properties, ingredients):
	N = len(ingredients)
	if N == 0:
		return 0

	assert all([len(values) == N for values in properties])

	best_score = 0
	best_spoons = spoons = [0] * N
	calories = properties.pop()

	def compute_score():
		nonlocal best_score, best_spoons
		if sum([s * v for s, v in zip(spoons, calories)]) != 500:
			return
		score = 1
		for values in properties:
			score *= max(0, sum([s * v for s, v in zip(spoons, values)]))
		if score > best_score:
			best_score = score
			best_spoons = spoons.copy()

	def recurse(i, spoons_left):
		if i + 1 == N:
			spoons[i] = spoons_left
			compute_score()
			return
		for j in range(spoons_left + 1):
			spoons[i] = j
			recurse(i + 1, spoons_left - j)

	recurse(0, 100)
	for ingredient, amount in zip(ingredients, best_spoons):
		print('{:4}'.format(amount), ingredient)
	return best_score

def main():
	property_names = ('capacity', 'durability', 'flavor', 'texture', 'calories')
	property_values = [[] for n in property_names]
	ingredient_names = []

	line_pattern = re.compile('^[A-Z][a-z]+(?:[A-Z][a-z]+)?: [a-z]+ -?[0-9](?:, [a-z]+ -?[0-9]){4}$')

	for line_number, line in enumerate(sys.stdin, start=1):
		if not line_pattern.match(line):
			sys.exit('Line {} doesn\'t match pattern!'.format(line_number))
		ingredient, line = line.split(': ')
		ingredient_names.append(ingredient)
		for prop, name, values in zip(line.split(', '), property_names, property_values):
			prop, value = prop.split(' ')
			assert prop == name
			values.append(int(value))

	print(max_score(property_values, ingredient_names))

if __name__ == '__main__':
	main()
