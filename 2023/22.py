import sys

def read_input():
	bricks = []
	for line in sys.stdin:
		a, b = line.split('~')
		x1, y1, z1 = map(int, a.split(','))
		x2, y2, z2 = map(int, b.split(','))
		assert x1 <= x2
		assert y1 <= y2
		assert z1 <= z2
		assert (x1 == x2) + (y1 == y2) + (z1 == z2) >= 2
		bricks.append((z1, z2-z1, y1, y2, x1, x2))
	bricks.sort()
	return bricks

def part1(above, below):
	return sum(1 for bricks in above
		if not bricks or all(len(below[brick]) > 1 for brick in bricks))

def part2(above, below):
	def recurse(i, fallen):
		new_fallen = [j for j in above[i] if not below[j] - fallen]
		fallen.update(new_fallen)
		for j in new_fallen:
			recurse(j, fallen)
		return len(fallen)

	return sum(recurse(i, {i}) - 1 for i in range(len(above)))

def settle(bricks):
	above = []
	below = []
	cubes = {}
	next_z = 1
	for i, (z, dz, y1, y2, x1, x2) in enumerate(bricks):
		yrange = range(y1, y2+1)
		xrange = range(x1, x2+1)
		if z > next_z:
			z = next_z
		for z in range(z-1, 0, -1):
			hits = set(brick
				for y in yrange
				for x in xrange
				if (brick := cubes.get((z, y, x))) is not None)
			if hits:
				for brick in hits:
					above[brick].append(i)
				below.append(hits)
				z += 1
				break
		else:
			below.append(set())
			z = 1
		zrange = range(z, z + dz + 1)
		next_z = max(next_z, zrange.stop)
		above.append([])
		cubes.update(((z, y, x), i)
			for z in zrange
			for y in yrange
			for x in xrange)
	return above, below

def main():
	above, below = settle(read_input())
	print('Part 1:', part1(above, below))
	print('Part 2:', part2(above, below))
main()
