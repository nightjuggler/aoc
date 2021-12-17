import re
import sys

def read_input():
	n = '(0|-?[1-9][0-9]*)'
	line_pattern = re.compile(f'^target area: x={n}\\.\\.{n}, y={n}\\.\\.{n}$')
	line = sys.stdin.readline()
	m = line_pattern.match(line)
	if not m:
		print('The input doesn\'t match the expected pattern!')
		return None
	return list(map(int, m.groups()))

def main():
	target = read_input()
	if not target:
		return
	xmin, xmax, ymin, ymax = target
	if not ((0 < xmin <= xmax) and (ymin <= ymax < 0)):
		print('The target area must be below and to the right of the initial position!')
		return

	n = 0
	best_y = 0
	best_v = []
	for try_vy in range(ymin, -ymin + 1):
		for try_vx in range(xmax, 0, -1):
			vx, vy = try_vx, try_vy
			x, y, max_y = 0, 0, 0
			while True:
				x += vx
				y += vy
				if y > max_y:
					max_y = y
				if xmin <= x <= xmax and ymin <= y <= ymax:
					n += 1
					if max_y >= best_y:
						if max_y > best_y:
							best_y = max_y
							best_v.clear()
						best_v.append((try_vx, try_vy))
					break
				elif x > xmax or y < ymin:
					break
				if vx > 0:
					vx -= 1
				elif x < xmin:
					break
				vy -= 1
			if x < xmin:
				break

	print('Part 1:', best_y, best_v)
	print('Part 2:', n)

if __name__ == '__main__':
	main()
