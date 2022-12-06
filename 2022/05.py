import re
import sys

def top_crates(stacks):
	return ''.join([stack[-1] if stack else '_' for stack in stacks])

def select1(crates): return crates[::-1]
def select2(crates): return crates

def process(stacks, moves, select):
	for move_num, (qty, src, dst) in enumerate(moves, start=1):
		src_stack = stacks[src]
		if qty > len(src_stack):
			sys.exit(f'Move {move_num}: Stack {src} has {len(src_stack)} crates. Cannot move {qty}!')
		stacks[dst] += select(src_stack[-qty:])
		stacks[src] = src_stack[:-qty]
	return top_crates(stacks)

def read_stacks(f):
	pattern = re.compile('^(?:\\[[A-Z]\\]|   )(?: \\[[A-Z]\\]|    ){0,8}$')
	stacks = []
	for line_num, line in enumerate(f, start=1):
		line = line.rstrip('\r\n')
		if not (m := pattern.match(line)): break
		if not stacks:
			stacks.extend(c if c != ' ' else '' for c in line[1::4])
		else:
			for i, c in enumerate(line[1::4]):
				if c != ' ': stacks[i] = c + stacks[i]
	else:
		sys.exit('Unexpected end of input file!')

	expected_line = ' '.join([format(i, '^3') for i in range(1, len(stacks)+1)])
	if not stacks or line != expected_line:
		sys.exit(f'Line {line_num} doesn\'t match expected pattern!')
	line_num += 1
	if f.readline().strip():
		sys.exit(f'Line {line_num} doesn\'t match expected pattern!')

	return stacks, line_num

def read_moves(f, line_num, num_stacks):
	pattern = re.compile('^move ([1-9][0-9]*) from ([1-9]) to ([1-9])$')
	moves = []
	for line_num, line in enumerate(f, start=line_num+1):
		if not (m := pattern.match(line)):
			sys.exit(f'Line {line_num}: Expected move <qty> from <src> to <dst>')
		qty, src, dst = map(int, m.groups())
		if src > num_stacks or dst > num_stacks:
			sys.exit(f'Line {line_num}: Expected stack number between 1 and {num_stacks}')
		moves.append((qty, src-1, dst-1))
	return moves

def main(f):
	stacks, line_num = read_stacks(f)
	moves = read_moves(f, line_num, len(stacks))

	print('Part 1:', process(stacks.copy(), moves, select1))
	print('Part 2:', process(stacks, moves, select2))

main(sys.stdin)
