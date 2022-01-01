import re
import sys

def read_input():
	line_pattern = re.compile('^((?:[a-z]+-)+)([1-9][0-9]*)\\[([a-z]{5})\\]$')
	rooms = []
	for line_num, line in enumerate(sys.stdin, start=1):
		m = line_pattern.match(line)
		if not m:
			print(f"Input line {line_num} doesn't match the expected pattern!")
			return None
		name, sector, checksum = m.groups()
		rooms.append((name, int(sector), checksum))
	return rooms

def real_checksum(name):
	freq = [0] * 26
	for letter in name.replace('-', ''):
		freq[ord(letter) - 97] += 1
	freq = [(count, -letter) for letter, count in enumerate(freq)]
	return ''.join([chr(97 - letter)
		for count, letter in sorted(freq, reverse=True)[:5]])

def decrypt_name(name, shift):
	return ''.join([' ' if letter == '-' else
		chr(97 + (ord(letter) - 97 + shift) % 26) for letter in name])

def main():
	rooms = read_input()
	if not rooms: return

	answer1 = 0
	answer2 = None
	for name, sector, checksum in rooms:
		if checksum == real_checksum(name):
			answer1 += sector
			if 'northpole' in decrypt_name(name, sector):
				assert answer2 is None
				answer2 = sector

	print('Part 1:', answer1)
	print('Part 2:', answer2)

if __name__ == '__main__':
	main()
