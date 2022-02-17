from collections import deque

# (x+y)*(x+y) = x*x + 2*x*y + y*y
# f(x, y) = x*x + 3*x + 2*x*y + y + y*y = (x+y)**2 + 3*x + y
#
# f(x+1, y) = (x+y+1)**2 + 3*(x+1) + y
#           = (x+y)**2 + 2*(x+y) + 1 + 3*x + 3 + y
#           = (x+y)**2 + 3*x + y + 2*(x+y) + 4
#           = f(x, y) + 2*(x+y+2)
#
# => f(x, y) = f(x+1, y) - 2*(x+y+2)
# => f(x-1, y) = f(x, y) - 2*(x+y+1)
#
# f(x, y+1) = (x+y+1)**2 + 3*x + y + 1
#           = (x+y)**2 + 2*(x+y) + 1 + 3*x + y + 1
#           = (x+y)**2 + 3*x + y + 2*(x+y) + 2
#           = f(x, y) + 2*(x+y+1)
#
# => f(x, y) = f(x, y+1) - 2*(x+y+1)
# => f(x, y-1) = f(x, y) - 2*(x+y)

def f_xy(x, y):
	return x*x + 3*x + 2*x*y + y + y*y

def solve(n, start_xy, end_xy=None):
	bits = {}
	seen = set()

	q = deque()
	q.append((0, *start_xy, n + f_xy(*start_xy)))

	while q:
		steps, x, y, n = q.popleft()

		oddbits = bits.get(n)
		if oddbits is None:
			oddbits = False
			m = n
			while m:
				m &= m - 1
				oddbits = not oddbits
			bits[n] = oddbits
		if oddbits:
			continue

		xy = (x, y)
		if xy in seen:
			continue
		seen.add(xy)

		if end_xy:
			if xy == end_xy:
				return steps
		elif steps == 50:
			continue

		steps += 1
		xy = 2*(x+y)

		q.append((steps, x+1, y, n+xy+4))
		q.append((steps, x, y+1, n+xy+2))
		if y: q.append((steps, x, y-1, n-xy))
		if x: q.append((steps, x-1, y, n-xy-2))

	return None if end_xy else len(seen)

def main():
	print('Example Part 1:', solve(10, (1, 1), (7, 4)))
	print('Example Part 2:', solve(10, (1, 1)))
	print('Part 1:', solve(1352, (1, 1), (31, 39)))
	print('Part 2:', solve(1352, (1, 1)))

if __name__ == '__main__':
	main()
