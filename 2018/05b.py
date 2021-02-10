import sys

def react(polymer, unit):
	upper = ord('A') + unit
	lower = ord('a') + unit
	polymer = [x for x in polymer if x != upper and x != lower]
	diff = ord('a') - ord('A')

	size = len(polymer)
	if size == 0:
		return 0, unit
	j = 0
	i = 1
	while i < size:
		if abs(polymer[i] - polymer[j]) != diff:
			j += 1
			polymer[j] = polymer[i]
		elif j == 0:
			i += 1
			if i == size:
				return 0, unit
			polymer[0] = polymer[i]
		else:
			j -= 1
		i += 1

	return j + 1, unit

def main():
	polymer = [ord(x) for x in sys.stdin.readline().rstrip()]
	assert all([(65 <= x <= 90) or (97 <= x <= 122) for x in polymer])

	print(min([react(polymer, unit) for unit in range(26)]))

if __name__ == '__main__':
	main()
