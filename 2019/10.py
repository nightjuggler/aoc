import sys

def line_of_sight(xys, xy1, xy2):
	x1, y1 = xy1
	x2, y2 = xy2

	gcd = dx = x2 - x1
	mod = dy = y2 - y1
	while mod:
		gcd, mod = mod, gcd % mod

	gcd = abs(gcd)
	if gcd == 1: return True
	dx //= gcd
	dy //= gcd

	for i in range(1, gcd):
		x1 += dx
		y1 += dy
		if (x1, y1) in xys: return False
	return True

def part2(xy1, xys, N):
	inf = 2*max(map(max, xys))
	xys.remove(xy1)

	n = 0
	while True:
		detect = [xy for xy in xys if line_of_sight(xys, xy1, xy)]
		if not detect:
			return None
		n += len(detect)
		if n >= N:
			n -= len(detect)
			break
		xys.difference_update(detect)

	x1, y1 = xy1
	detect = [(x-x1, y1-y) for x, y in detect]

	def k1(xy): x,y = xy; return x/y if y else inf
	def k2(xy): x,y = xy; return -y/x if x else inf
	def k3(xy): x,y = xy; return -x/-y
	def k4(xy): x,y = xy; return y/-x

	def q1(xy): x,y = xy; return x >= 0 and y >= 0
	def q2(xy): x,y = xy; return x >= 0 and y < 0
	def q3(xy): x,y = xy; return x < 0 and y < 0
	def q4(xy): x,y = xy; return x < 0 and y >= 0

	for q, k in (q1, k1), (q2, k2), (q3, k3), (q4, k4):
		xys = list(filter(q, detect))
		n += len(xys)
		if n >= N:
			n -= len(xys)
			xys.sort(key=k)
			x, y = xys[N-1-n]
			return (x+x1)*100 + (y1-y)
	return None

def main():
	asteroids = [[0, (x, y)]
		for y, line in enumerate(sys.stdin)
			for x, c in enumerate(line) if c == '#']
	if not asteroids: return

	xys = set(a[1] for a in asteroids)

	num_asteroids = len(asteroids)
	for i in range(num_asteroids-1):
		a1 = asteroids[i]
		for j in range(i+1, num_asteroids):
			a2 = asteroids[j]
			if line_of_sight(xys, a1[1], a2[1]):
				a1[0] += 1
				a2[0] += 1

	asteroids.sort(reverse=True)
	n, xy1 = asteroids[0]
	print('Part 1:', n)
	print('Part 2:', part2(xy1, xys, 200))

if __name__ == '__main__':
	main()
