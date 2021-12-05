import re
import sys

def read_input():
	n = '(0|[1-9][0-9]*)'
	line_pattern = re.compile(f'^{n},{n} -> {n},{n}$')
	line_number = 0
	lines = []
	for line in sys.stdin:
		line_number += 1
		m = line_pattern.match(line)
		if not m:
			print('Line', line_number, 'doesn\'t match pattern!')
			return []
		lines.append(tuple(map(int, m.groups())))
	return lines

def count_overlap(lines):
	points = {}

	for x1, y1, x2, y2 in lines:
		x_step = 1 if x1 < x2 else 0 if x1 == x2 else -1
		y_step = 1 if y1 < y2 else 0 if y1 == y2 else -1
		x, y = x1, y1
		last_xy = (x2, y2)

		while True:
			xy = (x, y)
			points[xy] = points.get(xy, 0) + 1
			if xy == last_xy:
				break
			x += x_step
			y += y_step

	overlap = 0
	for n in points.values():
		if n > 1:
			overlap += 1
	print(overlap)

def part1():
	count_overlap([line for line in read_input() if line[0] == line[2] or line[1] == line[3]])

def part2():
	count_overlap(read_input())

if __name__ == '__main__':
	if len(sys.argv) == 1:
		part1()
	elif len(sys.argv) != 2 or sys.argv[1] != '2':
		print('usage: wtf?')
	else:
		part2()
