import sys

def main(lines):
	ranges = []
	for line in lines:
		line = line.strip()
		if not line: break
		a, b = line.split('-')
		ranges.append((int(a), int(b) + 1))

	print('Part 1:', sum(any(a <= n < b for a, b in ranges) for n in map(int, lines)))

	ids = sorted(set().union(*ranges))
	fresh = [False] * (len(ids) - 1)
	for a, b in ranges:
		a = ids.index(a)
		b = ids.index(b)
		fresh[a:b] = [True] * (b - a)

	print('Part 2:', sum(ids[i+1] - ids[i] for i, good in enumerate(fresh) if good))

if __name__ == '__main__':
	main(sys.stdin)
