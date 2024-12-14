import argparse
import re
import sys

def read_input(example):
	n = '(-?[1-9][0-9]*|0)'
	pattern = re.compile(f'^p={n},{n} v={n},{n}$')
	filename = 'data/14.' + ('example' if example else 'input')

	robots = []
	with open(filename) as f:
		for line_num, line in enumerate(f, start=1):
			m = pattern.match(line)
			if not m:
				sys.exit(f'Line {line_num} doesn\'t match pattern!')
			robots.append(list(map(int, m.groups())))
	return robots

def part1(robots, width, height):
	secs = 100
	quads = [0]*4
	mid_x = width // 2
	mid_y = height // 2
	for x, y, vx, vy in robots:
		x = (x + vx*secs) % width
		y = (y + vy*secs) % height
		if x != mid_x and y != mid_y:
			quads[2 * (y > mid_y) + (x > mid_x)] += 1
	result = 1
	for q in quads: result *= q
	return result

def part2(robots, width, height, threshold):
	grid = [[False]*width for y in range(height)]
	for x, y, vx, vy in robots:
		grid[y][x] = True
	secs = 0
	while True:
		n = 0
		for x, y, vx, vy in robots:
			for ny, nx in (
				(y-1,x-1), (y-1,x), (y-1,x+1),
				(y  ,x-1),          (y  ,x+1),
				(y+1,x-1), (y+1,x), (y+1,x+1),
			):
				if not 0 <= nx < width: continue
				if not 0 <= ny < height: continue
				if grid[ny][nx]: n += 1
		if n > threshold: break
		secs += 1
		for bot in robots:
			x, y, vx, vy = bot
			grid[y][x] = False
			bot[0] = x = (x + vx) % width
			bot[1] = y = (y + vy) % height
			grid[y][x] = True
	while True:
		for row in grid:
			print(''.join('.#'[bot] for bot in row))
		print(secs, 'seconds')
		print('q = quit')
		print('f = step forward')
		print('b = step backward')
		while True:
			command = input('Command? ')
			if command in ('q', 'f', 'b'): break
		if command == 'q': break
		step_back = command == 'b'
		for bot in robots:
			x, y, vx, vy = bot
			if step_back:
				vx = -vx
				vy = -vy
			grid[y][x] = False
			bot[0] = x = (x + vx) % width
			bot[1] = y = (y + vy) % height
			grid[y][x] = True
		if step_back:
			secs -= 1
		else:
			secs += 1

def read_args():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('-x', '--example', action='store_true')
	parser.add_argument('-n', '--threshold', type=int, default=500)
	args = parser.parse_args()
	return args.example, args.threshold

def main():
	example, threshold = read_args()
	width, height = (11, 7) if example else (101, 103)
	robots = read_input(example)

	print('Part 1:', part1(robots, width, height))
	if not example:
		part2(robots, width, height, threshold)
main()
