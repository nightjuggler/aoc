import sys

def main(args):
	input_lookup = {
		'default': '463528179',
		'example': '389125467',
	}
	input_string = input_lookup.get(args[0], args[0]) if args else input_lookup['default']

	s = set()
	cups = []
	for c in input_string:
		c = ord(c) - 48
		assert 1 <= c <= 9
		assert c not in s
		s.add(c)
		cups.append(c)
	assert len(s) == 9

	for move in range(1, 101):
		print('move {}:'.format(move), ' '.join([str(c) for c in cups]))
		current = cups.pop(0)
		picked_up = cups[:3]
		cups[:3] = []
		cups.append(current)
		destination = current - 1
		if destination < min(cups):
			destination = max(cups)
		while True:
			for i, c in enumerate(cups):
				if c == destination:
					break
			else:
				destination -= 1
				continue
			break
		cups[i+1:i+1] = picked_up

	print('final:', ' '.join([str(c) for c in cups]))

	while (c := cups.pop(0)) != 1:
		cups.append(c)

	print(''.join([str(c) for c in cups]))

if __name__ == '__main__':
	main(sys.argv[1:])
