import re
import sys

def parse_wire(line):
	horz = []
	vert = []
	x, y, steps = 0, 0, 0
	for section in line.split(','):
		direction = section[0]
		distance = int(section[1:])
		if direction == 'U':
			vert.append((x, y, y + distance, steps, 1))
			y += distance
		elif direction == 'D':
			vert.append((x, y - distance, y, steps + distance, -1))
			y -= distance
		elif direction == 'L':
			horz.append((y, x - distance, x, steps + distance, -1))
			x -= distance
		else:
			horz.append((y, x, x + distance, steps, 1))
			x += distance
		steps += distance
	return horz, vert

def read_input():
	segment = '[DLRU][1-9][0-9]*'
	line_pattern = re.compile(f'^{segment}(?:,{segment})*$')
	wires = []
	for line_num, line in enumerate(sys.stdin, start=1):
		m = line_pattern.match(line)
		if not m:
			raise ValueError(f"Input line {line_num} doesn't match pattern!")
		wires.append(parse_wire(line))
	if len(wires) != 2:
		raise ValueError('Expected two lines of input!')
	return wires

def get_overlap(h1, h2):
	return [(y1, max(x1, x3), min(x2, x4))
		for y1, x1, x2, s1, s2 in h1
		for y2, x3, x4, s3, s4 in h2
			if y1 == y2 and x1 <= x4 and x2 >= x3]

def check_overlap(h1, h2):
	overlap = [x for x in get_overlap(h1, h2) if x != (0, 0, 0)]
	if overlap:
		print(overlap)

def get_crossings(horz, vert):
	return [(abs(x) + abs(y), s1+(x-x1)*s2 + s3+(y-y1)*s4)
		for y, x1, x2, s1, s2 in horz
		for x, y1, y2, s3, s4 in vert
			if x1 <= x <= x2 and y1 <= y <= y2 and not (x == 0 == y)]

def main():
	try:
		(h1, v1), (h2, v2) = read_input()
	except ValueError as e:
		print(e)
		return

	check_overlap(h1, h2)
	check_overlap(v1, v2)

	intersections = get_crossings(h1, v2) + get_crossings(v1, h2)
	print('Part 1:', min([d for d, s in intersections]))
	print('Part 2:', min([s for d, s in intersections]))

if __name__ == '__main__':
	main()
