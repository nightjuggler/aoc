import sys

def main(lines):
	ranges = []
	for line in lines:
		line = line.strip()
		if not line: break
		a, b = line.split('-')
		ranges.append((int(a), int(b) + 1))

	print('Part 1:', sum(any(a <= n < b for a, b in ranges) for n in map(int, lines)))

	fresh = prev_b = 0
	for a, b in sorted(ranges):
		if b > prev_b:
			fresh += b - (prev_b if prev_b > a else a)
			prev_b = b
	print('Part 2:', fresh)

if __name__ == '__main__':
	main(sys.stdin)
