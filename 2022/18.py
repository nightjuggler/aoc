import sys

def neighbors(x, y, z):
	return (x+1,y,z), (x-1,y,z), (x,y+1,z), (x,y-1,z), (x,y,z+1), (x,y,z-1)

def part1(cubes):
	return sum(neighbor not in cubes for xyz in cubes for neighbor in neighbors(*xyz))

def part2(cubes):
	xs = sorted(x for x, y, z in cubes)
	ys = sorted(y for x, y, z in cubes)
	zs = sorted(z for x, y, z in cubes)
	min_x, max_x = xs[0], xs[-1]
	min_y, max_y = ys[0], ys[-1]
	min_z, max_z = zs[0], zs[-1]
	closed = set()

	def is_open(xyz, visited=None):
		if xyz in cubes: return False
		if xyz in closed: return False
		x, y, z = xyz
		if x < min_x or x > max_x: return True
		if y < min_y or y > max_y: return True
		if z < min_z or z > max_z: return True
		if (root := not visited):
			visited = {xyz}
		else:
			if xyz in visited: return False
			visited.add(xyz)
		for xyz in neighbors(x, y, z):
			if is_open(xyz, visited): return True
		if root:
			closed.update(visited)
		return False

	return sum(is_open(neighbor) for xyz in cubes for neighbor in neighbors(*xyz))

def main():
	cubes = set(tuple(map(int, line.split(','))) for line in sys.stdin)
	print('Part 1:', part1(cubes))
	print('Part 2:', part2(cubes))
main()
