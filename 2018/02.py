import sys

def main():
	total2 = 0
	total3 = 0
	for line in sys.stdin:
		line = line.rstrip()
		count = [0] * 26
		exactly2 = 0
		exactly3 = 0
		for c in line:
			c = ord(c) - 97
			assert 0 <= c <= 25
			count[c] = n = count[c] + 1
			if n == 2:
				exactly2 += 1
			elif n == 3:
				exactly2 -= 1
				exactly3 += 1
			elif n == 4:
				exactly3 -= 1
		if exactly2:
			total2 += 1
		if exactly3:
			total3 += 1
	print(total2, '*', total3, '=', total2 * total3)

if __name__ == '__main__':
	main()
