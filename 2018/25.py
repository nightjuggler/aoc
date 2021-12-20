import re
import sys

def read_input():
	n = '(0|-?[1-9][0-9]*)'
	line_pattern = re.compile(f'^{n},{n},{n},{n}$')
	points = []
	for line_number, line in enumerate(sys.stdin, start=1):
		m = line_pattern.match(line)
		if not m:
			print(f'Input line {line_number} doesn\'t match expected pattern!')
			return None
		points.append(tuple(map(int, m.groups())))
	return points

def main():
	points = read_input()
	if not points: return

	num_points = len(points)
	point_constellation = [0] * num_points
	max_constellation = 0

	for i in range(num_points):
		p1 = points[i]
		c1 = point_constellation[i]
		if c1 == 0:
			max_constellation += 1
			c1 = point_constellation[i] = max_constellation
		for j in range(i+1, num_points):
			p2 = points[j]
			c2 = point_constellation[j]
			d = sum([abs(a - b) for a, b in zip(p1, p2)])
			if d <= 3:
				if c2 == 0:
					point_constellation[j] = c1
				elif c2 != c1:
					# keep c1, merge c2 into c1
					if c1 > c2: c1, c2 = c2, c1
					for k in range(num_points):
						if point_constellation[k] == c2:
							point_constellation[k] = c1
	print(len(set(point_constellation)))

if __name__ == '__main__':
	main()
