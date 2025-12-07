from collections import defaultdict
import sys
def main():
	lines = [{i for i, c in enumerate(line.strip()) if c != '.'} for line in sys.stdin]
	beams = {beam: 1 for beam in lines.pop(0)}
	splits = 0
	for line in lines:
		if not line: continue
		new_beams = defaultdict(int)
		for beam, timelines in beams.items():
			if beam in line:
				splits += 1
				new_beams[beam-1] += timelines
				new_beams[beam+1] += timelines
			else:
				new_beams[beam] += timelines
		beams = new_beams
	print('Part 1:', splits)
	print('Part 2:', sum(beams.values()))
main()
