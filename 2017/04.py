import re
import sys

def read_input():
	pattern = re.compile('^[a-z]+(?: [a-z]+)*$')
	phrases = []
	for line_num, line in enumerate(sys.stdin, start=1):
		if not pattern.match(line):
			sys.exit(f'Line {line_num} doesn\'t match expected pattern!')
		phrases.append(line.split())
	return phrases

def count_valid(phrases, no_anagrams=False):
	num_valid = 0
	for phrase in phrases:
		words = set()
		for word in phrase:
			if no_anagrams:
				word = ''.join(sorted(word))
			if word in words: break
			words.add(word)
		else:
			num_valid += 1
	return num_valid

def main():
	phrases = read_input()
	print('Part 1:', count_valid(phrases))
	print('Part 2:', count_valid(phrases, no_anagrams=True))

if __name__ == '__main__':
	main()
