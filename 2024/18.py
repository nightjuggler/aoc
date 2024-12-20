import argparse
from heapq import heappop, heappush

def part1(coords, num_bytes, max_xy):
	size = max_xy + 1
	blocked = [[False]*size for y in range(size)]
	for x, y in coords[:num_bytes]:
		blocked[y][x] = True
	q = []
	heappush(q, (0, max_xy, max_xy))
	while q:
		steps, x, y = heappop(q)
		if not (x or y): return steps
		if blocked[y][x]: continue
		blocked[y][x] = True
		steps += 1
		if x: heappush(q, (steps, x-1, y))
		if y: heappush(q, (steps, x, y-1))
		if x < max_xy: heappush(q, (steps, x+1, y))
		if y < max_xy: heappush(q, (steps, x, y+1))
	return None

def part2_v1(coords, num_bytes, max_xy):
	size = max_xy + 1
	blocked = [[False]*size for y in range(size)]
	for x, y in coords[:num_bytes]:
		blocked[y][x] = True
	start = size*size - 1
	for bx, by in coords[num_bytes:]:
		blocked[by][bx] = True
		seen = [False]*(start+1)
		q = []
		heappush(q, start)
		while q:
			xy = heappop(q)
			if not xy: break
			if seen[xy]: continue
			seen[xy] = True
			y, x = divmod(xy, size)
			if x and not blocked[y][x-1]: heappush(q, y*size + x-1)
			if y and not blocked[y-1][x]: heappush(q, (y-1)*size + x)
			if x < max_xy and not blocked[y][x+1]: heappush(q, y*size + x+1)
			if y < max_xy and not blocked[y+1][x]: heappush(q, (y+1)*size + x)
		else:
			return f'{bx},{by}'
	return None

def part2_v2(coords, num_bytes, max_xy):
	size = max_xy + 1
	blocked = [[2]*size]
	for y in range(size):
		blocked.append([0]*size)
	blocked.append([4]*size)
	for row in blocked:
		row.insert(0, 4)
		row.append(2)
	dxdy = [(dx, dy) for dy in range(-1,2) for dx in range(-1,2) if dx or dy]
	for bx, by in coords:
		blocked[by+1][bx+1] = 1
		todo = {(bx+1, by+1)}
		while todo:
			x, y = todo.pop()
			color = 0
			unassigned = []
			for dx, dy in dxdy:
				color2 = blocked[y+dy][x+dx]
				if not color2: continue
				if color2 == 1:
					unassigned.append((x+dx, y+dy))
				elif not color:
					color = color2
				elif color != color2:
					return f'{bx},{by}'
			if color:
				blocked[y][x] = color
				todo.update(unassigned)
	return None

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('-x', '--example', action='store_true')
	parser.add_argument('--old2', action='store_true')
	args = parser.parse_args()

	part2 = part2_v1 if args.old2 else part2_v2
	max_xy, num_bytes, suffix = (6, 12, 'example') if args.example else (70, 1024, 'input')

	with open(f'data/18.{suffix}') as f:
		coords = [tuple(map(int, line.split(','))) for line in f]

	print('Part 1:', part1(coords, num_bytes, max_xy))
	print('Part 2:', part2(coords, num_bytes, max_xy))

main()
