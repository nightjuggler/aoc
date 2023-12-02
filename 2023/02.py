import re
import sys

def read_input():
	n = '[1-9][0-9]*'
	cubes = f' {n} (?:red|green|blue)'
	subset = f'{cubes}(?:,{cubes}){{0,2}}'
	pattern = re.compile(f'^Game ({n}):({subset}(?:;{subset})*)$')
	games = []
	for line_num, line in enumerate(sys.stdin, start=1):
		m = pattern.match(line)
		if not m:
			sys.exit(f'Line {line_num} doesn\'t match pattern!')
		game, subsets = m.groups()
		if int(game) != line_num:
			sys.exit(f'Game {game} on line {line_num}?!')
		game = []
		for subset in subsets.split(';'):
			rgb = {'red': 0, 'green': 0, 'blue': 0}
			for cubes in subset.split(','):
				n, color = cubes.split()
				if rgb[color]:
					sys.exit(f'Line {line_num} subset specifies {color} more than once!')
				rgb[color] = int(n)
			game.append((rgb['red'], rgb['green'], rgb['blue']))
		games.append(game)
	return games

def part1(games):
	return sum(i for i, game in enumerate(games, start=1)
		if all(r <= 12 and g <= 13 and b <= 14 for r, g, b in game))

def power(r, g, b):
	return r * g * b

def part2(games):
	return sum(power(*map(max, zip(*game))) for game in games)

def main():
	games = read_input()
	print('Part 1:', part1(games))
	print('Part 2:', part2(games))
main()
