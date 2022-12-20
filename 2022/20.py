import sys

def mix_once(seq, prv, nxt):
	seqlen = len(seq) - 1
	for i, steps in enumerate(seq):
		steps %= seqlen
		if not steps: continue
		old_prv = prv[i]
		old_nxt = nxt[i]
		prv[old_nxt] = old_prv
		nxt[old_prv] = old_nxt
		new_prv = old_nxt
		for _ in range(steps - 1): new_prv = nxt[new_prv]
		new_nxt = nxt[new_prv]
		prv[new_nxt] = i
		nxt[new_prv] = i
		prv[i] = new_prv
		nxt[i] = new_nxt

def mix(seq, mix_count):
	seqlen = len(seq)
	prv = list(range(-1, seqlen-1))
	prv[0] = seqlen-1
	nxt = list(range(1, seqlen+1))
	nxt[seqlen-1] = 0

	for _ in range(mix_count):
		mix_once(seq, prv, nxt)

	i = seq.index(0)
	new_seq = [0]
	while (n := seq[(i := nxt[i])]): new_seq.append(n)
	x = new_seq[1000 % seqlen]
	y = new_seq[2000 % seqlen]
	z = new_seq[3000 % seqlen]
	return f'{x} + {y} + {z} = {x + y + z}'

def main():
	seq = list(map(int, sys.stdin))
	print('Part 1:', mix(seq, 1))
	print('Part 2:', mix([811589153 * n for n in seq], 10))
main()
