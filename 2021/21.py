from collections import deque

def part1(pos1, pos2):
	score1, score2 = 0, 0
	die, rolls = 0, 0

	while True:
		pos1 = (pos1 + 3*die + 6) % 10 or 10
		score1 += pos1
		die = (die + 3) % 10
		rolls += 3
		if score1 >= 1000:
			losing_score = score2
			break
		pos2 = (pos2 + 3*die + 6) % 10 or 10
		score2 += pos2
		die = (die + 3) % 10
		rolls += 3
		if score2 >= 1000:
			losing_score = score1
			break

	print('Part 1:', losing_score, '*', rolls, '=', losing_score * rolls)

def roll_sum_counts():
	rolls = (1, 2, 3)
	roll_sums = {}
	for r1 in rolls:
		for r2 in rolls:
			for r3 in rolls:
				r = r1 + r2 + r3
				roll_sums[r] = roll_sums.get(r, 0) + 1
	return tuple(roll_sums.items())

def process_queue(pos):
	roll_sums = roll_sum_counts()
	wins = [0] * 21
	not_wins = [0] * 21
	q = deque()
	q.append((0, 1, pos, 0))

	while q:
		turn, univ, pos, score = q.popleft()

		for r, u in roll_sums:
			new_univ = univ * u
			new_pos = (pos + r) % 10 or 10
			new_score = score + new_pos
			if new_score >= 21:
				wins[turn] += new_univ
			else:
				not_wins[turn] += new_univ
				q.append((turn + 1, new_univ, new_pos, new_score))
	return wins, not_wins

def part2(pos1, pos2):
	p1_wins, p1_not_wins = process_queue(pos1)
	p2_wins, p2_not_wins = process_queue(pos2)

	u1 = sum([u * p2_not_wins[i-1] # i > 0 implied since one can't win on the first turn
		for i, u in enumerate(p1_wins) if u])
	u2 = sum([u * p1_not_wins[i]
		for i, u in enumerate(p2_wins) if u])

	print('Player 1 wins in', u1, 'universes')
	print('Player 2 wins in', u2, 'universes')
	print('Part 2:', max(u1, u2))

def main():
#	pos1, pos2 = 4, 8
	pos1, pos2 = 6, 7

	part1(pos1, pos2)
	part2(pos1, pos2)

if __name__ == '__main__':
	main()
