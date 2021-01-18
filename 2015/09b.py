import sys

def longest(cities, distances):
	max_d = 0
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
		nonlocal max_d
		if i == max_i:
			d = add_distances()
			if d > max_d:
				max_d = d
			return
		recurse(i + 1)
		for j in range(i + 1, max_i + 1):
			cities[i], cities[j] = cities[j], cities[i]
			recurse(i + 1)
			cities[i], cities[j] = cities[j], cities[i]

#	print(cities)
	recurse(0)
	return max_d

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

	print(longest(list(cities), distances))

if __name__ == '__main__':
	main(sys.stdin)
