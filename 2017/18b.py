def p0_values():
	a = 2**31 - 1
	p = 680
	q = []
	for _ in range(127):
		p = (p * 8505 % a * 129749 + 12345) % a
		q.append(p % 10000)
	return q

def main():
	rcv = p0_values()
	snd = []
	p1 = True
	p1_snd = 0

	done = False
	while not done:
		done = True
		a = rcv[0]
		for b in rcv[1:]:
			if b > a:
				snd.append(b)
				done = False
			else:
				snd.append(a)
				a = b
		snd.append(a)
		if p1: p1_snd += 127
		p1 = not p1
		rcv = snd
		snd = []

	print(p1_snd)

main()
