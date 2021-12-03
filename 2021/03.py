import sys

def part1():
	numbers = [line.rstrip() for line in sys.stdin]
	N = len(numbers)
	zerofreq = [0] * len(numbers[0])
	for n in numbers:
		for i, digit in enumerate(n):
			if digit == '0':
				zerofreq[i] += 1

	gamma = 0
	epsilon = 0
	for shift, freq in enumerate(zerofreq[::-1]):
		if 2*freq < N:
			gamma += 1 << shift
		else:
			epsilon += 1 << shift

	print('gamma =', gamma)
	print('epsilon =', epsilon)
	print('gamma * epsilon =', gamma * epsilon)

def get_rating(keep, d1, d2):
	N = len(keep)
	pos = 0
	while N > 1:
		zerofreq = 0
		for n in keep:
			if n[pos] == '0':
				zerofreq += 1
		digit = d1 if 2*zerofreq <= N else d2
		keep = [n for n in keep if n[pos] == digit]
		N = len(keep)
		pos += 1
	return int(keep[0], 2)

def get_rating2(keep, co2):
	pos = 0
	while len(keep) > 1:
		zeros, ones = [], []
		for n in keep:
			(zeros if n[pos] == '0' else ones).append(n)
		keep_ones = len(ones) >= len(zeros)
		if co2: keep_ones = not keep_ones
		keep = ones if keep_ones else zeros
		pos += 1
	return int(keep[0], 2)

def part2():
	numbers = [line.rstrip() for line in sys.stdin]

	oxygen = get_rating(numbers, '1', '0')
	co2 = get_rating(numbers, '0', '1')

	print(f'oxygen = {oxygen}, CO2 = {co2}, oxygen * CO2 = {oxygen * co2}')

	oxygen = get_rating2(numbers, False)
	co2 = get_rating2(numbers, True)

	print(f'oxygen = {oxygen}, CO2 = {co2}, oxygen * CO2 = {oxygen * co2}')

if __name__ == '__main__':
	if len(sys.argv) == 1:
		part1()
	elif len(sys.argv) != 2 or sys.argv[1] != '2':
		print('usage: wtf?')
	else:
		part2()
