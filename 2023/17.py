from heapq import heappop, heappush
import sys

def part1(loss_map):
	dxdy = (
		( 1,  0), # 0 => east
		( 0,  1), # 1 => south
		(-1,  0), # 2 => west
		( 0, -1), # 3 => north
	)
	ymax = len(loss_map) - 1
	xmax = len(loss_map[0]) - 1
	end = xmax, ymax
	q = []
	best = None
	seen = set()
	heappush(q, (0, 1, 0, 0, 1))
	heappush(q, (0, 0, 1, 1, 1))
	while q:
		loss, x, y, direction, straight = heappop(q)
		if x < 0 or x > xmax: continue
		if y < 0 or y > ymax: continue
		state = x, y, direction, straight
		if state in seen: continue
		seen.add(state)
		loss += loss_map[y][x]
		if best and loss >= best: continue
		if (x, y) == end:
			if best is None or loss < best: best = loss
			continue
		if straight < 3:
			dx, dy = dxdy[direction]
			heappush(q, (loss, x+dx, y+dy, direction, straight+1))
		for d in ((direction-1) % 4, (direction+1) % 4):
			dx, dy = dxdy[d]
			heappush(q, (loss, x+dx, y+dy, d, 1))
	return best

def part2(loss_map):
	dxdy = (
		( 1,  0), # 0 => east
		( 0,  1), # 1 => south
		(-1,  0), # 2 => west
		( 0, -1), # 3 => north
	)
	ymax = len(loss_map) - 1
	xmax = len(loss_map[0]) - 1
	end = xmax, ymax
	q = []
	best = None
	seen = set()
	heappush(q, (sum(loss_map[0][x] for x in range(1, 4)), 4, 0, 0, 4))
	heappush(q, (sum(loss_map[y][0] for y in range(1, 4)), 0, 4, 1, 4))
	while q:
		loss, x, y, direction, straight = heappop(q)
		if x < 0 or x > xmax: continue
		if y < 0 or y > ymax: continue
		state = x, y, direction, straight
		if state in seen: continue
		seen.add(state)
		loss += loss_map[y][x]
		if best and loss >= best: continue
		if (x, y) == end:
			if best is None or loss < best: best = loss
			continue
		if straight < 10:
			dx, dy = dxdy[direction]
			heappush(q, (loss, x+dx, y+dy, direction, straight+1))
		for d in ((direction-1) % 4, (direction+1) % 4):
			dx, dy = dxdy[d]
			nx, ny, nloss = x, y, loss
			for i in range(3):
				nx += dx
				ny += dy
				if nx < 0 or nx > xmax: break
				if ny < 0 or ny > ymax: break
				nloss += loss_map[ny][nx]
			else:
				heappush(q, (nloss, nx+dx, ny+dy, d, 4))
	return best

def main(f, err):
	loss_map = [row.rstrip() for row in f]

	num_rows = len(loss_map)
	if num_rows < 5:
		err('The input must have at least 5 rows!')
	num_cols = len(loss_map[0])
	if num_cols < 5:
		err('The input must have at least 5 columns!')

	if not all(len(row) == num_cols for row in loss_map):
		err('The input rows must all have the same length!')

	if any(row.strip('123456789') for row in loss_map):
		err('The input must have only the digits 1 through 9!')

	loss_map = [list(map(int, row)) for row in loss_map]

	print('Part 1:', part1(loss_map))
	print('Part 2:', part2(loss_map))

main(sys.stdin, sys.exit)
