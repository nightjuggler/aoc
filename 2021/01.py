import sys

def part1():
	increases = 0
	prev = None
	for line in sys.stdin:
		n = int(line)
		if prev is not None and n > prev:
			increases += 1
		prev = n
	print(increases)

def part2():
	increases = 0
	prev1, prev2, prev_sum = None, None, None
	for line in sys.stdin:
		n = int(line)
		if prev2 is not None:
			curr_sum = n + prev1 + prev2
			if prev_sum is not None and curr_sum > prev_sum:
				increases += 1
			prev_sum = curr_sum
		prev2 = prev1
		prev1 = n
	print(increases)

if __name__ == '__main__':
	part2()
