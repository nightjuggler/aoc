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

def prune(graph):
	for node1, next_nodes in enumerate(graph):
		remove = 0
		for node2, steps in next_nodes:
			seen = 1<<node1
			q = deque()
			q.append(node2)
			while q:
				node = q.popleft()
				if node == 1: break
				seen |= 1<<node
				for node, steps in graph[node]:
					if not (seen & (1<<node)): q.append(node)
			else:
				# Cannot reach the end node by going from node1 to node2
				remove |= 1<<node2
		if remove:
			next_nodes[:] = [move for move in next_nodes if not (remove & (1<<move[0]))]
	return graph

def connect(lines, next_xy):
	rows = [[None if c == '#' else [0] for c in line] for line in lines]
	rows[0][1], rows[-1][-2] = graph = [[0, [rows[1][1]]], [1, []]]

	for y, row in enumerate(rows[1:-1], start=1):
		for x, trail in enumerate(row[1:-1], start=1):
			if trail:
				moves = [rows[ny][nx] for nx, ny in next_xy(x, y) if rows[ny][nx]]
				trail.append(moves)
				if len(moves) > 2:
					trail[0] = len(graph)
					graph.append(trail)
	for trail in graph:
		node, moves = trail
		graph[node] = nodes = []
		for trail2 in moves:
			prev = trail
			steps = 1
			while True:
				node, moves = trail2
				if node:
					nodes.append((node, steps))
					break
				if len(moves) == 1:
					move1, = moves
					if prev is move1: break
					prev, trail2 = trail2, move1
				else:
					move1, move2 = moves
					prev, trail2 = trail2, (move2 if prev is move1 else move1)
				steps += 1
	return prune(graph)

def solve(graph):
	best = 0
	q = deque()
	q.append((0, 0, 0))
	while q:
		steps, node, seen = q.popleft()
		if node == 1:
			if steps > best: best = steps
			continue
		seen |= 1<<node
		for next_node, next_steps in graph[node]:
			if not (seen & (1<<next_node)):
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

	print('Part 1:', solve(connect(lines, part1)))
	print('Part 2:', solve(connect(lines, part2)))
main()
