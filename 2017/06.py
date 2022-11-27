import sys

def main():
	banks = list(map(int, sys.stdin.readline().split()))
	num_banks = len(banks)

	seen = {}
	max_index = 0
	max_value = banks[0]
	for i, v in enumerate(banks):
		if v > max_value:
			max_value = v
			max_index = i
	while (key := tuple(banks)) not in seen:
		seen[key] = len(seen)
		d, r = divmod(max_value, num_banks)
		max_value = banks[max_index] = 0
		j = max_index + 1
		for i, v in enumerate(banks):
			v += d
			if (i - j) % num_banks < r:
				v += 1
			banks[i] = v
			if v > max_value:
				max_value = v
				max_index = i
	print('Part 1:', len(seen))
	print('Part 2:', len(seen) - seen[key])

main()
