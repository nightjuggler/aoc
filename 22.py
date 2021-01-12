import sys

def read_cards(input, header):
	assert next(input) == header + '\n'
	cards = []
	for line in input:
		if line == '\n':
			break
		cards.append(int(line))
	return cards

def main(input):
	p1 = read_cards(input, 'Player 1:')
	p2 = read_cards(input, 'Player 2:')

	n = 0
	while p1 and p2:
		n += 1
		print('-- Round', n, '--')
		print('Player 1\'s deck:', ', '.join([str(c) for c in p1]))
		print('Player 2\'s deck:', ', '.join([str(c) for c in p2]))
		c1 = p1.pop(0)
		c2 = p2.pop(0)
		print('Player 1 plays:', c1)
		print('Player 2 plays:', c2)
		if c1 > c2:
			print('Player 1 wins the round!')
			p1.append(c1)
			p1.append(c2)
		elif c2 > c1:
			print('Player 2 wins the round!')
			p2.append(c2)
			p2.append(c1)
		else:
			sys.exit('Both cards have the same value!')
	if p2:
		p1 = p2

	score = sum([i * c for i, c in enumerate(reversed(p1), start=1)])
	print(score)

if __name__ == '__main__':
	main(sys.stdin)
