import sys

def main(f):
	towels = set(towel.strip() for towel in f.readline().split(','))
	maxlen = max(map(len, towels))
	cache = {}

	def count(design):
		if design in cache:
			return cache[design]
		n = design in towels
		for i in range(1, min(len(design), maxlen+1)):
			if design[:i] in towels:
				n += count(design[i:])
		cache[design] = n
		return n

	possible = 0
	sum_ways = 0
	for line in f:
		line = line.strip()
		if not line: continue
		if n := count(line):
			possible += 1
			sum_ways += n
	print('Part 1:', possible)
	print('Part 2:', sum_ways)

main(sys.stdin)
