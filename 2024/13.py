import re
import sys

def read_input():
	n = '([1-9][0-9]{1,4})'
	pattern = re.compile(
		f'Button A: X\\+{n}, Y\\+{n}\\n'
		f'Button B: X\\+{n}, Y\\+{n}\\n'
		f'Prize: X={n}, Y={n}\\n?')
	configs = []
	for config_num, config_txt in enumerate(sys.stdin.read().split('\n\n'), start=1):
		m = pattern.fullmatch(config_txt)
		if not m:
			sys.exit(f'Config {config_num} doesn\'t match expected pattern!')
		configs.append(list(map(int, m.groups())))
	return configs

def main():
	add = 10_000_000_000_000
	tokens1 = tokens2 = 0
	for ax, ay, bx, by, px, py in read_input():
		d = ax*by - bx*ay
		if not d:
			sys.exit(f'{ax}*{by} - {bx}*{ay} = 0')
		a, m = divmod(px*by - bx*py, d)
		if not m:
			b, m = divmod(ax*py - px*ay, d)
			if not m:
				tokens1 += a*3 + b
		px += add
		py += add
		a, m = divmod(px*by - bx*py, d)
		if not m:
			b, m = divmod(ax*py - px*ay, d)
			if not m:
				tokens2 += a*3 + b
	print('Part 1:', tokens1)
	print('Part 2:', tokens2)

main()
