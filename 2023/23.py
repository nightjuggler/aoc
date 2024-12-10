from collections import deque
import sys

def read_input():
	lines = [line.rstrip() for line in sys.stdin]
	num_rows = len(lines)
	assert num_rows >= 3
	num_cols = len(lines[0])
	assert num_cols >= 3
	assert all(len(line) == num_cols for line in lines)
	assert all(line[0] == '#' == line[-1] for line in lines)
	assert lines[0][1] == '.' and not lines[0][2:].strip('#')
	assert lines[-1][-2] == '.' and not lines[-1][:-2].strip('#')
	assert lines[1][1] == '.' == lines[-2][-2]
	assert all(not line.strip('#.<>^v') for line in lines)
	return lines

def connect(lines, next_xy):
	ymax = len(lines) - 1
	xmax = len(lines[0]) - 2
	q = deque()
	nq = deque()
	node, x, y = 0, 1, 0
	nq.append((node, x, y))
	xy_to_node = {(x, y): node}
	graph = [None]

	while nq:
		node, x, y = nq.popleft()
		graph[node] = next_nodes = []
		seen = set()
		q.append((0, x, y))
		while q:
			steps, x, y = q.popleft()
			if (x, y) in seen: continue
			seen.add((x, y))
			if y == 0:
				q.append((steps+1, x, 1))
				continue
			if y != ymax:
				nxy = [(nx, ny) for nx, ny in next_xy(x, y) if lines[ny][nx] != '#']
				if not steps or len(nxy) <= 2:
					q.extend((steps+1, nx, ny) for nx, ny in nxy)
					continue
			node = xy_to_node.get((x, y))
			if not node:
				xy_to_node[x, y] = node = len(graph)
				graph.append(None)
				if y != ymax:
					nq.append((node, x, y))
			next_nodes.append((steps, node))

	return graph, xy_to_node[xmax, ymax]

def solve(graph, end):
	best = 0
	q = deque()
	q.append((0, 0, frozenset()))
	while q:
		steps, node, seen = q.popleft()
		if node == end:
			if steps > best: best = steps
			continue
		seen = seen | {node}
		for next_steps, next_node in graph[node]:
			if next_node not in seen:
				q.append((steps + next_steps, next_node, seen))
	return best

def main():
	lines = read_input()
	dxdy = {
		'.': ((1,0), (0,1), (-1,0), (0,-1)),
		'<': ((-1,0),),
		'>': ((1,0),),
		'^': ((0,-1),),
		'v': ((0,1),),
	}
	def part1(x, y):
		return [(x+dx, y+dy) for dx, dy in dxdy[lines[y][x]]]
	def part2(x, y):
		return (x+1,y), (x,y+1), (x-1,y), (x,y-1)

	print('Part 1:', solve(*connect(lines, part1)))
	print('Part 2:', solve(*connect(lines, part2)))
main()
