import sys

def shortest(cities, distances):
	min_d = None
	max_i = len(cities) - 1
	if max_i < 0:
		return 0

	def add_distances():
		d = 0
		p = cities[0]
		for i in range(1, max_i + 1):
			c = cities[i]
			d += distances[(p, c)]
			p = c
#		print(' -> '.join(cities), '=', d)
		return d

	def recurse(i):
		nonlocal min_d
		if i == max_i:
			d = add_distances()
			if min_d is None or d < min_d:
				min_d = d
			return
		recurse(i + 1)
		for j in range(i + 1, max_i + 1):
			cities[i], cities[j] = cities[j], cities[i]
			recurse(i + 1)
			cities[i], cities[j] = cities[j], cities[i]

#	print(cities)
	recurse(0)
	return min_d

def main(input_file):
	cities = set()
	distances = {}
	for line in input_file:
		a, to, b, eq, d = line.split()
		assert to == 'to'
		assert eq == '='
		d = int(d)
		distances[(a, b)] = d
		distances[(b, a)] = d
		cities.add(a)
		cities.add(b)

	print(shortest(list(cities), distances))

if __name__ == '__main__':
	main(sys.stdin)
