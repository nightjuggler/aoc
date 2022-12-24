from collections import deque
import re
import sys

def read_input():
	n = '([1-9][0-9]?)'
	pattern = re.compile(f'^Blueprint {n}:'
		f' Each ore robot costs {n} ore.'
		f' Each clay robot costs {n} ore.'
		f' Each obsidian robot costs {n} ore and {n} clay.'
		f' Each geode robot costs {n} ore and {n} obsidian.$')
	blueprints = []
	for line_num, line in enumerate(sys.stdin, start=1):
		if not (m := pattern.match(line)):
			sys.exit(f'Line {line_num} doesn\'t match expected pattern!')
		blueprints.append(list(map(int, m.groups())))
	return blueprints

def play(blueprint, time_left=24, max_geodes=0):
	ore0, ore1, ore2, max_bot1, ore3, max_bot2 = blueprint
	max_bot0 = max(ore0, ore1, ore2, ore3)

	q = deque()
	q.append((time_left, 0,0,0,0, 1,0,0,0))
	seen = set()

	print(blueprint, time_left, max_geodes)
	while q:
		state = q.popleft()
		if state in seen: continue
		seen.add(state)
		time_left, q0,q1,q2,g, bot0,bot1,bot2,bot3 = state
		if g + time_left*bot3 + time_left*(time_left-1)//2 <= max_geodes: continue
		r0,r1,r2,g = q0+bot0,q1+bot1,q2+bot2,g+bot3
		time_left -= 1
		if not time_left:
			if g > max_geodes: max_geodes = g
			continue

		if q2 >= max_bot2 and q0 >= ore3:
			q.append((time_left, r0-ore3,r1,r2-max_bot2,g, bot0,bot1,bot2,bot3+1))
			continue

		if q1 >= max_bot1 and q0 >= ore2 and time_left > 2 and bot2 < max_bot2:
			q.append((time_left, r0-ore2,r1-max_bot1,r2,g, bot0,bot1,bot2+1,bot3))

		if q0 >= ore1 and time_left > 4 and bot1 < max_bot1:
			q.append((time_left, r0-ore1,r1,r2,g, bot0,bot1+1,bot2,bot3))

		if q0 >= ore0 and time_left > 2 and bot0 < max_bot0:
			q.append((time_left, r0-ore0,r1,r2,g, bot0+1,bot1,bot2,bot3))

		q.append((time_left, r0,r1,r2,g, bot0,bot1,bot2,bot3))

	print('max_geodes =', max_geodes)
	return max_geodes

def part1(blueprints):
	return sum(i * play(b) for i, *b in blueprints)

def part2(blueprints):
	geodes = []
	for i, *b in blueprints:
		g = 0
		for t in range(23, 33):
			g = play(b, t, g)
		geodes.append(g)
	product = 1
	for g in geodes: product *= g
	return product

def main():
	blueprints = read_input()
	print('Part 1:', part1(blueprints))
	print('Part 2:', part2(blueprints[:3]))
main()
