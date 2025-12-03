import argparse
import re
import sys

def part1(ranges):
	result = 0
	for r in ranges:
		start = r.start
		stop = r.stop
		digits = len(str(start))
		next_start = 10**digits
		if digits % 2:
			start = next_start
			next_start *= 10
			digits += 1
		m = 10**(digits//2)
		while True:
			next_start = min(next_start, stop)
			half_start, other_half = divmod(start, m)
			if other_half > half_start: half_start += 1
			half_stop, other_half = divmod(next_start - 1, m)
			if other_half >= half_stop: half_stop += 1
			result += sum(range(half_start, half_stop)) * (m + 1)
			if next_start == stop: break
			start = next_start * 10
			next_start *= 100
			m *= 10
	return result

def part2(ranges):
	result = 0
	for r in ranges:
		seen = set()
		start = r.start
		stop = r.stop
		digits = len(str(start))
		next_start = 10**digits
		while True:
			next_start = min(next_start, stop)
			for reps in range(2, digits+1):
				d, m = divmod(digits, reps)
				if m: continue
				m = 10**(digits-d)
				a = start//m
				b = (next_start-1)//m
				m = sum(10**x for x in range(d, digits, d)) + 1
				if start > a*m: a += 1
				if stop > b*m: b += 1
				seen.update(n*m for n in range(a, b))
			if next_start == stop: break
			start = next_start
			next_start *= 10
			digits += 1
		result += sum(seen)
	return result

def part1_str(ranges):
	return sum(n for r in ranges for n in r if (s:=str(n))[:(i:=len(s)//2)] == s[i:])
def part2_str(ranges):
	return sum(n for r in ranges for n in r if (s:=str(n)) in (s+s)[1:-1])

def solve_re(ranges, pattern):
	pattern = re.compile(pattern)
	return sum(n for r in ranges for n in r if pattern.fullmatch(str(n)))

def main(f):
	args = argparse.ArgumentParser(allow_abbrev=False)
	args.add_argument('-r', '--re', action='store_true')
	args.add_argument('-s', '--str', action='store_true')
	args = args.parse_args()

	line = f.readline().strip()
	n = '[1-9][0-9]*'
	if not re.fullmatch(f'{n}-{n}(?:,{n}-{n})*', line):
		return 'The input doesn\'t match the expected pattern!'
	ranges = []
	for r in line.split(','):
		first, last = r.split('-')
		ranges.append(range(int(first), int(last)+1))
	if args.re:
		print('Part 1:', solve_re(ranges, fr'({n})\1'))
		print('Part 2:', solve_re(ranges, fr'({n})\1+'))
	elif args.str:
		print('Part 1:', part1_str(ranges))
		print('Part 2:', part2_str(ranges))
	else:
		print('Part 1:', part1(ranges))
		print('Part 2:', part2(ranges))

if __name__ == '__main__':
	sys.exit(main(sys.stdin))
