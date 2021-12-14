from collections import deque

def part1(depth, target_x, target_y, draw_map=0):
	terrain = ('.', '=', '|') # rocky, wet, narrow
	y_range = target_y + 1 + draw_map
	x_range = target_x + 1 + draw_map

	risk_level = 0
	prev_row = None

	for y in range(y_range):
		row = []
		for x in range(x_range):
			geologic_index = (0 if y == target_y and x == target_x
				else x * 16807 if y == 0
				else y * 48271 if x == 0
				else row[x-1] * prev_row[x])
			erosion_level = (geologic_index + depth) % 20183
			row.append(erosion_level)
			if y <= target_y and x <= target_x:
				risk_level += erosion_level % 3
		if draw_map:
			print(''.join(['M' if y == x == 0
				else 'T' if y == target_y and x == target_x
				else terrain[level % 3] for x, level in enumerate(row)]))
		prev_row = row

	print(risk_level)

def make_terrain_map(depth, target_x, target_y, xmax, ymax):
	levels = []
	prev_row = None
	for y in range(ymax + 1):
		levels.append(row := [])
		for x in range(xmax + 1):
			row.append(((0 if y == target_y and x == target_x
				else x * 16807 if y == 0
				else y * 48271 if x == 0
				else row[x-1] * prev_row[x]) + depth) % 20183)
		prev_row = row
	return [[e % 3 for e in row] for row in levels]

def make_minutes_map(xmax, ymax):
	minutes_map = []
	for y in range(ymax + 1):
		minutes_map.append(row := [])
		for x in range(xmax + 1):
			row.append([0, 0, 0])
	return minutes_map

def extend_minutes_map(minutes_map, xmax, ymax):
	ry = range(ymax + 1 - len(minutes_map))
	rx = range(xmax + 1 - len(minutes_map[0]))
	for row in minutes_map:
		for x in rx:
			row.append([0, 0, 0])
	rx = range(xmax + 1)
	for y in ry:
		minutes_map.append(row := [])
		for x in rx:
			row.append([0, 0, 0])

def part2(depth, target_x, target_y):
	# Tools: 0 = neither, 1 = torch, 2 = climbing gear
	allowed = (
		(False, True, True), # rocky: torch, climbing gear
		(True, False, True), # wet: neither, climbing gear
		(True, True, False), # narrow: neither, torch
	)
	switch = (
		(None, 2, 1),
		(2, None, 0),
		(1, 0, None),
	)
	ymax = target_y
	xmax = target_x
	minutes_map = make_minutes_map(xmax, ymax)
	terrain_map = make_terrain_map(depth, target_x, target_y, xmax, ymax)
	print(sum([sum(row) for row in terrain_map]))

	def process_queue(q, best):
		while q:
			minutes, y, x, tool = q.popleft()

			if best and minutes + abs(target_y - y) + abs(target_x - x) >= best:
				continue
			if y == target_y and x == target_x and tool != 1:
				tool = 1
				minutes += 7

			mm = minutes_map[y][x]
			if 0 < mm[tool] <= minutes:
				continue
			mm[tool] = minutes
			if y == target_y and x == target_x:
				best = minutes
				continue

			terrain = terrain_map[y][x]
			for ay, ax in ((y, x+1), (y+1, x), (y, x-1), (y-1, x)):
				if ay < 0 or ay > ymax: continue
				if ax < 0 or ax > xmax: continue

				adjacent_terrain = terrain_map[ay][ax]
				if allowed[adjacent_terrain][tool]:
					q.append((minutes + 1, ay, ax, tool))
				else:
					q.append((minutes + 8, ay, ax, switch[terrain][adjacent_terrain]))
		return best

	q = deque()
	q.append((0, 0, 0, 1)) # Start at 0, 0 with torch equipped
	best = process_queue(q, 0)

	print('At most', best, 'minutes')
	ymax = (best - target_x + target_y) // 2
	xmax = (best - target_y + target_x) // 2
	print(f'Extending to {xmax} x {ymax}')

	extend_minutes_map(minutes_map, xmax, ymax)
	terrain_map = make_terrain_map(depth, target_x, target_y, xmax, ymax)

	def queue_adjacent(q, y, x, ay, ax):
		terrain = terrain_map[y][x]
		adjacent_terrain = terrain_map[ay][ax]
		for tool, minutes in enumerate(minutes_map[y][x]):
			if minutes:
				if allowed[adjacent_terrain][tool]:
					q.append((minutes + 1, ay, ax, tool))
				else:
					q.append((minutes + 8, ay, ax, switch[terrain][adjacent_terrain]))
	if xmax > target_x:
		x = target_x + 1
		for y in range(target_y):
			queue_adjacent(q, y, target_x, y, x)
	if ymax > target_y:
		y = target_y + 1
		for x in range(target_x):
			queue_adjacent(q, target_y, x, y, x)

	best = process_queue(q, best)
	print(best, 'minutes')

def main():
	print('----- Part 1 Example -----')
	part1(510, 10, 10, 5)
	print('----- Part 1 -----')
	part1(11817, 9, 751)

	print('----- Part 2 Example -----')
	part2(510, 10, 10)
	print('----- Part 2 -----')
	part2(11817, 9, 751)

if __name__ == '__main__':
	main()
