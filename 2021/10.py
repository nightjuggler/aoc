import sys

def median(scores):
	if len(scores) % 2 == 0:
		return None
	scores.sort()
	return scores[len(scores) // 2]

def main(verbose=False):
	open_to_close = {
		'(': ')',
		'[': ']',
		'{': '}',
		'<': '>',
	}
	paren_to_syntax_error_score = {
		')': 3,
		']': 57,
		'}': 1197,
		'>': 25137,
	}
	paren_to_autocomplete_score = {
		')': 1,
		']': 2,
		'}': 3,
		'>': 4,
	}
	syntax_error_score = 0
	autocomplete_scores = []

	for y, line in enumerate(sys.stdin):
		parens = []
		for x, c in enumerate(line.rstrip()):
			if c in '([{<':
				parens.append(open_to_close[c])
				continue
			if not parens:
				print(f'Unexpected character on line {y}, column {x}!')
				return
			if c != parens.pop():
				score = paren_to_syntax_error_score.get(c)
				if not score:
					print(f'Unexpected character on line {y}, column {x}!')
					return
				syntax_error_score += score
				break
		else:
			score = 0
			for c in parens[::-1]:
				score *= 5
				score += paren_to_autocomplete_score[c]
			if verbose:
				print(''.join(parens[::-1]), '-', score)
			autocomplete_scores.append(score)

	print('Part 1: syntax error score =', syntax_error_score)
	print('Part 2: median autocomplete score =', median(autocomplete_scores))

if __name__ == '__main__':
	main()
