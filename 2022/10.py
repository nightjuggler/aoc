import sys

def main():
	x = 1
	xs = [x]
	for line in sys.stdin:
		xs.append(x)
		if line[:5] == 'addx ':
			x += int(line[5:])
			xs.append(x)
		else:
			assert line == 'noop\n'

	print('Part 1:', sum((i+1)*xs[i] for i in range(19, len(xs), 40)))
	print('Part 2:')
	for y in range(0, 240, 40):
		print(''.join(['.#'[abs(xs[y+x]-x) <= 1] for x in range(40)]))
main()
