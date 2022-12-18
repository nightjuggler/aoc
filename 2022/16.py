from collections import deque
from heapq import heappush, heappop
from itertools import combinations
import operator
import re
import sys

def read_input():
	v = '[A-Z]{2}'
	n = '([1-9][0-9]*|0)'
	t1 = f'(?:tunnel leads to valve ({v}))'
	t2 = f'(?:tunnels lead to valves ({v}(?:, {v})+))'
	pattern = re.compile(f'^Valve ({v}) has flow rate={n}; (?:{t1}|{t2})$')
	flows = {}
	tunnels = {}
	for line_num, line in enumerate(sys.stdin, start=1):
		if not (m := pattern.match(line)):
			sys.exit(f'Line {line_num} doesn\'t match expected pattern!')
		valve, flow, t1, t2 = m.groups()
		flows[valve] = int(flow)
		tunnels[valve] = (t1 or t2).split(', ')
	return flows, tunnels

def part1(graph, flows, visited=frozenset(), time_left=30):
	q = []
	heappush(q, (0, time_left, 0, visited, flows))
	max_pressure = 0
	while q:
		pressure, time_left, valve, visited, flows = heappop(q)
		if pressure < max_pressure:
			max_pressure = pressure
		elif pressure - sum(map(operator.mul, flows, range(time_left-2, 0, -2))) >= max_pressure:
			continue
		for valve, distance, flow in graph[valve]:
			if valve in visited: continue
			next_time_left = time_left - distance - 1
			if next_time_left <= 0: continue
			next_flows = list(flows)
			del next_flows[flows.index(flow)]
			heappush(q, (pressure - flow * next_time_left, next_time_left, valve,
				visited | {valve}, tuple(next_flows)))
	return -max_pressure

def part2(graph, flows):
	valves = frozenset(valve for valve, distance, flow in graph[0])
	pressure_map = {}
	for k in range(len(valves) + 1):
		for visited in combinations(valves, k):
			visited = frozenset(visited)
			pressure_map[visited] = part1(graph, flows, visited, 26)
	return max(pressure + pressure_map[valves - visited]
		for visited, pressure in pressure_map.items())

def connect(start, flows, tunnels):
	q = deque()
	visited = {start: 0}
	q.append((start, 0))
	while q:
		valve, distance = q.popleft()
		distance += 1
		for valve in tunnels[valve]:
			if visited.get(valve, 30) <= distance: continue
			visited[valve] = distance
			q.append((valve, distance))
	return sorted((valve, distance, flow)
		for valve, distance in visited.items() if (flow := flows[valve]))

def make_graph(flows, tunnels):
	graph = [connect('AA', flows, tunnels)]
	if flows['AA']:
		edges = graph[0][1:]
		first_edge = 0
	else:
		edges = graph[0]
		first_edge = 1

	for valve, distance, flow in edges:
		graph.append(connect(valve, flows, tunnels))

	return [[(i, distance, flow)
		for i, (valve, distance, flow) in enumerate(edges, start=first_edge)]
		for edges in graph]

def main():
	flows, tunnels = read_input()
	graph = make_graph(flows, tunnels)
	flows = sorted((flow for flow in flows.values() if flow), reverse=True)
	print('Part 1:', part1(graph, flows))
	print('Part 2:', part2(graph, flows))
main()
