import re
import sys

def read_input():
	n = '(0|-?[1-9][0-9]*)'
	r = f'{n}\\.\\.{n}'
	line_pattern = re.compile(f'^(on|off) x={r},y={r},z={r}$')

	cuboids = []
	for line_number, line in enumerate(sys.stdin, start=1):
		m = line_pattern.match(line)
		if not m:
			print(f'Input line {line_number} doesn\'t match pattern!')
			return None
		c = [m.group(1) == 'on']
		c.extend(map(int, m.group(2,3,4,5,6,7)))
		assert c[1] <= c[2]
		assert c[3] <= c[4]
		assert c[5] <= c[6]
		cuboids.append(c)
	return cuboids

def segment(ax1, ax2, bx1, bx2):
	if ax1 <= bx1 <= ax2:
		x = []
		if bx1 > ax1:
			x.append((False, ax1, bx1-1))
		if ax2 > bx2:
			x.append((True, bx1, bx2))
			x.append((False, bx2+1, ax2))
		else:
			x.append((True, bx1, ax2))
		return x
	if ax1 <= bx2 <= ax2:
		x = [(True, ax1, bx2)]
		if ax2 > bx2:
			x.append((False, bx2+1, ax2))
		return x
	if bx1 < ax1 < bx2: # implies ax2 < bx2
		return [(True, ax1, ax2)]

	return None

def intersect(a, b):
	# If A and B intersect, break up A into smaller regions that don't intersect with B

	xs = segment(a[1], a[2], b[1], b[2])
	ys = segment(a[3], a[4], b[3], b[4])
	zs = segment(a[5], a[6], b[5], b[6])

	if not (xs and ys and zs):
		return None # A and B don't intersect

	a[0] = False # Turn off A

	return [[True, x1, x2, y1, y2, z1, z2]
		for abx, x1, x2 in xs
		for aby, y1, y2 in ys
		for abz, z1, z2 in zs
			if not (abx and aby and abz)]

def volume(c):
	on, x1, x2, y1, y2, z1, z2 = c
	return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)

def solve(cuboids):
	on_regions = []
	for c in cuboids:
		new_on_regions = []
		for a in on_regions:
			if a[0] and (x := intersect(a, c)):
				new_on_regions.extend(x)
		on_regions.extend(new_on_regions)
		if c[0]:
			on_regions.append(c.copy())
	return sum([volume(a) for a in on_regions if a[0]])

def main():
	cuboids = read_input()
	if not cuboids: return

	init_cuboids = [c for c in cuboids
		if  c[1] >= -50 and c[2] <= 50
		and c[3] >= -50 and c[4] <= 50
		and c[5] >= -50 and c[6] <= 50]

	print('Part 1:', solve(init_cuboids))
	print('Part 2:', solve(cuboids))

if __name__ == '__main__':
	main()
