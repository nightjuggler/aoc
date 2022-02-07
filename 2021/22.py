import re
import sys

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

def segment(ax1, ax2, bx1, bx2):
	if ax2 < bx1 or ax1 > bx2:
		return None
	x = []
	if ax1 < bx1:
		x.append((False, ax1, bx1-1))
		ax1 = bx1
	if bx2 < ax2:
		x.append((True, ax1, bx2))
		x.append((False, bx2+1, ax2))
	else:
		x.append((True, ax1, ax2))
	return x

def solve(cuboids):
	regions = []
	for c in cuboids:
		c_on, cx1, cx2, cy1, cy2, cz1, cz2 = c
		new_regions = []
		for a in regions:
			if (a[0] and
				(xs := segment(a[1], a[2], cx1, cx2)) and
				(ys := segment(a[3], a[4], cy1, cy2)) and
				(zs := segment(a[5], a[6], cz1, cz2))
			):
				# A and C intersect: Turn off A, and keep only subregions
				# of A that don't intersect with C (if any).
				a[0] = False
				new_regions.extend([True, x1, x2, y1, y2, z1, z2]
					for overlap_x, x1, x2 in xs
					for overlap_y, y1, y2 in ys
					for overlap_z, z1, z2 in zs
						if not (overlap_x and overlap_y and overlap_z))
		regions.extend(new_regions)
		if c_on:
			regions.append(c.copy())

	return sum((x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
		for on, x1, x2, y1, y2, z1, z2 in regions if on)

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
