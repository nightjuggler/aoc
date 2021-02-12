import sys

def compute_d(f, i, di, dj, threshold):
	ds = []

	while di + dj < threshold:
		ds.append(di)
		i -= 1
		di = f(i)

	ds.append(di)
	ds.reverse()

	i += len(ds)
	di = f(i)

	while di + dj < threshold:
		ds.append(di)
		i += 1
		di = f(i)

	ds.append(di)
	return ds

def main():
	threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 10000

	xs = []
	ys = []
	for line in sys.stdin:
		x, y = map(int, line.split(', '))
		xs.append(x)
		ys.append(y)

	avg_x = sum(xs) // len(xs)
	avg_y = sum(ys) // len(ys)
	fx = lambda i: sum([abs(i - x) for x in xs])
	fy = lambda i: sum([abs(i - y) for y in ys])
	dx = fx(avg_x)
	dy = fy(avg_y)
	dxs = compute_d(fx, avg_x, dx, dy, threshold)
	dys = compute_d(fy, avg_y, dy, dx, threshold)

	max_i = len(dxs) - 1
	max_j = len(dys) - 1
	area = 0
	for j, dy in enumerate(dys):
		for i, dx in enumerate(dxs):
			if dx + dy < threshold:
				if i == 0 or j == 0 or i == max_i or j == max_j:
					print('{},{} < {}!'.format(i, j, threshold))
				area += 1
	print(area)

if __name__ == '__main__':
	main()
