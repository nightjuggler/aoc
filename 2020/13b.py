import sys

def err(message, *args):
	sys.exit(message.format(*args))

def extended_euclid(a, b):
	# Extended Euclidean algorithm for finding the greatest common divisor and Bezout coefficients of a and b
	x, x1 = 1, 0
	y, y1 = 0, 1
	while b != 0:
		q, r = divmod(a, b)
		a, b = b, r
		x, x1 = x1, x - q * x1
		y, y1 = y1, y - q * y1
	return a, x, y

def chinese_remainder(c):
	# c is a list of (remainder, divisor) tuples
	a1, n1 = c.pop(0)
	print(a1, n1)
	for a2, n2 in c:
		print(a2, n2)
		gcd, m1, m2 = extended_euclid(n1, n2)
		if gcd != 1:
			err('{} and {} are not coprime (gcd = {})!', n1, n2, gcd)
		a1 = a1 * m2 * n2 + a2 * m1 * n1
		n1 *= n2
		a1 %= n1
		print('=>', a1, n1)
	return a1

def main(input):
	next(input)

	# Find t such that for each (i, bus), t % bus = (bus-i) % bus, i.e. t = bus-i (mod bus)

	buses = []
	for i, bus in enumerate(next(input).strip().split(',')):
		if bus != 'x':
			bus = int(bus)
			buses.append(((bus - i) % bus, bus))

	print(chinese_remainder(buses))

if __name__ == '__main__':
	main(sys.stdin)
