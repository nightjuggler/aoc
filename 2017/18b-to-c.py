import sys

# Usage: python3 18b-to-c.py < data/18.input > 18.c && clang -Ofast 18.c && ./a.out

def is_int(x): return x == str(int(x))
def is_reg(x): return len(x) == 1 and 97 <= ord(x) <= 122

def read_input():
	code = []
	ops_no_y = ('snd', 'rcv')
	ops_int_x = ('snd', 'jgz')

	for i, line in enumerate(sys.stdin):
		op, x, *y = line.split()
		assert len(op) == 3
		if is_reg(x):
			x = f'r[{ord(x) - 97}]'
		else:
			assert is_int(x)
			assert op in ops_int_x
		if not y:
			assert op in ops_no_y
		else:
			assert len(y) == 1
			assert op not in ops_no_y
			y, = y
			if is_reg(y):
				y = f'r[{ord(y) - 97}]'
			else:
				assert is_int(y)

		if   op == 'snd': code.append(f'SND({i}, {x})')
		elif op == 'set': code.append(f'{x} = {y};')
		elif op == 'add': code.append(f'{x} += {y};')
		elif op == 'mul': code.append(f'{x} *= {y};')
		elif op == 'mod': code.append(f'{x} %= {y};')
		elif op == 'rcv': code.append(f'RCV({i}, {x})')
		elif op == 'jgz': code.append(f'if ({x} > 0) {{ ip = {i} + {y}; goto top; }}')
		else:
			sys.exit(f'Unknown instruction on line {i+1}!')
	return code

def main():
	code = read_input()

	print('''#include <stdio.h>
#include <string.h>
typedef long long reg_t;
typedef unsigned int uint;
#define MAX_QUEUE_DEPTH 64
typedef struct {
	uint ip;
	reg_t regs[26];
	reg_t queue[MAX_QUEUE_DEPTH];
	uint queue_depth;
	uint send_count;
	int waiting; /* 0 = not waiting, 1 = waiting to send; 2 = waiting to receive */
} state_t;
int snd(int p, state_t *states, reg_t value)
{
	state_t *snd_state = &states[p];
	state_t *rcv_state = &states[!p];
	if (rcv_state->queue_depth == MAX_QUEUE_DEPTH) {
		if (rcv_state->waiting == 1 && snd_state->queue_depth == MAX_QUEUE_DEPTH) {
			printf("Both programs are waiting to send!\\n");
			return -1;
		}
		snd_state->waiting = 1;
		rcv_state->waiting = 0;
		return 1;
	}
	rcv_state->queue[rcv_state->queue_depth++] = value;
	snd_state->send_count++;
	return 0;
}
int rcv(int p, state_t *states, reg_t *reg)
{
	state_t *rcv_state = &states[p];
	state_t *snd_state = &states[!p];
	if (!rcv_state->queue_depth) {
		if (snd_state->waiting == 2 && !snd_state->queue_depth) {
			printf("Both programs are waiting to receive!\\n");
			return -1;
		}
		rcv_state->waiting = 2;
		snd_state->waiting = 0;
		return 1;
	}
	reg_t *q = rcv_state->queue;
	*reg = *q;
	memmove(q, q + 1, --rcv_state->queue_depth * sizeof(reg_t));
	return 0;
}
#define SNDRCV(i, f, x) \\
	if ((swap = f(p, states, x)) < 0) break; \\
	if (swap) { states[p].ip = i; p = !p; goto init; }
#define SND(i, x) SNDRCV(i, snd, x)
#define RCV(i, x) SNDRCV(i, rcv, &x)
uint play()
{
	static state_t states[2];
	int p, swap;
	uint ip;
	reg_t *r;

	states[1].regs['p' - 'a'] = 1;
	p = 0;

init:	ip = states[p].ip;
	r = states[p].regs;

top:	switch (ip) {''')

	for i, line in enumerate(code):
		print(f'\t\tcase {i}:', line)

	print('''	}
	return states[1].send_count;
}
int main(int argc, char *argv[])
{
	printf("Part 2: %u\\n", play());
	return 0;
}''')

main()
