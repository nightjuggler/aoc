import sys

def main():
	polymer = [ord(x) for x in sys.stdin.readline().rstrip()]
	assert all([(65 <= x <= 90) or (97 <= x <= 122) for x in polymer])
	diff = ord('a') - ord('A')

	i = 1
	size = len(polymer)
	while i < size:
		if abs(polymer[i] - polymer[i-1]) == diff:
			polymer[i-1:i+1] = []
			size -= 2
			if i > 1:
				i -= 1
		else:
			i += 1

#	print(''.join([chr(x) for x in polymer]))
	print(size)

if __name__ == '__main__':
	main()
