import sys

def read_cards(input, header):
	assert next(input) == header + '\n'
	cards = []
	for line in input:
		if line == '\n':
			break
		cards.append(int(line))
	return cards

def win(player_num, deck, card1, card2, round_num, game_num):
	print('Player {} wins round {} of game {}!'.format(player_num, round_num, game_num))
	deck.append(card1)
	deck.append(card2)

GAME_NUM = 0

def play(p1, p2):
	global GAME_NUM
	GAME_NUM += 1
	game_num = GAME_NUM
	print('=== Game {} ==='.format(game_num))

	prev_decks = set()
	round_num = 0
	while p1 and p2:
		round_num += 1
		print('\n-- Round {} (Game {}) --'.format(round_num, game_num))
		print('Player 1\'s deck:', ', '.join([str(c) for c in p1]))
		print('Player 2\'s deck:', ', '.join([str(c) for c in p2]))
		decks = (tuple(p1), tuple(p2))
		if decks in prev_decks:
			print('The winner of game {} is player 1!\n'.format(game_num))
			return True
		prev_decks.add(decks)
		c1 = p1.pop(0)
		c2 = p2.pop(0)
		print('Player 1 plays:', c1)
		print('Player 2 plays:', c2)
		if c1 <= len(p1) and c2 <= len(p2):
			print('Playing a sub-game to determine the winner...\n')
			if play(p1[:c1], p2[:c2]):
				win(1, p1, c1, c2, round_num, game_num)
			else:
				win(2, p2, c2, c1, round_num, game_num)
		elif c1 > c2:
			win(1, p1, c1, c2, round_num, game_num)
		elif c2 > c1:
			win(2, p2, c2, c1, round_num, game_num)
		else:
			sys.exit('Both cards have the same value!')

	print('The winner of game {} is player {}!\n'.format(game_num, 1 if p1 else 2))
	return bool(p1)

def main(input):
	p1 = read_cards(input, 'Player 1:')
	p2 = read_cards(input, 'Player 2:')
	player1_wins = play(p1, p2)

	print(sum([i * c for i, c in enumerate(reversed(p1 if player1_wins else p2), start=1)]))

if __name__ == '__main__':
	main(sys.stdin)
