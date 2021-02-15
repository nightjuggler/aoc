def make_grid(n):
	return [[((x + 10) * y + n) * (x + 10) // 100 % 10 - 5 for x in range(1, 301)] for y in range(1, 301)]

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', type=int, default=2694) # grid serial number
	parser.add_argument('-x', action='count')
	args = parser.parse_args()

	if args.x == 1:
		for x, y, n in ((122,79,57), (217,196,39), (101,153,71)):
			print('- Fuel cell at {:3},{:3}, grid serial number {}: power level {:2}'.format(
				x, y, n, make_grid(n)[y-1][x-1]))
		return

	grid = make_grid(args.n)

	max_power = -5 * 3 * 3
	max_power_xy = None

	for y in range(300-2):
		for x in range(300-2):
			power = sum([grid[j][i] for i in range(x, x+3) for j in range(y, y+3)])
			if power > max_power:
				max_power = power
				max_power_xy = (x, y)

	x, y = max_power_xy
	print('top-left X,Y = {},{}'.format(x+1, y+1))
	print('total power = {}'.format(max_power))

if __name__ == '__main__':
	main()
