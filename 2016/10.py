from collections import defaultdict, deque
import re
import sys

def read_input():
	n = '(0|[1-9][0-9]*)'
	re1 = re.compile(f'^bot {n} gives low to (bot|output) {n} and high to (bot|output) {n}$')
	re2 = re.compile(f'^value {n} goes to bot {n}$')

	bot_spec = {}
	bot_vals = defaultdict(list)
	q = deque()

	for line_num, line in enumerate(sys.stdin, start=1):
		if m := re1.match(line):
			bot, lo_type, lo, hi_type, hi = m.groups()
			bot = int(bot)
			assert bot not in bot_spec
			bot_spec[bot] = (lo_type == 'bot', int(lo), hi_type == 'bot', int(hi))
		elif m := re2.match(line):
			value, bot = m.groups()
			bot = int(bot)
			vals = bot_vals[bot]
			assert len(vals) < 2
			vals.append(int(value))
			if len(vals) == 2:
				q.append((bot, vals))
		else:
			raise SystemExit(f'Syntax error on input line {line_num}!')

	return bot_spec, bot_vals, q

def main():
	bot_spec, bot_vals, q = read_input()

	outputs = {}
	part1_vals = [17, 61]

	if len(sys.argv) == 3:
		part1_vals = sorted(map(int, sys.argv[1:]))

	def give(value, n, is_bot):
		if is_bot:
			vals = bot_vals[n]
			assert len(vals) < 2
			vals.append(value)
			if len(vals) == 2:
				q.append((n, vals))
		else:
			assert n not in outputs
			outputs[n] = value

	while q:
		bot, vals = q.popleft()
		vals.sort()
		if vals == part1_vals:
			print('Part 1:', bot)
		lo_bot, lo, hi_bot, hi = bot_spec[bot]
		give(vals[0], lo, lo_bot)
		give(vals[1], hi, hi_bot)
		vals.clear()

	print('Part 2:', outputs[0] * outputs[1] * outputs[2])

if __name__ == '__main__':
	main()
