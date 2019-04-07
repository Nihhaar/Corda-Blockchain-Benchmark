import re
import sys
import os.path
import numpy as np
from collections import OrderedDict

def parse_read(filename, iterations):
	file = open(filename, 'r')
	lines = file.readlines()
	requests = int(len(lines)/(6*iterations))
	throughput = 0
	latency = 0
	total_time = 0
	od = OrderedDict()

	# Read metrics
	for line in lines:
		if 'RPC_REQUEST_START' in line:
			str_list = line.split()
			od[str_list[1]] = [0 for i in range(6)]
			od[str_list[1]][0] = int(str_list[2])
		if 'FLOW_START' in line:
			str_list = line.split()
			od[str_list[1]][1] = int(str_list[2])
		if 'FLOW_SEND' in line:
			str_list = line.split()
			od[str_list[1]][2] = int(str_list[2])
		if 'FLOW_RECV' in line:
			str_list = line.split()
			od[str_list[1]][3] = int(str_list[2])
		if 'FLOW_END' in line:
			str_list = line.split()
			od[str_list[1]][4] = int(str_list[2])
		if 'RPC_REQUEST_END' in line:
			str_list = line.split()
			od[str_list[1]][5] = int(str_list[2])

	# Calculate metrics averaged over iterations
	for i in range(iterations):
		subpart = list(od.keys())[requests*i : requests*(i+1)]
		latency = sum((od[key][5] - od[key][0])/1000.0 for key in subpart) / requests # in sec
		total_time += (od[subpart[-1]][5] - od[subpart[0]][0])/1000.0 # in sec
		throughput += requests/total_time # in tps

	throughput /= iterations
	latency /= iterations
	total_time /= iterations

	# Print metrics
	print()
	print('Transactions per second')
	print('-----------------------')
	print(requests, 'requests,', iterations, 'iterations')
	print('Total time:', str.format('{0:.4f}', total_time), 'sec')
	print('Latency:', str.format('{0:.4f}', latency), 'sec')
	print('Throughput:', str.format('{0:.4f}', throughput), 'tps')
	print()

def main():
	home = os.path.expanduser("~")
	initiator = os.path.join(home, 'Initiator.log')

	if len(sys.argv) != 2:
		print('Usage: python ' + sys.argv[0] + ' num_iterations')
		sys.exit(1)

	parse_read(initiator, int(sys.argv[1]))

main()