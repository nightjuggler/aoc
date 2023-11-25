from collections import deque
from heapq import heappop, heappush
import sys

err = sys.exit

def scan(portals, rows, y1, y2, x1, x2, rows_are_cols=False):
	s1 = slice(x1, x1+3)
	s2 = slice(x2-3, x2)
	m = 'cols' if rows_are_cols else 'rows'
	is_outer = x1 == 0

	def is_upper(a): return 65 <= ord(a) <= 90
	def is_valid(a): return a == ' ' or is_upper(a) and not is_outer

	def add(a,b,c, x,y):
		if c == '#':
			return is_valid(a) and is_valid(b)
		if not (c == '.' and is_upper(a) and is_upper(b)):
			return False

		p = portals.get(ab := a+b)
		if is_outer:
			if p: err(f'More than one outer portal {ab}!')
			portals[ab] = p = []
		elif not p:
			err(f'No outer portal {ab}!')
		elif len(p) != 1:
			err(f'More than one inner portal {ab}!')

		p.append((y,x) if rows_are_cols else (x,y))
		return True

	for y in range(y1, y2):
		row = rows[y]
		a,b,c = row[s1]
		if not add(a,b,c, x1+2,y):
			err(f'{m}[{y}][{x1}:{x1+3}] must be "  #" or "XX."!')
		c,a,b = row[s2]
		if not add(a,b,c, x2-3,y):
			err(f'{m}[{y}][{x2-3}:{x2}] must be "#  " or ".XX"!')

def read_input():
	rows = [row.rstrip('\n') for row in sys.stdin]

	ysize = len(rows)
	if ysize < 15:
		err('Expected at least 15 lines of input!')
	xsize = len(rows[0])
	if xsize < 15 or any(len(row) != xsize for row in rows):
		err('All input lines must have the same length (>= 15)!')

	portals = {}
	cols = [''.join(col) for col in zip(*rows)]

	scan(portals, rows, 2, ysize-2, 0, xsize)
	scan(portals, cols, 2, xsize-2, 0, ysize, True)

	row = rows[ysize//2]
	for w in range(2, xsize-2):
		c = row[w]
		if c != '#' and c != '.': break
	else:
		err(f'rows[{ysize//2}] is not empty in the middle!')

	scan(portals, rows, w, ysize-w, xsize-w-2, w+2)
	scan(portals, cols, w, xsize-w, ysize-w-2, w+2, True)

	nodes = {(x,y): []
		for y in range(2, ysize-2)
		for x in range(2, xsize-2)
		if rows[y][x] == '.'}

	def pop_end(ab):
		xy, = portals.pop(ab)
		return nodes[xy]

	aa = pop_end('AA')
	zz = pop_end('ZZ')
	portals = [(nodes[xy1], nodes[xy2]) for xy1, xy2 in portals.values()]

	return nodes, aa, zz, portals

def prepare1(nodes, aa, zz, portals):
	for i, ((x,y), node) in enumerate(nodes.items()):
		node[:] = [i]
		for xy in ((x+1,y), (x,y+1), (x-1,y), (x,y-1)):
			neighbor = nodes.get(xy)
			if neighbor is not None:
				node.append(neighbor)

	for node1, node2 in portals:
		node1.append(node2)
		node2.append(node1)

	return aa, zz[0]

def part1(aa, zz):
	seen = set()
	q = deque()
	q.append((0, aa))
	while q:
		step, (node, *neighbors) = q.popleft()
		if node in seen: continue
		seen.add(node)
		if node == zz: return step
		q.extend((step + 1, node) for node in neighbors)
	return None

def connect(node):
	graph = {}
	q = deque()
	pq = deque()
	pq.append(node)
	while pq:
		node = pq.popleft()
		node_id = node[0]
		if node_id in graph: continue
		graph[node_id] = paths = []
		seen = set()
		q.append((0, node))
		while q:
			step, (node_id, portal, *neighbors) = q.popleft()
			if node_id in seen: continue
			seen.add(node_id)
			if portal:
				dy, node = portal
				if dy:
					paths.append((dy, step + 1, node[0]))
					pq.append(node)
				else: # ZZ
					paths.append((0, step, None))
			q.extend((step + 1, node) for node in neighbors)
	return graph

def prepare2(nodes, aa, zz, portals):
	for i, ((x,y), node) in enumerate(nodes.items()):
		node[:] = [i, None]
		for xy in ((x+1,y), (x,y+1), (x-1,y), (x,y-1)):
			neighbor = nodes.get(xy)
			if neighbor is not None:
				node.append(neighbor)
	zz[1] = 0, zz
	for node1, node2 in portals:
		node1[1] = -1, node2
		node2[1] =  1, node1

	return aa[0], connect(aa), len(portals)

def part2(aa, graph, max_level):
	seen = {}
	best = None
	q = []
	heappush(q, (0, 0, aa))
	while q:
		level, step, node = heappop(q)
		steps = seen.get(node)
		state = level, node
		steps = seen.get(state)
		if steps is not None and steps <= step: continue
		seen[state] = step
		if best is not None and best <= step: continue
		if level == max_level: continue
		for dy, steps, next_node in graph[node]:
			if not dy: # ZZ
				if not level and (best is None or step + steps < best):
					best = step + steps
			elif level or dy > 0:
				heappush(q, (level + dy, step + steps, next_node))
	return best

def main():
	data = read_input()
	print('Part 1:', part1(*prepare1(*data)))
	print('Part 2:', part2(*prepare2(*data)))
main()
