from collections import defaultdict
import sys

def group_by_range(scanners):
	r2d = defaultdict(set)
	for d, r in scanners:
		r += r - 2
		d %= r
		r2d[r].add(r - d if d else 0)
	return sorted(r2d.items())

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

def get_delay_step(scanners):
	start, step = 0, 1
	for si, (sr, sd) in enumerate(scanners[::-1], start=1):
		s = set(range(sr))
		s.difference_update(sd, *(range(e, sr, r) for r, d in scanners[:-si] if not sr % r for e in d))
		if not s:
			sys.exit('No solution!')
		e = s.pop()
		if not s:
			while start % sr != e: start += step
			step *= sr // gcd(sr, step)
	return start, step

def part1(scanners):
	return sum(d * r for d, r in scanners if not d % (r + r - 2))

def part2_method1(scanners):
	scanners = sorted((2*(r-1), d) for d, r in scanners)
	delay = 0
	while True:
		for r, d in scanners:
			if not (d + delay) % r: break
		else:
			break
		delay += 1
	return delay

def part2_method2(scanners):
	scanners = group_by_range(scanners)
	delay = 0
	while True:
		for r, d in scanners:
			if delay % r in d: break
		else:
			break
		delay += 1
	return delay

def part2_method3(scanners):
	scanners = group_by_range(scanners)
	delay, step = get_delay_step(scanners)
	while True:
		for r, d in scanners:
			if delay % r in d: break
		else:
			break
		delay += step
	return delay

def main():
	part2 = part2_method3
	scanners = [tuple(map(int, line.split(':'))) for line in sys.stdin]
	print('Part 1:', part1(scanners))
	print('Part 2:', part2(scanners))

main()
