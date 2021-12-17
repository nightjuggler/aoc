import re
import sys

def read_input():
	n = '(0|-?[1-9][0-9]*)'
	line_pattern = re.compile(f'^pos=<{n},{n},{n}>, r=([1-9][0-9]*)$')
	line_number = 0

	nanobots = []
	for line in sys.stdin:
		line_number += 1
		m = line_pattern.match(line)
		if not m:
			print(f'Input line {line_number} doesn\'t match pattern!')
			return None
		x, y, z, r = map(int, m.groups())
		nanobots.append((r, x, y, z))
	return nanobots

def part1(bots):
	bots.sort(reverse=True)
	if len(bots) > 1 and bots[0][0] == bots[1][0]:
		print('More than one nanobot has the largest signal radius!')
		return
	r, x, y, z = bots[0]
	print(f'The nanobot at {x},{y},{z} has the largest signal radius {r}.')

	n = 0
	for r2, x2, y2, z2 in bots:
		if abs(x2-x) + abs(y2-y) + abs(z2-z) <= r:
			n += 1

	print(n, 'nanobots are in range of the nanobot with the largest signal radius.')

# If we have 3 equations like the following:
#
# a1*x + b1*y + c1*z = d1
# a2*x + b2*y + c2*z = d2
# a3*x + b3*y + c3*z = d3
#
#              | a1 b1 c1 |         | x |         | d1 |
# Then let A = | a2 b2 c2 | and X = | y | and D = | d2 |
#              | a3 b3 c3 |         | z |         | d3 |
#
# So A * X = D
#
# Thus X = D multiplied by the inverse of A
# We can use Cramer's rule to solve for x, y, and z

def det(a, b, c, d, e, f, g, h, i):
	# Determinant for a 3x3 matrix
	# | a b c |
	# | d e f |
	# | g h i |
	return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)

