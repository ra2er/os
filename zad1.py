#-*- coding: utf-8 -*-
import itertools
import os
import matplotlib.pyplot as plt
#import random
#import time

PROCESSOR_TIME = [100, 1000, 120, 40, 90, 1200, 50, 800, 100, 40, 880, 120, 50,
                  10, 100, 50, 1000, 400, 30, 330, 600, 50, 230, 440, 510, 230,
                  90, 100, 760, 120, 100, 10, 50, 90, 880, 10, 40, 20, 700, 30,
                  50, 100, 500, 230, 430, 220, 60, 750, 100, 30]


class Process(object):

    def __init__(self, pid, duration):
        # duration - czas w ms
        self.pid = pid
        self.duration = duration
        self._remaining = self.duration

    def get_remaining(self):
        return self._remaining

    def set_remaining(self, time_elapsed):
        self._remaining = self._remaining - time_elapsed


class FCFS(object):

    LOG_FILE = 'fcfs.txt'

    def __init__(self, processes):
        self.processes = processes
        self.counter = 0
        self.max_waiting_time = 0.0
        self.max_avg_wait_time = 0.0

    def run(self):
        processes_set_count = 1.0
        self.processes = sorted(self.processes, key=lambda p: p.pid)
        with open(self.LOG_FILE, 'w+') as socket:
            while len(self.processes) > 0:
                p = self.processes.pop(0)
                self.counter += 1
                self.max_waiting_time += p.duration if self.counter != 0 else 0
                avg_wait_time = self.get_avg()
                line = '%d,%f' % (self.counter, avg_wait_time)
                line += os.linesep
                socket.write(line)
                if avg_wait_time > self.max_avg_wait_time:
                    self.max_avg_wait_time = avg_wait_time
                if processes_set_count < 10 and (self.counter/processes_set_count) % 25 == 0:
                    new_processes = [Process(i+50*processes_set_count, d) for i, d in enumerate(PROCESSOR_TIME)]
                    self.processes = list(itertools.chain(self.processes, new_processes))
                    processes_set_count += 1

    def get_avg(self):
        return self.max_waiting_time / self.counter

    def get_results(self):
        with open(self.LOG_FILE, 'r') as socket:
            xlist = []
            ylist = []
            lines = socket.readlines()
            for line in lines:
                line = line.rstrip()
                fx = line.split(',')
                xlist.append(int(fx[0]))
                ylist.append(float(fx[1]))
            return xlist, ylist


class SJF(object):

    LOG_FILE = 'sjf.txt'

    def __init__(self, processes):
        self.processes = processes
        self.counter = 0
        self.max_waiting_time = 0.0
        self.max_avg_wait_time = 0.0

    def run(self):
        processes_set_count = 1.0
        self.processes = sorted(self.processes, key=lambda p: p.duration)
        # posortowanie procesów wg rosnącej długości czasu procesora
        with open(self.LOG_FILE, 'w+') as socket:
            while len(self.processes) > 0:
                p = self.processes.pop(0)
                self.counter += 1
                self.max_waiting_time += p.duration if self.counter != 0 else 0
                avg_wait_time = self.get_avg()
                line = '%d,%f' % (self.counter, avg_wait_time)
                line += os.linesep
                socket.write(line)
                if avg_wait_time > self.max_avg_wait_time:
                    self.max_avg_wait_time = avg_wait_time
                if processes_set_count < 10 and self.counter % 25 == 0:
                    new_processes = [Process(i+50*processes_set_count, d) for i, d in enumerate(PROCESSOR_TIME)]
                    self.processes = list(itertools.chain(self.processes, new_processes))
                    self.processes = sorted(self.processes, key=lambda p: p.duration)
                    processes_set_count += 1

    def get_avg(self):
        return self.max_waiting_time / self.counter

    def get_results(self):
        with open(self.LOG_FILE, 'r') as socket:
            xlist = []
            ylist = []
            lines = socket.readlines()
            for line in lines:
                line = line.rstrip()
                fx = line.split(',')
                xlist.append(int(fx[0]))
                ylist.append(float(fx[1]))
            return xlist, ylist


