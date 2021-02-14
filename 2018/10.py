import re
import sys

def main():
	points = []
	line_pattern = re.compile('^position=<{n},{n}> velocity=<{n},{n}>$'.format(n=' *(-?[1-9][0-9]*|0)'))
	for i, line in enumerate(sys.stdin, start=1):
		m = line_pattern.match(line)
		if not m:
			print('Line {} doesn\'t match pattern!'.format(i))
			return
		points.append(list(map(int, m.groups())))
	if not points:
		print('Wtf?')
		return

	min_x = max_x = min_y = max_y = None
	for x, y, dx, dy in points:
		if min_x is None:
			min_x = max_x = x
			min_y = max_y = y
		else:
			if   x < min_x: min_x = x
			elif x > max_x: max_x = x
			if   y < min_y: min_y = y
			elif y > max_y: max_y = y
	prev_area = (max_x - min_x) * (max_y - min_y)

	t = 0
	while True:
		t += 1
		min_x = max_x = min_y = max_y = None
		for p in points:
			x, y, dx, dy = p
			x += dx
			y += dy
			p[0] = x
			p[1] = y
			if min_x is None:
				min_x = max_x = x
				min_y = max_y = y
			else:
				if   x < min_x: min_x = x
				elif x > max_x: max_x = x
				if   y < min_y: min_y = y
				elif y > max_y: max_y = y
		area = (max_x - min_x) * (max_y - min_y)
		if area >= prev_area:
			break
		prev_area = area

	print(t - 1)
	min_x = max_x = min_y = max_y = None
	for p in points:
		x, y, dx, dy = p
		x -= dx
		y -= dy
		p[0] = x
		p[1] = y
		if min_x is None:
			min_x = max_x = x
			min_y = max_y = y
		else:
			if   x < min_x: min_x = x
			elif x > max_x: max_x = x
			if   y < min_y: min_y = y
			elif y > max_y: max_y = y

	w = max_x - min_x + 1
	h = max_y - min_y + 1
	print(w, 'x', h)
	grid = [[False] * w for y in range(h)]
	for x, y, dx, dy in points:
		grid[y - min_y][x - min_x] = True
	for row in grid:
		print(''.join(['#' if p else '.' for p in row]))

if __name__ == '__main__':
	main()
