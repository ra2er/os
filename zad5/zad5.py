#-*- coding: utf-8 -*-
import random
#import time


class Processor(object):

    def __init__(self, n):
        self.n = n
        self.load = 0
        self.usage = 0
        self.procs = {}
        self.loads = []
        self.load_avg = 0
        self.load_checks = 0
        self.queries = 0
        self.deloads = 0

    def add_process(self, p):
        self.procs[p.pid] = p
        self.usage += p.cpu_usage
        self.load += 1

    def delete_process(self, pid):
        self.procs.pop(pid)
        self.load -= 1
        self.usage -= proc.cpu_usage

    def time_clock(self):
        to_delete = []
        for pid, proc in self.procs.items():
            proc.time -= 1
            if proc.time <= 0:
                to_delete.append(pid)
                self.load -= 1
                self.usage -= proc.cpu_usage
        for p in to_delete:
            self.procs.pop(p)

    def take_process(self, from_processor):
        procs = sorted(from_processor.procs.items(), key=lambda p: p[1].cpu_usage,  reverse=True)
        if len(procs) > 0:
            pid, process = procs[0]
            self.add_process(process)
            from_processor.delete_process(pid)
            from_processor.deloads += 1

    def __repr__(self):
        return "#: %d, Load avg: %f, Queries: %d, Deloads: %d" % (self.n, self.load_avg, self.queries, self.deloads)


class Process(object):

    def __init__(self, pid, cpu_usage, time):
        self.pid = pid
        self.cpu_usage = cpu_usage
        self.time = time


if __name__ == '__main__':
    N = 100 # ilość procesorów
    p = 50  # maksymalne obciążenie
    r = 10 # minimalne obciążenie
    z = 10 # ilość prób

    import matplotlib.pyplot as plt
    import numpy as np
    fig, ax = plt.subplots()
    ind = np.arange(0, N)

    # show the figure, but do not block
    plt.show(block=False)

    processors = [Processor(n) for n in range(N)]
    procs = [Process(i, random.randrange(1, 20), random.randrange(1, 1000)) for i in range(1000)]

    cpus = plt.bar(ind, [cpu.usage for cpu in processors])
    centers = ind + 0.5*cpus[0].get_width()
    ax.set_xlim([0, N])
    ax.set_xticks(centers)
    ax.set_ylim([0, 100])
    ax.set_xticklabels(["%d" %cpu.n for cpu in processors ])
    ax.set_ylabel('Percent usage')
    ax.set_title('System Monitor')

    tick = 0
    while len(procs) > 0:
        refresh = tick % 100 == 0
        dequeue = random.randrange(1, 100) > 70
        if dequeue:
            proc = procs.pop(0)
            processor = random.choice(processors)
            counter = 1
            def get_processor_for_process(proc, next, counter):
                if next.usage > p and counter < z:
                    next = random.choice(processors)
                    counter += 1
                    return get_processor_for_process(proc, next, counter)
                else:
                    if next.usage > p:
                        return None
                    return next
            winner = get_processor_for_process(proc, processor, counter)
            procesor = winner or processor
            processor.add_process(proc)
        high_usage_processors = list(filter(lambda cpu: cpu.usage > p, processors))
        for processor in processors:
            if tick % 100 == 0:
                processor.loads.append(processor.load)
                processor.load_checks += 1
                processor.load_avg = 1.0 * sum(processor.loads) / processor.load_checks
            if processor.usage < r and len(high_usage_processors) > 0:
                from_processor = random.choice(high_usage_processors)
                high_usage_processors.remove(from_processor)
                processor.take_process(from_processor)
                processor.queries += 1

            processor.time_clock()

            index = processors.index(processor)
            cpus[index].set_height(processor.usage)
        #if refresh:
        #    fig.canvas.draw_idle()
        #    try:
        #        fig.canvas.flush_events()
        #    except NotImplementedError:
        #        pass
        tick += 1
    for processor in processors:
        print(processor)