def cramers_rule(coeffs):
	m = []
	n = []
	for abc, d in coeffs.items():
		m.extend(abc)
		n.append(d)
		if len(n) == 3: break
	if len(n) != 3:
		return None
	D = det(*m)
	if not D:
		return None
	s = []
	for i in range(3):
		c = m[i::3]
		m[i::3] = n
		s.append(det(*m) // D)
		m[i::3] = c
	return s

def solve(bots, indices):
	bots_len = len(indices)
	# Not necessary to determine the min/max x,y,z to solve the puzzle, but they can be
	# a nice sanity check when solving for x, y, and z. So I'm keeping this in for now.
	minmax = [[], [], []]
	coeffs = {}
	for i in range(bots_len-1):
		b1 = indices[i]
		r1, x1, y1, z1 = bots[b1]
		for j in range(i+1, bots_len):
			b2 = indices[j]
			r2, x2, y2, z2 = bots[b2]
			d = abs(x2-x1) + abs(y2-y1) + abs(z2-z1)
			if r1 + r2 == d:
				for m, (c1, c2, d1, d2) in zip(minmax, (
					(x1, x2, r1, r2) if x1 <= x2 else (x2, x1, r2, r1),
					(y1, y2, r1, r2) if y1 <= y2 else (y2, y1, r2, r1),
					(z1, z2, r1, r2) if z1 <= z2 else (z2, z1, r2, r1))):
					c1 = max(c2 - d2, c1)
					c2 = min(c1 + d1, c2)
					if m:
						if c1 > m[0]: m[0] = c1
						if c2 < m[1]: m[1] = c2
					else:
						m[:] = c1, c2

				# abs(x-x1) + abs(y-y1) + abs(z-z1) = r1
				# x1 <= x2 implies x1 <= x which implies abs(x-x1) = x-x1
				# x1 >  x2 implies x1 >  x which implies abs(x-x1) = x1-x
				a = 1 if x1 <= x2 else -1
				b = 1 if y1 <= y2 else -1
				c = 1 if z1 <= z2 else -1
				d = r1 + a*x1 + b*y1 + c*z1
				abc = (a, b, c)
				if d < 0 and abc != (1, 1, 1):
					abc, d = (-a, -b, -c), -d
				coeffs[abc] = d

				a = 1 if x2 <= x1 else -1
				b = 1 if y2 <= y1 else -1
				c = 1 if z2 <= z1 else -1
				d = r2 + a*x2 + b*y2 + c*z2
				abc = (a, b, c)
				if d < 0 and abc != (1, 1, 1) or abc == (-1,-1,-1):
					abc, d = (-a, -b, -c), -d
				coeffs[abc] = d

	if not coeffs:
		print('Unable to solve for x, y, and z!')
		return

	for m, c in zip(minmax, 'xyz'):
		print(f'{m[0]:,} <= {c} <= {m[1]:,}')

	print('To find x, y, and z, solve the following equations:')
	for (a, b, c), d in coeffs.items():
		a = '' if a == 1 else '-'
		b = '' if b == 1 else '-'
		c = '' if c == 1 else '-'
		print(f'{a}x + {b}y + {c}z = {d}')

	xyz = cramers_rule(coeffs)
	if not xyz:
		print('Unable to use Cramer\'s rule to solve for x, y, and z!')
		if not all([m[0] >= 0 for m in minmax]):
			return
		d = coeffs.get((1, 1, 1))
		if d is not None:
			print('However, since we\'ve determined that x, y, and z must all be non-negative,')
			print('and we have an equation for x + y + z, the answer is', d)
		return

	print('x, y, z = ({})'.format(', '.join(map(str, xyz))))
	d = sum(map(abs, xyz))
	print('So the answer is |x| + |y| + |z| =', d)

def part2(bots):
	bots.sort(reverse=True)
	bots_len = len(bots)

	print('Finding all range intersections ...')
	intersects = [set() for i in range(bots_len)]
	for i in range(bots_len-1):
		r1, x1, y1, z1 = bots[i]
		s = intersects[i]
		for j in range(i+1, bots_len):
			r2, x2, y2, z2 = bots[j]
			d = abs(x2-x1) + abs(y2-y1) + abs(z2-z1)
			if r1 + r2 >= d:
				s.add(j)

	max_size = 0
	max_size_sets = []

	def recurse(x, s):
		nonlocal max_size, max_size_sets
		# The ranges of all the bots in x intersect the ranges of all the bots in x and s,
		# but the ranges of the bots in s may not all intersect each other.

		x_size = len(x)
		if x_size > max_size:
			max_size = x_size
			max_size_sets = [x.copy()]
		elif x_size == max_size:
			max_size_sets.append(x.copy())
		elif x_size + len(s) < max_size:
			return

		for j in sorted(s):
			x.append(j)
			recurse(x, s & intersects[j])
			x.pop()

	print('Finding the largest set of nanobots whose ranges all intersect ...')
	for i, s in enumerate(intersects):
		recurse([i], s)

	print('The largest such set has', max_size, 'nanobots.')
	if len(max_size_sets) == 1:
		print('There is one such set of that size.')
	else:
		print('There are', len(max_size_sets), 'different sets of that size.')

	for i, indices in enumerate(max_size_sets, start=1):
		print(f'-------------------- Set #{i} --------------------')
		solve(bots, indices)

# The puzzle input results in the following three equations:
#
# (1) x + y + z = 113799398
# (2) -x + y + z = 2697038
# (3) x + -y + z = 35840114
#
# Solving these gives x, y, z = (55551180, 38979642, 19268576)
#
# I constructed the following example to help me visualize the problem.
# A, B, and C all intersect each other such that for each pair, the sum
# of their radii equals the Manhattan distance between them.
#
# 9 .....b...
# 8 ....bbb..
# 7 ...bbbbb.
# 6 ..xbbBbbb
# 5 .aaxbbbb.
# 4 aaAaPbb..
# 3 .aaycz...
# 2 ..ycCcc..
# 1 ...ccc...
# 0 ....c....
#   012345678
# A: pos=<2,4>, r=2
# B: pos=<5,6>, r=3
# C: pos=<4,2>, r=2
# x = a & b
# y = a & c
# z = b & c
# P = a & b & c
#
# Eq.1: (Bx - x) + (By - y) = Br
#    => 5 - x + 6 - y = 3
#    => x + y = 8
#
# Eq.2: (Cx - x) + (y - Cy) = Cr
#    => 4 - x + y - 2 = 2
#    => x - y = 0
#    => x = y
#    => 2x = 8
#    => x = 4 and y = 4
#
# So the point P where the ranges of A, B, and C intersect is <4,4>

def main():
	bots = read_input()
	if not bots:
		return
	part1(bots)
	part2(bots)

if __name__ == '__main__':
	main()
