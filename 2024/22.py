import sys

def solve(secrets):
	size = 19**4 # Price changes range from -9 to 9 (19 possible values)
	totals = [0]*size
	part1_sum = 0
	for secret in secrets:
		seen = set()
		price1 = secret % 10
		changes = 0
		for i in range(2000):
			secret ^= secret << 6
			secret %= 16777216
			secret ^= secret >> 5
			secret %= 16777216
			secret ^= secret << 11
			secret %= 16777216
			price2 = secret % 10
			changes = changes * 19 % size + 9 + price2 - price1
			if i > 2 and changes not in seen:
				seen.add(changes)
				totals[changes] += price2
			price1 = price2
		part1_sum += secret
	print('Part 1:', part1_sum)
	print('Part 2:', max(totals))

solve(list(map(int, sys.stdin)))
