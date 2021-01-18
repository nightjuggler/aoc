import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def traverse(graph, parent_color):
	count = 0
	for number, color in graph.get(parent_color, ()):
		count += number + number * traverse(graph, color)
	return count

def main():
	pattern1 = re.compile('^([a-z]+ [a-z]+) bags contain ')
	pattern2 = re.compile('1 ([a-z]+ [a-z]+) bag$')
	pattern3 = re.compile('([1-9][0-9]*) ([a-z]+ [a-z]+) bags$')

	graph = {}
	line_number = 0

	for line in sys.stdin:
		line_number += 1
		m = pattern1.match(line)
		if not m:
			err('Line {} doesn\'t match pattern!', line_number)
		parent_color = m.group(1)
		if parent_color in graph:
			err('Line {}: Rule for "{}" bags was already defined!', line_number, color)
		graph[parent_color] = contents = []
		if line[-2:] != '.\n':
			err('Line {} doesn\'t match pattern!', line_number)
		line = line[m.end():-2]
		if line == 'no other bags':
			continue
		colors = set()
		for line in line.split(', '):
			m = pattern2.match(line)
			if m:
				number, color = 1, m.group(1)
			else:
				m = pattern3.match(line)
				if m:
					number, color = int(m.group(1)), m.group(2)
				else:
					err('Line {} doesn\'t match pattern!', line_number)

			if color in colors:
				err('Color "{}" occurs more than once on line {}!', color, line_number)
			colors.add(color)

			contents.append((number, color))

	print(traverse(graph, 'shiny gold'))

if __name__ == '__main__':
	main()
