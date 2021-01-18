import re
import sys

def main(input_file):
	grid = [[False] * 1000 for i in range(1000)]

	turn_on = lambda row, x1, x2: [True] * (x2 - x1 + 1)
	turn_off = lambda row, x1, x2: [False] * (x2 - x1 + 1)
	toggle = lambda row, x1, x2: [not row[x] for x in range(x1, x2+1)]

	line_number = 0
	line_pattern = re.compile('^((?:turn (?:on|off))|toggle) '
		'(0|[1-9][0-9]*),(0|[1-9][0-9]*) through '
		'(0|[1-9][0-9]*),(0|[1-9][0-9]*)$')

	for line in input_file:
		line_number += 1
		m = line_pattern.match(line)
		if not m:
			sys.exit('Line {} doesn\'t match pattern!'.format(line_number))
		w, y1, x1, y2, x2 = m.groups()
		w = turn_on if w == 'turn on' else turn_off if w == 'turn off' else toggle
		y1, x1, y2, x2 = int(y1), int(x1), int(y2), int(x2)
		assert y1 <= y2 < 1000
		assert x1 <= x2 < 1000
		for y in range(y1, y2+1):
			row = grid[y]
			row[x1:x2+1] = w(row, x1, x2)

	print(sum([c for line in grid for c in line]))

if __name__ == '__main__':
	main(sys.stdin)
