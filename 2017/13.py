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
	for s, (r, d) in enumerate(scanners[::-1], start=1):
		others = [(r2, d2) for r2, d2 in scanners[:-s] if not r % r2]
		v = None
		for i in range(r):
			for r2, d2 in others:
				if i % r2 in d2: break
			else:
				if i not in d:
					if v is not None: break
					v = i
		else:
			if v is not None:
				while start % r != v: start += step
				step *= r // gcd(r, step)
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
