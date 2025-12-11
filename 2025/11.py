import re
import sys

def part1(devs, start):
	cache = {}
	def solve(dev):
		if dev in cache: return cache[dev]
		cache[dev] = paths = sum(1 if d == 'out' else solve(d) for d in devs[dev])
		return paths
	return solve(start) if start in devs else None

def part2(devs, start):
	cache = {}
	def solve(dev):
		if dev in cache: return cache[dev]
		cache[dev] = paths = [0]*4
		visited = 1 if dev == 'dac' else 2 if dev == 'fft' else 0
		for d in devs[dev]:
			if d == 'out':
				paths[visited] += 1
			else:
				for v, p in enumerate(solve(d)):
					paths[visited | v] += p
		return paths
	return solve(start)[3] if start in devs else None

def main(f):
	devs = {}
	pattern = re.compile('^[a-z]{3}:(?: [a-z]{3})+$')
	for line_num, line in enumerate(f, start=1):
		if not pattern.match(line):
			return f'Line {line_num} doesn\'t match the expected pattern!'
		devs[line[:3]] = line[5:].split()
	print('Part 1:', part1(devs, 'you'))
	print('Part 2:', part2(devs, 'svr'))

if __name__ == '__main__':
	sys.exit(main(sys.stdin))
