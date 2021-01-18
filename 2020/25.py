import sys

def transform_naive(n, k):
	value = 1
	for i in range(k):
		value = (value * n) % 20201227

	print('Encryption key for n={} and k={} is {}'.format(n, k, value))
	return value

def find_loop_size_naive(n):
	value = 1
	i = 0
	while value != n:
		if i == 10000000:
			print('Giving up on finding the loop size for {}!'.format(n))
			return None
		value = (value * 7) % 20201227
		i += 1

	print('Loop size for {} is {}'.format(n, i))
	return i

def main(input_file):
	pk1 = int(next(input_file))
	pk2 = int(next(input_file))

	ls1 = find_loop_size_naive(pk1)
	ls2 = find_loop_size_naive(pk2)

	ek1 = transform_naive(pk2, ls1)
	ek2 = transform_naive(pk1, ls2)
	assert ek1 == ek2

if __name__ == '__main__':
	main(sys.stdin)
