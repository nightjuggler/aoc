import sys

class ParseError(Exception):
	pass

def err(message, *args):
	raise ParseError(message.format(*args))

def parse(line, i=0):
	expr = []
	c = line[i]

	while True:
		if c == '(':
			value, i = parse(line, i + 1)
			c = line[i]
		elif c == '0':
			value = 0
			i += 1
			c = line[i]
		elif c in '123456789':
			value = ord(c) - 48
			i += 1
			c = line[i]
			while c in '0123456789':
				value = 10 * value + ord(c) - 48
				i += 1
				c = line[i]
		else:
			err('Column {}: Unexpected character!', i)

		expr.append(value)

		if c == ' ':
			i += 1
			op = line[i]
			if op != '+' and op != '*':
				err('Column {}: Expected "+" or "*"!', i)
			i += 1
			if line[i] != ' ':
				err('Column {}: Expected " "!', i)
			i += 1
			c = line[i]

			expr.append(op)

		elif c == ')' or c == '\n':

			values = [expr.pop(0)]
			while expr:
				op = expr.pop(0)
				value = expr.pop(0)
				if op == '+':
					values[-1] += value
				else:
					values.append(value)
			result = values.pop(0)
			while values:
				result *= values.pop(0)

			return result if c == '\n' else (result, i + 1)
		else:
			err('Column {}: Unexpected character!', i)

def main():
	result = 0
	for line_number, line in enumerate(sys.stdin, start=1):
		if not line.endswith('\n'):
			sys.exit('Line {} doesn\'t end with a newline!'.format(line_number))
		try:
			result += parse(line)
		except ParseError as e:
			sys.exit('Line {}: {}'.format(line_number, e))
	print(result)

if __name__ == '__main__':
	main()
