import argparse
from collections import deque
import sys

def connect(graph, loc, node):
	keys = 0
	q = deque()
	pq = deque()
	pq.append((loc, node))
	while pq:
		loc, node = pq.popleft()
		if loc in graph: continue
		graph[loc] = dest = []
		seen = set()
		q.append((0, node))
		while q:
			step, node = q.popleft()
			node_id, loc, adjacent = node
			if node_id in seen: continue
			seen.add(node_id)
			if loc and step:
				dest.append((loc & 63, step))
				pq.append((loc & 63, node))
				if not loc & 32:
					keys |= 1 << (loc & 31)
			else:
				q.extend((step + 1, node) for node in adjacent)
	return keys

def connect_keys(graph):
	# From every node that's not a door (keys and start nodes), find paths to
	# every other reachable node while keeping track of which keys are required
	# along the way, either for opening doors or because they should be collected
	# first. Discard paths for which the required keys are a superset of the keys
	# required by another path unless the superset path is shorter.
	# Return a mapping that maps every non-door node to a list of 3-tuples. Each
	# 3-tuple represents a path from that node to a key: the number of the key,
	# the number of steps to the key, and the other keys needed along that path.
	q = deque()
	new_graph = {}
	for loc in graph:
		if loc & 32: continue
		paths = {}
		q.extend((dest, steps, 0) for dest, steps in graph[loc])
		while q:
			dest, steps, keys = q.popleft()
			p = paths.get(dest)
			if p is None:
				paths[dest] = p = []
			elif any(steps >= p_steps and keys & p_keys == p_keys
				for p_steps, p_keys in p): continue
			p.append((steps, keys))
			keys |= 1 << (dest & 31)
			q.extend((next_dest, steps + next_steps, keys)
				for next_dest, next_steps in graph[dest])
		new_graph[loc] = [(dest, steps, keys)
			for dest, p in paths.items() if not dest & 32
			for steps, keys in p]
	return new_graph

def process(start):
	locs = 0
	graph = {}
	all_keys = 0
	vault_keys = []
	assert 1 <= len(start) <= 4
	for i, node in enumerate(start):
		loc = 27 + i
		locs |= loc << i*6
		keys = connect(graph, loc, node)
		all_keys |= keys
		vault_keys.append((i*6, keys))
	graph = connect_keys(graph)
	seen = {}
	best = None
	q = deque()
	q.append((0, locs, all_keys))
	while q:
		step, locs, keys = q.popleft()
		state = locs, keys
		steps = seen.get(state)
		if steps is not None and steps <= step: continue
		seen[state] = step
		if best is not None and best <= step: continue
		for i, vkeys in vault_keys:
			if not keys & vkeys: continue
			new_locs = locs & ~(63 << i)
			for dest, steps, keys_needed in graph[(locs >> i) & 63]:
				if keys & keys_needed: continue
				key = 1 << dest
				if not keys & key:
					continue # We already have this key.
				elif keys == key:
					if best is None or step + steps < best: best = step + steps
				else:
					q.append((step + steps, new_locs | (dest << i), keys - key))
	return best

def odd_gt3(n): return n > 3 and n & 1

def change_start(lines):
	assert odd_gt3(len(lines))
	line_len = len(lines[0])
	assert odd_gt3(line_len)
	assert all(len(line) == line_len for line in lines)
	y = len(lines) // 2
	x = line_len // 2
	for y, s_old, s_new in (
		(y-1, '...', '@#@'),
		(y  , '.@.', '###'),
		(y+1, '...', '@#@')
	):
		assert lines[y][x-1:x+2] == s_old
		lines[y] = lines[y][:x-1] + s_new + lines[y][x+2:]

def set_keys_and_doors(special):
	a_lower = ord('a')
	a_upper = ord('A')
	for i in range(26):
		key = chr(a_lower + i)
		door = chr(a_upper + i)
		key_node = special.pop(key, None)
		door_node = special.pop(door, None)
		if key_node:
			key_node[1] = 64 + i
			if not door_node:
				print(f"Key '{key}' has no door")
		if door_node:
			door_node[1] = 64 + 32 + i
			if not key_node:
				print(f"Door '{door}' has no key")
	assert not special

def parse_lines(lines):
	start = []
	node_id = 0
	special = {}
	curr_row = {}

	for line in lines:
		prev_row = curr_row
		curr_row = {}
		for x, c in enumerate(line):
			if c == '#': continue
			node_id += 1
			adjacent = []
			node = [node_id, 0, adjacent]
			if c != '.':
				if c == '@':
					start.append(node)
				else:
					assert c not in special
					special[c] = node
			if prev := prev_row.get(x):
				adjacent.append(prev)
				prev[2].append(node)
			if prev := curr_row.get(x-1):
				adjacent.append(prev)
				prev[2].append(node)
			curr_row[x] = node

	set_keys_and_doors(special)
	return start

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('part', nargs='?', type=int, choices=(1,2), default=1)
	args = parser.parse_args()

	lines = [line.rstrip() for line in sys.stdin]
	if args.part == 2:
		change_start(lines)

	print(f'Part {args.part}:', process(parse_lines(lines)))

if __name__ == '__main__':
	main()
