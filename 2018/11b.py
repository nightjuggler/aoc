def make_grid(n):
	return [[((x + 10) * y + n) * (x + 10) // 100 % 10 - 5 for x in range(1, 301)] for y in range(1, 301)]

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', type=int, default=2694) # grid serial number
	args = parser.parse_args()

	grid = make_grid(args.n)
	col_cache = [row.copy() for row in grid]
	row_cache = [row.copy() for row in grid]
	sqr_cache = [row.copy() for row in grid]

	max_power = -6
	max_power_xy = None

	for y in range(300):
		for x in range(300):
			power = grid[y][x]
			if power > max_power:
				max_power = power
				max_power_xy = (x, y, 0)

	for size in range(1, 300):
		stop = 300 - size
		for y in range(stop):
			for x in range(stop):
				i = x + size
				j = y + size
				r = row_cache[j][x]
				c = col_cache[y][i]
				p = grid[j][i]
				sqr_cache[y][x] = power = sqr_cache[y][x] + r + c + p
				row_cache[j][x] = r + p
				col_cache[y][i] = c + p
				if power > max_power:
					max_power = power
					max_power_xy = (x, y, size)

	x, y, size = max_power_xy
	print('X,Y,size = {},{},{}'.format(x+1, y+1, size+1))
	print('total power = {}'.format(max_power))

if __name__ == '__main__':
	main()
