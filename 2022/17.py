import sys

def draw(stopped, rock, max_y):
	for y in range(max_y, 0, -1):
		print('|', *['@' if (x, y) in rock else '#' if (x, y) in stopped else '.'
			for x in range(1, 8)], '|', sep='')
	print(f'+-------+')
	print()

def draw_state(state):
	for y in range(max(y for x, y in state) + 1):
		print('|', *['.#'[(x, y) in state] for x in range(1, 8)], '|', sep='')
	print()

def play(rocks, jets, drops):
	jet = 0
	num_jets = len(jets)
	seen = {}
	max_y = 0
	max_ys = [0] * 7
	i_to_max_y = []
	stopped = set((x, 0) for x in range(1, 8))

	for i in range(drops):
		state = (jet, frozenset((x, max_y - y)
			for y in range(min(max_ys), max_y + 1)
				for x in range(1, 8)
					if (x, y) in stopped))
		if state in seen:
			prev_i = seen[state]
			prev_max_y = i_to_max_y[prev_i]
			d, m = divmod(drops - i, i - prev_i)
			max_y += d * (max_y - prev_max_y) + i_to_max_y[prev_i + m] - prev_max_y
			break
		seen[state] = i
		i_to_max_y.append(max_y)

		rock = [(3 + x, max_y + 4 + y) for x, y in rocks[i % 5]]
		while True:
			dx = jets[jet]
			jet = (jet + 1) % num_jets
			r = [(x + dx, y) for x, y in rock]
			for x, y in r:
				if x == 0 or x == 8 or (x, y) in stopped: break
			else:
				rock = r
			r = [(x, y - 1) for x, y in rock]
			for xy in r:
				if xy in stopped: break
			else:
				rock = r
				continue
			break
		stopped.update(rock)
		for x, y in rock:
			if y > max_ys[x-1]: max_ys[x-1] = y
		max_y = max(max_ys)

	return max_y

def main():
	jets = [1 if jet == '>' else -1 for jet in sys.stdin.readline().strip()]
	rocks = (
		((0,0),(1,0),(2,0),(3,0)),
		((1,0),(0,1),(1,1),(2,1),(1,2)),
		((0,0),(1,0),(2,0),(2,1),(2,2)),
		((0,0),(0,1),(0,2),(0,3)),
		((0,0),(1,0),(0,1),(1,1)),
	)
	print('Part 1:', play(rocks, jets, 2022))
	print('Part 2:', play(rocks, jets, 1_000_000_000_000))
main()
