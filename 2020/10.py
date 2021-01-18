import sys

def main():
	adapters = [int(line.strip()) for line in sys.stdin]
	adapters.sort()

	num1 = 0
	num3 = 1
	prev = 0

	for n in adapters:
		diff = n - prev
		if diff == 1:
			num1 += 1
		elif diff == 3:
			num3 += 1
		elif diff != 2:
			sys.exit('Wtf?')
		prev = n

	print(num1, '1-jolt differences')
	print(num3, '3-jolt differences')
	print(num1, '*', num3, '=', num1 * num3)

if __name__ == '__main__':
	main()
