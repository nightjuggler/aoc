import sys

def part1(lines):
	def count(line):
		return line.count('XMAS') + line.count('SAMX')
	n = len(lines)
	m = n - 1
	result = sum(map(count, lines))
	for line in zip(*lines):
		result += count(''.join(line))
	for x in range(n):
		result += count(''.join(lines[i][x+i] for i in range(n-x)))
		result += count(''.join(lines[i][m-(x+i)] for i in range(n-x)))
	for y in range(1, n):
		result += count(''.join(lines[y+i][i] for i in range(n-y)))
		result += count(''.join(lines[y+i][m-i] for i in range(n-y)))
	return result

def part2(lines):
	m = len(lines) - 1
	result = 0
	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			if c == 'A' and 0 < x < m and 0 < y < m:
				d1 = lines[y-1][x-1] + lines[y+1][x+1]
				d2 = lines[y-1][x+1] + lines[y+1][x-1]
				if (d1 == 'MS' or d1 == 'SM') and (d2 == 'MS' or d2 == 'SM'):
					result += 1
	return result

def main():
	lines = [line.strip() for line in sys.stdin]
	line_len = len(lines)
	assert line_len and all(len(line) == line_len for line in lines)

	print('Part 1:', part1(lines))
	print('Part 2:', part2(lines))

if __name__ == '__main__':
	main()
