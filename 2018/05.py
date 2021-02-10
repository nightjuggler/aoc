import sys

def react(polymer):
	diff = ord('a') - ord('A')

	size = len(polymer)
	if size == 0:
		return 0
	j = 0
	i = 1
	while i < size:
		if abs(polymer[i] - polymer[j]) != diff:
			j += 1
			polymer[j] = polymer[i]
		elif j == 0:
			i += 1
			if i == size:
				return 0
			polymer[0] = polymer[i]
		else:
			j -= 1
		i += 1

	return j + 1

def main():
	polymer = [ord(x) for x in sys.stdin.readline().rstrip()]
	assert all([(65 <= x <= 90) or (97 <= x <= 122) for x in polymer])

	size = react(polymer)
#	print(''.join([chr(x) for x in polymer[:size]]))
	print(size)

if __name__ == '__main__':
	main()
