import sys

def solve(jolts, seqlen):
	num_batteries = sum(map(len, jolts))
	jolts = list(enumerate(jolts))[::-1]
	max_joltage = 0
	min_index = -1
	for max_index in range(num_batteries - seqlen, num_batteries):
		max_joltage *= 10
		for j, indices in jolts:
			for i in indices:
				if i > min_index: break
			else:
				continue
			if i <= max_index:
				min_index = i
				max_joltage += j
				break
	return max_joltage

def main():
	total1 = total2 = 0
	for line in sys.stdin:
		jolts = [[] for j in range(10)]
		for i, j in enumerate(map(int, line.strip())):
			jolts[j].append(i)
		total1 += solve(jolts, 2)
		total2 += solve(jolts, 12)
	print('Part 1:', total1)
	print('Part 2:', total2)

if __name__ == '__main__':
	main()
