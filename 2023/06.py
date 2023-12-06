import sys

def solve(t, d):
	return sum(1 for s in range(1, t) if (t-s)*s > d)

def solve(t, d):
	# (t-s)*s > d => s*s - t*s + d < 0
	# Use the quadratic formula to solve s*s - t*s + d = 0
	# s = (t +- sqrt(t*t - 4*d)) / 2

	r = t*t - 4*d
	if r < 0: return 0
	r **= 0.5

	s_max = (t + r) / 2
	s_min = (t - r) / 2

	# Return the number of integers > s_min and < s_max

	s_max = int(s_max) - s_max.is_integer()
	s_min = int(s_min) + 1

	return 0 if s_max < s_min else s_max - s_min + 1

def part1(times, distances):
	product = 1
	for t, d in zip(map(int, times), map(int, distances)):
		product *= solve(t, d)
	return product

def part2(times, distances):
	t = int(''.join(times))
	d = int(''.join(distances))
	return solve(t, d)

def main(f):
	times = f.readline().removeprefix('Time:').split()
	distances = f.readline().removeprefix('Distance:').split()

	print('Part 1:', part1(times, distances))
	print('Part 2:', part2(times, distances))

main(sys.stdin)
