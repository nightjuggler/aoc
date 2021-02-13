import sys

def main():
	data = map(int, sys.stdin.readline().split())

	def node_value():
		num_children = next(data)
		num_metadata = next(data)
		if num_children == 0:
			return sum([next(data) for i in range(num_metadata)])

		child_values = [node_value() for i in range(num_children)]
		value = 0
		for i in range(num_metadata):
			child_index = next(data) - 1
			if 0 <= child_index < num_children:
				value += child_values[child_index]
		return value

	value = node_value()
	assert len(list(data)) == 0
	print(value)

if __name__ == '__main__':
	main()
