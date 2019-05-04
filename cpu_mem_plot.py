import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def main():
	save=False
	f = open('top.dat')
	times = []
	mem = []
	cpu = []

	for line in f:
		str_list = line.split()
		times.append(int(str_list[0]))
		try:
			mem.append(int(str_list[1]))
		except ValueError:
			mem.append(float(str_list[1][:-1]) * 1024 * 1024)
		cpu.append(float(str_list[2]))

	# Change time scale
	times = [(i-times[0]) for i in times]

	# Chane memory scale
	mem = [(i/1024) for i in mem]

	# Plot CPU
	#plt.plot(times, smooth(cpu, 100))
	plt.xlabel('Time (in sec)')
	plt.ylabel('CPU (in %)')
	plt.plot(times, savgol_filter(cpu, 101, 3))
	if save:
		plt.savefig('cpu_100_1.png')
	else:
		plt.show()
	plt.clf()

	# Plot Memory
	#plt.plot(times, smooth(mem, 100))
	#plt.plot(times, savgol_filter(mem, 101, 3))
	plt.xlabel('Time (in sec)')
	plt.ylabel('Memory (in MB)')
	plt.plot(times, mem)
	if save:
		plt.savefig('mem_100_1.png')
	else:
		plt.show()
	plt.clf()

main()