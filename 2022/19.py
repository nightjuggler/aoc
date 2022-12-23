from collections import deque
import operator
import re
import sys

def read_input():
	n = '[1-9][0-9]?'
	pattern = re.compile(f'^Blueprint ({n}):'
		f'(?: Each (?:ore|clay|obsidian|geode) robot costs [234] ore'
		f'(?: and {n} (?:clay|obsidian))?\\.){{4}}$')
	order = ((), ('ore',), ('clay',), ('obsidian', 'clay'), ('geode', 'obsidian'))
	blueprints = []
	for line_num, line in enumerate(sys.stdin, start=1):
		if not (m := pattern.match(line)) or int(m.group(1)) != line_num:
			sys.exit(f'Line {line_num} doesn\'t match expected pattern!')
		blueprint = []
		for i, line in enumerate(map(str.strip, line.split(':')[1].split('.')), start=1):
			expect = order[i % 5]
			if not expect:
				assert not line
				continue
			line = line.split()
			if len(expect) == 1:
				assert len(line) == 6
				assert line[1] == expect[0]
				blueprint.append(int(line[4]))
			else:
				assert len(line) == 9
				assert line[1] == expect[0]
				assert line[8] == expect[1]
				blueprint.append((int(line[4]), int(line[7])))
		blueprints.append(blueprint)
	return blueprints

def play(blueprint, time_left=24, max_geodes=0):
	add = operator.add
	sub = operator.sub
	gte = operator.ge
	need_ore0, need_ore1, (need_ore2, max_bot1), (need_ore3, max_bot2) = blueprint
	max_bot0 = max(need_ore0, need_ore1, need_ore2, need_ore3)
	cost3 = (need_ore3, 0, max_bot2)
	cost2 = (need_ore2, max_bot1, 0)
	cost1 = (need_ore1, 0, 0)
	cost0 = (need_ore0, 0, 0)

	q = deque()
	q.append((time_left, (0, 0, 0, 0), (1, 0, 0, 0)))
	seen = set()

	print(blueprint, time_left, max_geodes)
	while q:
		time_left, resources, robots = state = q.popleft()
		if state in seen: continue
		seen.add(state)
		bot0, bot1, bot2, bot3 = robots
		*old3, g = resources
		if g + time_left * bot3 + time_left * (time_left - 1) // 2 <= max_geodes: continue
		*new3, g = resources = tuple(map(add, resources, robots))
		time_left -= 1
		if not time_left:
			if g > max_geodes: max_geodes = g
			continue

		if all(map(gte, old3, cost3)):
			q.append((time_left, (*map(sub, new3, cost3), g), (bot0, bot1, bot2, bot3+1)))
			continue

		if all(map(gte, old3, cost2)) and time_left > 2 and bot2 < max_bot2:
			q.append((time_left, (*map(sub, new3, cost2), g), (bot0, bot1, bot2+1, bot3)))

		if all(map(gte, old3, cost1)) and time_left > 4 and bot1 < max_bot1:
			q.append((time_left, (*map(sub, new3, cost1), g), (bot0, bot1+1, bot2, bot3)))

		if all(map(gte, old3, cost0)) and time_left > 2 and bot0 < max_bot0:
			q.append((time_left, (*map(sub, new3, cost0), g), (bot0+1, bot1, bot2, bot3)))

		q.append((time_left, resources, robots))

	print('max_geodes =', max_geodes)
	return max_geodes

def part1(blueprints):
	return sum(i * play(b) for i, b in enumerate(blueprints, start=1))

def part2(blueprints):
	geodes = []
	for b in blueprints:
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
