import argparse
import re
import sys

def read_input():
	n = '(-?[1-9][0-9]*|0)'
	pattern = re.compile(f'^Sensor at x={n}, y={n}: closest beacon is at x={n}, y={n}$')
	sensors = []
	for line_num, line in enumerate(sys.stdin, start=1):
		if not (m := pattern.match(line)):
			sys.exit(f'Line {line_num} doesn\'t match expected pattern!')
		sensors.append(list(map(int, m.groups())))
	return sensors

def part1(sensors, y):
	n = 0
	for x1, x2 in sorted((sx - d, sx + d)
		for sx, sy, sd in sensors
			if (d := sd - abs(y - sy)) >= 0):
		if not n:
			n = x2 - x1 + 1
			last_x = x2
		elif x2 > last_x:
			n += x2 - x1 + 1 if x1 > last_x else x2 - last_x
			last_x = x2
	return n

def part2(sensors, max_coord):
	for y in range(max_coord + 1):
		x = 0
		for x1, x2 in sorted((sx - d, sx + d)
			for sx, sy, sd in sensors
				if (d := sd - abs(y - sy)) >= 0):
			if x1 > x: break
			if x2 >= x: x = x2 + 1
		if x <= max_coord:
			return f'{x*4000000 + y} {x, y}'
	return None

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('y', nargs='?', type=int, default=2_000_000)
	args = parser.parse_args()
	row_y = args.y

	sensors = read_input()
	beacons = set(bx for sx, sy, bx, by in sensors if by == row_y)
	sensors = [(sx, sy, abs(bx - sx) + abs(by - sy)) for sx, sy, bx, by in sensors]

	print('Part 1:', part1(sensors, row_y) - len(beacons))
	print('Part 2:', part2(sensors, row_y * 2))
main()
