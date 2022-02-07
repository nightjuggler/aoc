import re
import sys

# https://www.quora.com/What-is-coordinate-compression-and-what-is-it-used-for
# https://www.youtube.com/watch?v=YKpViLcTp64&t=1060s

def read_input():
	n = '(0|-?[1-9][0-9]*)'
	r = f'{n}\\.\\.{n}'
	line_pattern = re.compile(f'^(on|off) x={r},y={r},z={r}$')

	cuboids = []
	for line_num, line in enumerate(sys.stdin, start=1):
		m = line_pattern.match(line)
		if not m:
			sys.exit(f'Input line {line_num} doesn\'t match pattern!')
		c = [m.group(1) == 'on']
		c.extend(map(int, m.group(2,3,4,5,6,7)))
		assert c[1] <= c[2]
		assert c[3] <= c[4]
		assert c[5] <= c[6]
		cuboids.append(c)
	return cuboids

def solve(cuboids):
	xs = []
	ys = []
	zs = []
	for on, x1, x2, y1, y2, z1, z2 in cuboids:
		xs.append(x1)
		xs.append(x2 + 1)
		ys.append(y1)
		ys.append(y2 + 1)
		zs.append(z1)
		zs.append(z2 + 1)
	xs = sorted(set(xs))
	ys = sorted(set(ys))
	zs = sorted(set(zs))

	xn = len(xs)
	yn = len(ys)
	zn = len(zs)
	grid = [[[False] * xn for y in range(yn)] for z in range(zn)]

	for on, x1, x2, y1, y2, z1, z2 in cuboids:
		x1 = xs.index(x1)
		x2 = xs.index(x2 + 1)
		y1 = ys.index(y1)
		y2 = ys.index(y2 + 1)
		z1 = zs.index(z1)
		z2 = zs.index(z2 + 1)
		for z in range(z1, z2):
			for y in range(y1, y2):
				grid[z][y][x1:x2] = [on] * (x2 - x1)

	xs = [xs[x+1] - xs[x] for x in range(xn - 1)]
	ys = [ys[y+1] - ys[y] for y in range(yn - 1)]
	zs = [zs[z+1] - zs[z] for z in range(zn - 1)]

	return sum(x * y * z
		for z, zg in zip(zs, grid)
		for y, yg in zip(ys, zg)
		for x, on in zip(xs, yg) if on)

def main():
	cuboids = read_input()

	init_cuboids = [c for c in cuboids
		if  c[1] >= -50 and c[2] <= 50
		and c[3] >= -50 and c[4] <= 50
		and c[5] >= -50 and c[6] <= 50]

	print('Part 1:', solve(init_cuboids))
	print('Part 2:', solve(cuboids))

if __name__ == '__main__':
	main()
