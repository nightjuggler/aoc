from collections import deque
import sys

def main():
	lines = [line.strip() for line in sys.stdin]
	size = len(lines)
	assert size and all(len(line) == size for line in lines)

	plots = [[0] * size for y in range(size)]
	areas = [0]
	perims = [0]
	sides = [0]
	num_plots = 0
	max_xy = size - 1
	q = deque()

	for y1, row in enumerate(plots):
		for x1, plot in enumerate(row):
			if plot: continue
			num_plots += 1
			area = perim = 0
			label = lines[y1][x1]
			q.append((x1, y1))
			while q:
				x, y = q.popleft()
				if plots[y][x]: continue
				plots[y][x] = num_plots
				area += 1
				if y and label == lines[y-1][x]:
					q.append((x, y-1))
				else:
					perim += 1
				if x and label == lines[y][x-1]:
					q.append((x-1, y))
				else:
					perim += 1
				if y < max_xy and label == lines[y+1][x]:
					q.append((x, y+1))
				else:
					perim += 1
				if x < max_xy and label == lines[y][x+1]:
					q.append((x+1, y))
				else:
					perim += 1
			areas.append(area)
			perims.append(perim)
			sides.append(0)

	def count_sides():
		for y, row in enumerate(plots):
			prev1 = prev2 = 0
			for x, plot in enumerate(row):
				if y and plots[y-1][x] == plot:
					prev1 = 0
				elif prev1 != plot:
					prev1 = plot
					sides[plot] += 1
				if y < max_xy and plots[y+1][x] == plot:
					prev2 = 0
				elif prev2 != plot:
					prev2 = plot
					sides[plot] += 1
	count_sides()
	plots = list(zip(*plots[::-1]))
	count_sides()

	print('Part 1:', sum(a * n for a, n in zip(areas, perims)))
	print('Part 2:', sum(a * n for a, n in zip(areas, sides)))

main()
