import sys

def main():
	p1_map = {'A':0, 'B':1, 'C':2}
	p2_map = {'X':0, 'Y':1, 'Z':2}
	total1 = 0
	total2 = 0
	for line in sys.stdin:
		p1, p2 = line.split()
		p1 = p1_map[p1]
		p2 = p2_map[p2]
		total1 += 1 + p2 + 3*((p2 - p1 + 1)%3)
		total2 += 1 + (p1 + p2 + 2)%3 + 3*p2
	print('Part 1:', total1)
	print('Part 2:', total2)

main()
