from collections import deque
from itertools import combinations
import re
import sys

def read_input():
	x = 'an? [a-z]+(?:(?:-compatible microchip)|(?: generator))'
	pattern = re.compile('^The ([a-z]+) floor contains ((?:nothing relevant)|'
		f'(?:{x}(?:(?:(?:, {x})+,)? and {x})?))\\.$')
	ordinals = ('first', 'second', 'third', 'fourth')
	max_floor = len(ordinals) - 1

	all_microchips = set()
	all_generators = set()
	floors = []

	floor = None
	for floor, line in enumerate(sys.stdin):
		if floor > max_floor:
			break
		m = pattern.match(line)
		if not m or m.group(1) != ordinals[floor]:
			raise SystemExit(f'Syntax error on input line {floor+1}!')
		contains = m.group(2)
		if contains == 'nothing relevant':
			assert floor > 0
			floors.append((frozenset(), frozenset()))
			continue
		contains = contains.split(', ')
		if len(contains) == 1:
			i = contains[0].find(' and a')
			if i > 0:
				contains = contains[0]
				contains = [contains[:i], contains[i+5:]]
		else:
			assert len(contains) > 2
			assert contains[-1].startswith('and a')
			contains[-1] = contains[-1][4:]
		microchips = set()
		generators = set()
		for item in contains:
			a, b, c = item.split(' ')
			if c == 'microchip':
				b = b.removesuffix('-compatible')
				assert b not in all_microchips
				all_microchips.add(b)
				microchips.add(b)
			else:
				assert b not in all_generators
				all_generators.add(b)
				generators.add(b)
		if microchips and generators:
			assert microchips <= generators
		floors.append((frozenset(microchips), frozenset(generators)))

	if floor != max_floor:
		raise SystemExit(f'Expected exactly {max_floor+1} input lines!')

	assert all_microchips == all_generators
	assert len(floors) == max_floor + 1
	return floors

def valid(items):
	m1, g1, m2, g2 = items
	return (not (m1 and g1) or m1 <= g1) and (not (m2 and g2) or m2 <= g2)

def two_combos(items, next_items):
	m1, g1 = items
	m2, g2 = next_items

	for x in m1 & g1:
		x = (x,)
		yield (m1.difference(x), g1.difference(x), m2.union(x), g2.union(x))
		break
	for x in combinations(m1, 2):
		yield (m1.difference(x), g1, m2.union(x), g2)
	for x in combinations(g1, 2):
		yield (m1, g1.difference(x), m2, g2.union(x))

def one_combos(items, next_items):
	m1, g1 = items
	m2, g2 = next_items

	for x in m1:
		x = (x,)
		yield (m1.difference(x), g1, m2.union(x), g2)
	for x in g1:
		x = (x,)
		yield (m1, g1.difference(x), m2, g2.union(x))

def solve(floors):
	q = deque()
	q.append((0, 0, floors.copy()))
	seen = set()

	while q:
		steps, floor, floors = q.popleft()
		state = (floor, *((len(m)<<4) + len(g) for m, g in floors))
		if state in seen:
			continue
		seen.add(state)
		max_floor = len(floors) - 1
		if not max_floor:
			return steps

		items = floors[floor]
		steps += 1

		if floor < max_floor:
			next_floor = floor + 1
			next_items = floors[next_floor]
			combos = list(filter(valid, two_combos(items, next_items)))
			if not combos:
				combos = filter(valid, one_combos(items, next_items))
			for mics, gens, next_mics, next_gens in combos:
				floors[floor] = (mics, gens)
				floors[next_floor] = (next_mics, next_gens)
				if floor or mics or gens:
					q.append((steps, next_floor, floors.copy()))
				else:
					q.append((steps, 0, floors[1:]))
			floors[next_floor] = next_items

		if floor:
			next_floor = floor - 1
			next_items = floors[next_floor]
			combos = list(filter(valid, one_combos(items, next_items)))
			if not combos:
				combos = filter(valid, two_combos(items, next_items))
			for mics, gens, next_mics, next_gens in combos:
				floors[floor] = (mics, gens)
				floors[next_floor] = (next_mics, next_gens)
				q.append((steps, next_floor, floors.copy()))
	return None

def main():
	floors = read_input()
	print('Part 1:', solve(floors))

	floors[0] = tuple(items.union(('elerium', 'dilithium')) for items in floors[0])
	print('Part 2:', solve(floors))

# > python3 11.py < data/11.example
# Part 1: 11
# Part 2: None

# > python3 11.py < data/11.input
# Part 1: 47
# Part 2: 71

if __name__ == '__main__':
	main()
