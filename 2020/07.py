import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def traverse(graph, color, colors):
	for parent in graph.get(color, ()):
		colors.add(parent)
		traverse(graph, parent, colors)

def main():
	pattern1 = re.compile('^([a-z]+ [a-z]+) bags contain ')
	pattern2 = re.compile('1 ([a-z]+ [a-z]+) bag$')
	pattern3 = re.compile('([1-9][0-9]*) ([a-z]+ [a-z]+) bags$')

	graph = {}
	parent_colors = set()
	line_number = 0

	for line in sys.stdin:
		line_number += 1
		m = pattern1.match(line)
		if not m:
			err('Line {} doesn\'t match pattern!', line_number)
		parent_color = m.group(1)
		if parent_color in parent_colors:
			err('Line {}: Rule for {} bags was already defined!', line_number, parent_color)
		parent_colors.add(parent_color)
		if line[-2:] != '.\n':
			err('Line {} doesn\'t match pattern!', line_number)
		line = line[m.end():-2]
		if line == 'no other bags':
			continue
		colors = set()
		for line in line.split(', '):
			m = pattern2.match(line)
			if m:
				color = m.group(1)
			else:
				m = pattern3.match(line)
				if m:
					number, color = m.groups()
				else:
					err('Line {} doesn\'t match pattern!', line_number)

			if color in colors:
				err('Line {}: {} occurs more than once!', line_number, color)
			graph.setdefault(color, []).append(parent_color)
			colors.add(color)

	colors = set()
	traverse(graph, 'shiny gold', colors)
	print(len(colors))

if __name__ == '__main__':
	main()
