import sys

def react(polymer, unit):
	upper = ord('A') + unit
	lower = ord('a') + unit
	polymer = [x for x in polymer if x != upper and x != lower]
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
	return size

def main():
	polymer = [ord(x) for x in sys.stdin.readline().rstrip()]
	assert all([(65 <= x <= 90) or (97 <= x <= 122) for x in polymer])

	print(min([react(polymer, unit) for unit in range(26)]))

if __name__ == '__main__':
	main()
