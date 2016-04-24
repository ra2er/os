import os
import matplotlib.pyplot as plt
import random


class Disk(object):

    BLOCK_MOVE_TIME = 1 # ms

    def __init__(self, blocksCount):
        self.tasks = []
        self.disk = [i for i in range(blocksCount)]
        for i in range(100):
            self.tasks.append(random.choice(self.disk))

    def fcfs(self, add_realtime_process=False):
        prefix = 'with_realtime_process_' if add_realtime_process else ''
        position = 500
        time_elapsed = 0
        num = 0
        with open(prefix+'fcfs.txt', 'w+') as socket:
            for task in self.tasks:
                if num%10 == 0 and add_realtime_process:
                    priority_task = random.choice(self.disk) # proces piorytetowy wymagający natychmiastowej obsługi
                    time = abs(priority_task-position) * self.BLOCK_MOVE_TIME
                    time_elapsed += time
                    position = priority_task
                    line = '%d,%d,%d,%d' % (num, priority_task, time, time_elapsed)
                    line += os.linesep
                    socket.write(line)
                    num += 1
                time = abs(task-position) * self.BLOCK_MOVE_TIME
                time_elapsed += time
                position = task
                line = '%d,%d,%d,%d' % (num, task, time, time_elapsed)
                line += os.linesep
                socket.write(line)
                num += 1

    def sstf(self, add_realtime_process=False):
        prefix = 'with_realtime_process_' if add_realtime_process else ''
        position = 500
        def find_nearest(l, val):
            return min(l, key=lambda i: abs(val-i))

        time_elapsed = 0
        num = 0
        tasks = [t for t in self.tasks]
        with open(prefix+'sstf.txt', 'w+') as socket:
            while len(tasks) > 0:
                if num%10 == 0 and add_realtime_process:
                    priority_task = random.choice(self.disk) # proces piorytetowy wymagający natychmiastowej obsługi
                    time = abs(priority_task-position) * self.BLOCK_MOVE_TIME
                    time_elapsed += time
                    position = priority_task
                    line = '%d,%d,%d,%d' % (num, priority_task, time, time_elapsed)
                    line += os.linesep
                    socket.write(line)
                    num += 1
                nearest = find_nearest(tasks, position)
                time = abs(nearest-position) * self.BLOCK_MOVE_TIME
                time_elapsed += time
                position = nearest
                line = '%d,%d,%d,%d' % (num, nearest, time, time_elapsed)
                line += os.linesep
                socket.write(line)
                num += 1
                tasks.pop(tasks.index(nearest))

    def scan(self, add_realtime_process=False):
        prefix = 'with_realtime_process_' if add_realtime_process else ''
        position = 500
        time_elapsed = 0
        num = 0
        tasks = [t for t in self.tasks]
        scan_f = True
        with open(prefix+'scan.txt', 'w+') as socket:
            while len(tasks) > 0:
                if num%10 == 0 and add_realtime_process:
                    priority_task = random.choice(self.disk) # proces piorytetowy wymagający natychmiastowej obsługi
                    time = abs(priority_task-position) * self.BLOCK_MOVE_TIME
                    time_elapsed += time
                    position = priority_task
                    line = '%d,%d,%d,%d' % (num, priority_task, time, time_elapsed)
                    line += os.linesep
                    socket.write(line)
                    num += 1
                time = self.BLOCK_MOVE_TIME
                if position == len(self.disk) - 1:
                    scan_f = False
                elif position == 0:
                    scan_f = True
                if scan_f:
                    position += 1
                else:
                    position -= 1
                time_elapsed += time
                if position in tasks:
                    line = '%d,%d,%d,%d' % (num, position, time, time_elapsed)
                    line += os.linesep
                    socket.write(line)
                    tasks.pop(tasks.index(position))
                    num += 1

    def c_scan(self, add_realtime_process=False):
        prefix = 'with_realtime_process_' if add_realtime_process else ''
        position = 500
        time_elapsed = 0
        num = 0
        tasks = [t for t in self.tasks]
        with open(prefix+'c_scan.txt', 'w+') as socket:
            while len(tasks) > 0:
                if num%10 == 0 and add_realtime_process:
                    priority_task = random.choice(self.disk) # proces piorytetowy wymagający natychmiastowej obsługi
                    time = abs(priority_task-position) * self.BLOCK_MOVE_TIME
                    time_elapsed += time
                    position = priority_task
                    line = '%d,%d,%d,%d' % (num, priority_task, time, time_elapsed)
                    line += os.linesep
                    socket.write(line)
                    num += 1
                if position == len(self.disk) - 1:
                    time = len(self.disk) * self.BLOCK_MOVE_TIME
                    position = 0
                else:
                    time = self.BLOCK_MOVE_TIME
                    position += 1
                time_elapsed += time
                if position in tasks:
                    line = '%d,%d,%d,%d' % (num, position, time, time_elapsed)
                    line += os.linesep
                    socket.write(line)
                    tasks.pop(tasks.index(position))
                    num += 1

    def get_results(self, file_name):
        with open(file_name, 'r') as socket:
            xlist = []
            ylist = []
            lines = socket.readlines()
            for line in lines:
                line = line.rstrip()
                fx = line.split(',')
                xlist.append(int(fx[0]))
                ylist.append(float(fx[3]))
            return xlist, ylist


if __name__ == '__main__':
    disk = Disk(1000)
    disk.fcfs()
    disk.sstf()
    disk.scan()
    disk.c_scan()
    disk.fcfs(True)
    disk.sstf(True)
    disk.scan(True)
    disk.c_scan(True)
    for f in ['fcfs.txt', 'with_realtime_process_fcfs.txt',
              'sstf.txt', 'with_realtime_process_sstf.txt',
              'scan.txt', 'with_realtime_process_scan.txt',
              'c_scan.txt', 'with_realtime_process_c_scan.txt']:
        x, y = disk.get_results(f)
        plt.plot(x, y, label=f)
    plt.legend(bbox_to_anchor=(1, 1), loc=2,
               borderaxespad=0.)
    plt.axis([1, 100, 10, 35000])
    plt.xlabel('Processes count')
    plt.ylabel('Time elapsed [ms]')
    plt.yscale('log')
    plt.show()


