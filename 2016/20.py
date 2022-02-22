import re
import sys

def read_input(size):
	ip = '([1-9][0-9]*|0)'
	pattern = re.compile(f'^{ip}-{ip}$')
	ip_ranges = []
	for line_num, line in enumerate(sys.stdin, start=1):
		m = pattern.match(line)
		if not m:
			sys.exit(f"Input line {line_num} doesn't match pattern!")
		lo, hi = map(int, m.groups())
		assert lo <= hi < size
		ip_ranges.append((lo, hi + 1))
	return ip_ranges

def main():
	size = 1<<32
	ip_ranges = read_input(size)

	ips = [0, size]
	for lo, hi in ip_ranges:
		ips.append(lo)
		ips.append(hi)

	ips = sorted(set(ips))
	firewall = [True] * len(ips)
	firewall[-1] = False

	for lo, hi in ip_ranges:
		lo = ips.index(lo)
		hi = ips.index(hi, lo)
		firewall[lo:hi] = [False] * (hi - lo)

	min_allowed = None
	num_allowed = 0
	for i, allowed in enumerate(firewall):
		if allowed:
			if min_allowed is None:
				min_allowed = ips[i]
			num_allowed += ips[i+1] - ips[i]

	print('Part 1:', min_allowed)
	print('Part 2:', num_allowed)

if __name__ == '__main__':
	main()
