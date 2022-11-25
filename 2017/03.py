import argparse
import math

def part1_method1(square):
	print('Part 1, Method 1')
	d = 0
	n = 1
	while square > n:
		d += 1
		n += 8*d
	return d, n

def part1_method2(square):
	print('Part 1, Method 2')
	d = math.ceil((math.sqrt(square) - 1)/2)
	n = (2*d + 1)**2
	return d, n

def part1(args):
	square = args.input
	method = (
		part1_method1,
		part1_method2,
	)[args.method - 1]

	d, n = method(square)
	if d:
		d += abs((n - square) % (2*d) - d)
	return d

def part2(args):
	value = args.input
	grid = {}
	x = y = 0
	w = v = 1
	if v > value: return v
	grid[x,y] = v
	while True:
		w += 2
		x += 1
		v = 0
		p = x-1
		for y in range(y, y + w - 1):
			v += sum(grid.get(xy, 0) for xy in ((p,y-1), (p,y), (p,y+1)))
			if v > value: return v
			grid[x,y] = v
		p = y-1
		for x in range(x - 1, x - w, -1):
			v += sum(grid.get(xy, 0) for xy in ((x-1,p), (x,p), (x+1,p)))
			if v > value: return v
			grid[x,y] = v
		p = x+1
		for y in range(y - 1, y - w, -1):
			v += sum(grid.get(xy, 0) for xy in ((p,y-1), (p,y), (p,y+1)))
			if v > value: return v
			grid[x,y] = v
		p = y+1
		for x in range(x + 1, x + w):
			v += sum(grid.get(xy, 0) for xy in ((x-1,p), (x,p), (x+1,p)))
			if v > value: return v
			grid[x,y] = v
	return None

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('input', nargs='?', type=int, default=312051)
	parser.add_argument('-m', '--method', type=int, choices=range(1, 3), default=1)
	args = parser.parse_args()

	if args.input < 1:
		sys.exit('The input value must be >= 1!')
	print('Part 1:', part1(args))
	print('Part 2:', part2(args))

if __name__ == '__main__':
	main()
