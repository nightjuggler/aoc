from collections import deque
import sys

def energize(q, tiles, reflect, xmax, ymax):
	energized = set()
	while q:
		x, y, dx, dy = state = q.popleft()
		if x < 0 or x > xmax: continue
		if y < 0 or y > ymax: continue
		if state in energized: continue
		energized.add(state)
		tile = tiles.get((x, y))
		if not tile:
			q.append((x+dx, y+dy, dx, dy))
		elif tile == '|':
			if dy:
				q.append((x, y+dy, 0, dy))
			else:
				q.append((x, y-1, 0, -1))
				q.append((x, y+1, 0,  1))
		elif tile == '-':
			if dx:
				q.append((x+dx, y, dx, 0))
			else:
				q.append((x-1, y, -1, 0))
				q.append((x+1, y,  1, 0))
		else:
			dx, dy = reflect[tile, dx, dy]
			q.append((x+dx, y+dy, dx, dy))

	return len(set((x, y) for x, y, dx, dy in energized))

def main():
	lines = [line.rstrip() for line in sys.stdin]
	if not lines:
		sys.exit('No input!')
	num_rows = len(lines)
	num_cols = len(lines[0])
	if not all(len(line) == num_cols and not line.strip('.|-/\\') for line in lines):
		sys.exit('Input not valid!')

	tiles = {(x, y): tile for y, line in enumerate(lines)
		for x, tile in enumerate(line) if tile != '.'}

	north =  0, -1
	south =  0,  1
	east  =  1,  0
	west  = -1,  0
	reflect = {
		('/', *north): east,
		('/', *south): west,
		('/', *east): north,
		('/', *west): south,
		('\\', *north): west,
		('\\', *south): east,
		('\\', *east): south,
		('\\', *west): north,
	}

	q = deque()
	xmax = num_cols - 1
	ymax = num_rows - 1

	def solve(state):
		q.append(state)
		return energize(q, tiles, reflect, xmax, ymax)

	def start_states():
		for x in range(num_cols):
			yield (x, 0, *south)
			yield (x, ymax, *north)
		for y in range(num_rows):
			yield (0, y, *east)
			yield (xmax, y, *west)

	print('Part 1:', solve((0, 0, *east)))
	print('Part 2:', max(map(solve, start_states())))
main()
