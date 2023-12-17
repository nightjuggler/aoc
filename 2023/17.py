from heapq import heappop, heappush
import sys

def solve(loss_map, min_moves, max_moves):
	dxdy = (
		( 1,  0), # 0 => east
		( 0,  1), # 1 => south
		(-1,  0), # 2 => west
		( 0, -1), # 3 => north
	)
	ymax = len(loss_map) - 1
	xmax = len(loss_map[0]) - 1
	end = xmax, ymax
	moves = range(1, max_moves + 1)
	q = []
	best = None
	seen = set()

	def push(loss, x, y, d):
		dx, dy = dxdy[d]
		for move in moves:
			x += dx
			y += dy
			if x < 0 or x > xmax: break
			if y < 0 or y > ymax: break
			loss += loss_map[y][x]
			if move >= min_moves:
				if best and loss >= best: break
				heappush(q, (loss, x, y, d))
	push(0, 0, 0, 0)
	push(0, 0, 0, 1)
	while q:
		loss, x, y, d = heappop(q)
		state = x, y, d
		if state in seen: continue
		seen.add(state)
		if (x, y) == end:
			if best is None or loss < best: best = loss
			continue
		push(loss, x, y, (d-1) % 4)
		push(loss, x, y, (d+1) % 4)
	return best

def main(f, err):
	loss_map = [row.rstrip() for row in f]
	num_rows = len(loss_map)
	if num_rows < 5:
		err('The input must have at least 5 rows!')
	num_cols = len(loss_map[0])
	if num_cols < 5:
		err('The input must have at least 5 columns!')

	if any(len(row) != num_cols for row in loss_map):
		err('The input rows must all have the same length!')

	if any(row.strip('123456789') for row in loss_map):
		err('The input must have only the digits 1 through 9!')

	loss_map = [list(map(int, row)) for row in loss_map]

	print('Part 1:', solve(loss_map, 1, 3))
	print('Part 2:', solve(loss_map, 4, 10))

main(sys.stdin, sys.exit)
