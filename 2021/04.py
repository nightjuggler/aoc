import sys

def read_input():
	input = sys.stdin
	line = input.readline()
	numbers = list(map(int, line.split(',')))
	boards = []

	for line in input:
		assert line == '\n'
		board = []
		for i in range(5):
			line = input.readline()
			board.append(list(map(int, line.split())))
		boards.append(board)

	return numbers, boards

def score(board):
	return sum([n for row in board for n in row if n >= 0])

def sum_column(board, i):
	return sum([row[i] for row in board])

def main():
	numbers, boards = read_input()
	first_score = None
	last_score = None

	for n in numbers:
		assert n >= 0
		keep_boards = []
		for board in boards:
			win = False
			for row in board:
				for i, m in enumerate(row):
					if n == m:
						row[i] = -1
						if sum(row) == -5 or sum_column(board, i) == -5:
							win = True
			if win:
				last_score = n * score(board)
				if first_score is None:
					first_score = last_score
			else:
				keep_boards.append(board)
		boards = keep_boards

	print('First score (Part 1):', first_score)
	print('Last score (Part 2):', last_score)

if __name__ == '__main__':
	main()