class SRF(object):
    """ SJF z wywłaszczeniem """
    LOG_FILE = 'srf.txt'

    def __init__(self, processes, time_quantum):
        self.processes = processes
        self.time_quantum = time_quantum
        self.counter = 0
        self.max_waiting_time = 0.0
        self.max_avg_wait_time = 0.0

    def insert_in_queue(self, process):
        for p in self.processes:
            if p.get_remaining() > process.get_remaining():
                i = self.processes.index(p)
                self.processes.insert(i+1, process)
                break

    def run(self):
        processes_set_count = 1.0
        self.processes = sorted(self.processes, key = lambda p: p.pid)
        with open(self.LOG_FILE, 'w+') as socket:
            while len(self.processes) > 0:
                p = self.processes.pop(0)
                time_elapsed = min(self.time_quantum, p.get_remaining())
                p.set_remaining(time_elapsed)
                self.max_waiting_time += time_elapsed if self.counter != 0 else 0
                next_p = self.processes[1] if len(self.processes) > 1 else None
                if next_p and next_p.get_remaining() == next_p.duration:  # proces czekał do tej chwili
                    # obliczenie średniego czasu dostępu dla tego procesu
                    self.counter += 1
                    avg_wait_time = self.get_avg()
                    line = '%d,%f' % (self.counter, avg_wait_time)
                    line += os.linesep
                    socket.write(line)
                    if avg_wait_time > self.max_avg_wait_time:
                        self.max_avg_wait_time = avg_wait_time
                if p.get_remaining() > 0:
                    self.insert_in_queue(p)
                else:
                    if p in self.processes:
                        self.processes.remove(p)
                if processes_set_count < 10 and self.counter % 25 == 0:
                    new_processes = [Process(i+50*processes_set_count, d) for i, d in enumerate(PROCESSOR_TIME)]
                    self.processes = list(itertools.chain(self.processes, new_processes))
                    processes_set_count += 1

    def get_avg(self):
        return self.max_waiting_time / self.counter

    def get_results(self):
        with open(self.LOG_FILE, 'r') as socket:
            xlist = []
            ylist = []
            lines = socket.readlines()
            for line in lines:
                line = line.rstrip()
                fx = line.split(',')
                xlist.append(int(fx[0]))
                ylist.append(float(fx[1]))
            return xlist, ylist


class RR(object):

    LOG_FILE = 'rr.txt'

    def __init__(self, processes, time_quantum):
        self.processes = processes
        self.time_quantum = time_quantum
        self.counter = 0
        self.max_waiting_time = 0.0
        self.max_avg_wait_time = 0.0

    def run(self):
        processes_set_count = 1.0
        self.processes = sorted(self.processes, key = lambda p: p.pid)
        with open(self.LOG_FILE, 'w+') as socket:
            while len(self.processes) > 0:
                p = self.processes.pop(0)
                time_elapsed = min(self.time_quantum, p.get_remaining())
                p.set_remaining(time_elapsed)
                self.max_waiting_time += time_elapsed if self.counter != 0 else 0
                #next_p = self.processes[1] if len(self.processes) > 1 else None
                self.counter += 1
                avg_wait_time = self.get_avg()
                line = '%d,%f' % (self.counter, avg_wait_time)
                line += os.linesep
                socket.write(line)
                if avg_wait_time > self.max_avg_wait_time:
                    self.max_avg_wait_time = avg_wait_time
                if p.get_remaining() > 0:
                    self.processes.append(p)
                else:
                    if p in self.processes:
                        self.processes.remove(p)
                if processes_set_count < 10 and self.counter % 25 == 0:
                    new_processes = [Process(i+50*processes_set_count, d) for i, d in enumerate(PROCESSOR_TIME)]
                    self.processes = list(itertools.chain(self.processes, new_processes))
                    processes_set_count += 1

    def get_avg(self):
        return self.max_waiting_time / self.counter

    def get_results(self):
        with open(self.LOG_FILE, 'r') as socket:
            xlist = []
            ylist = []
            lines = socket.readlines()
            for line in lines:
                line = line.rstrip()
                fx = line.split(',')
                xlist.append(int(fx[0]))
                ylist.append(float(fx[1]))
            return xlist, ylist


if __name__ == '__main__':
    processes = [Process(i, d) for i, d in enumerate(PROCESSOR_TIME)]
    fcfs = FCFS(processes)
    fcfs.run()
    fcfs_x, fcfs_y= fcfs.get_results()

    sjf = SJF(processes)
    sjf.run()
    sjf_x, sjf_y= sjf.get_results()

    srf = SRF(processes, time_quantum=100)
    srf.run()
    srf_x, srf_y= srf.get_results()

    rr = RR(processes, time_quantum=100)
    rr.run()
    rr_x, rr_y = rr.get_results()

    plt.plot(fcfs_x, fcfs_y, label='FSFS')
    plt.plot(sjf_x, sjf_y, label='SJF')
    plt.plot(srf_x, srf_y, label='SRF')
    plt.plot(rr_x, rr_y, label='RR')
    plt.legend(bbox_to_anchor=(1, 1), loc=2,
               borderaxespad=0.)
    plt.axis([1, 500, 1, 600])
    plt.xlabel('Processes count')
    plt.ylabel('Avg wait time [ms]')
    plt.show()

