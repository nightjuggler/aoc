import sys

def read_input():
	elves = set()
	for y, line in enumerate(sys.stdin):
		line = line.strip()
		assert line and not line.strip('#.')
		elves.update((x, y) for x, c in enumerate(line) if c == '#')
	return elves

def play(elves, slices):
	moved = False
	proposals = {}
	for x, y in elves:
		adjacent = [(ax, ay) in elves
			for ay in (y-1, y, y+1)
				for ax in (x-1, x, x+1)]
		if sum(adjacent) == 1: continue
		for s, dx, dy in slices:
			if not sum(adjacent[s]):
				new_xy = x + dx, y + dy
				proposals[new_xy] = None if new_xy in proposals else (x, y)
				break
	for new_xy, old_xy in proposals.items():
		if old_xy:
			elves.remove(old_xy)
			elves.add(new_xy)
			moved = True
	return moved

def part1(elves, slices):
	for step in range(10):
		play(elves, slices)
		slices.append(slices.pop(0))
	xs = sorted(x for x, y in elves)
	ys = sorted(y for x, y in elves)
	xs = range(xs[0], xs[-1]+1)
	ys = range(ys[0], ys[-1]+1)
#	for y in ys: print(''.join(['#' if (x, y) in elves else '.' for x in xs]))
	return sum((x, y) not in elves for y in ys for x in xs)

def part2(elves, slices):
	step = 1
	while play(elves, slices):
		slices.append(slices.pop(0))
		step += 1
	return step

def main():
	elves = read_input()
	slices = [(slice(0,3),0,-1), (slice(6,9),0,1), (slice(0,9,3),-1,0), (slice(2,9,3),1,0)]
	print('Part 1:', part1(elves.copy(), slices.copy()))
	print('Part 2:', part2(elves, slices))
main()
