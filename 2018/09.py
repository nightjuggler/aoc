def play(num_players, num_marbles):
	player = 0
	scores = [0] * num_players
	next_marble = [0] * num_marbles
	curr_marble = 0
	for m in range(1, num_marbles):
		if m % 23 == 0:
			a = curr_marble - 4
			r = next_marble[a]
			b = next_marble[r]
			next_marble[a] = curr_marble = b
			scores[player] += m + r
		else:
			a = next_marble[curr_marble]
			b = next_marble[a]
			next_marble[a] = curr_marble = m
			next_marble[m] = b
		player += 1
		if player == num_players:
			player = 0

	print(max(scores))

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', type=int, default=71510)
	parser.add_argument('-p', type=int, default=447)
	args = parser.parse_args()

	num_players = args.p
	num_marbles = args.m + 1

	if num_players <= 0:
		print('The number of players must be > 0!')
		return
	if num_marbles <= 0:
		print('The last marble must be >= 0!')
		return

	play(num_players, num_marbles)

if __name__ == '__main__':
	main()
