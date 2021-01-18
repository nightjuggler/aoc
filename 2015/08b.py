import sys

def main(input_file):
	backslash = '\\'
	doublequote = '\"'
	hexdigits = '0123456789abcdef'
	size_diff = 0
	for line in input_file:
		k = len(line) - 1
		j = k - 1
		assert j > 0
		assert line[0] == doublequote
		assert line[j] == doublequote
		assert line[k] == '\n'
		size_diff += 4
		i = 1
		while i < j:
			c = line[i]
			if c == backslash:
				size_diff += 1
				i += 1
				assert i < j
				c = line[i]
				if c == 'x':
					i += 2
					assert i < j
					assert line[i - 1] in hexdigits
					assert line[i] in hexdigits
				else:
					assert c == backslash or c == doublequote
					size_diff += 1
			i += 1
	print(size_diff)

if __name__ == '__main__':
	main(sys.stdin)
