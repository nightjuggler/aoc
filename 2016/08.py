import re
import sys

def read_input():
	c = '(0|[1-9][0-9]*)'
	n = '([1-9][0-9]*)'
	patterns = (
		re.compile(f'^rotate column x={c} by {n}$'),
		re.compile(f'^rotate row y={c} by {n}$'),
		re.compile(f'^rect {n}x{n}$'),
	)
	ops = []
	for line_num, line in enumerate(sys.stdin, start=1):
		for op, pattern in enumerate(patterns):
			if m := pattern.match(line):
				ops.append((op, *map(int, m.groups())))
				break
		else:
			sys.exit(f'Syntax error on input line {line_num}!')
	return ops

def main():
	ops = read_input()

	width = 50
	height = 6
	screen = [[False] * width for i in range(height)]

	for op, a, b in ops:
		if op == 0:
			col = [row[a] for row in screen]
			for i in range(height):
				screen[i][a] = col[(i - b) % height]
		elif op == 1:
			row = screen[a]
			screen[a] = [row[(i - b) % width] for i in range(width)]
		else:
			for i in range(b):
				screen[i][:a] = [True] * a

	print('Part 1:', sum(map(sum, screen)))
	print('Part 2:')
	for row in screen:
		print(''.join([' #'[pixel] for pixel in row]))

main()
