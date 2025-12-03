import sys

def solve(jolts, maxlen, seqlen):
	max_jolts = 0
	min_index = -1
	for max_index in range(maxlen - seqlen, maxlen):
		max_jolts *= 10
		for j, indices in jolts:
			for i in indices:
				if i > min_index: break
			else:
				continue
			if i <= max_index:
				min_index = i
				max_jolts += j
				break
	return max_jolts

def main():
	total1 = total2 = 0
	for line in sys.stdin:
		line = line.strip()
		size = len(line)
		jolts = [[] for j in range(10)]
		for i, j in enumerate(map(int, line)):
			jolts[j].append(i)
		jolts = list(enumerate(jolts))[::-1]
		total1 += solve(jolts, size, 2)
		total2 += solve(jolts, size, 12)
	print('Part 1:', total1)
	print('Part 2:', total2)

if __name__ == '__main__':
	main()
