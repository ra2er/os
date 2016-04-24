#-*- coding: utf-8 -*-
import random

MEM_LENGTH = 500
PAGES_COUNT = 2000


class Process(object):

    def __init__(self, id, pages):
        self.id = id
        self.pages = pages
        self.page_errors = 0
        self.call_counter = 0
        self.last_page = None
        self.allocated_pages = []
        self.called_pages = []

    def get_random_page(self):
        if self.last_page is None:
            seed = random.choice(self.pages)
            self.last_page = seed
        take_local_page = random.randrange(0, 10) > 2 # 70%
        if take_local_page:
            try:
                next = random.choice(self.pages[self.last_page:self.last_page+2])
            except IndexError:
                next = random.choice(self.pages)
        else:
            next = random.choice(self.pages)
        self.last_page = next
        self.call_counter += 1
        return next

    def run(self, mem, mode):
        for i in range(10): # 10 odwołań na proces
            called_page = self.get_random_page()
            if called_page not in self.called_pages:
                self.called_pages.append(called_page)
            pages = [page_num for p_id, page_num, time in mem]
            if called_page not in pages:
                self.page_errors += 1
                if mode == 'proportional_allocation':
                    self.page_swap_proportional_allocation(called_page, mem)
                if mode == 'equal_allocation':
                    self.page_swap_equal_allocation(called_page, mem)
                if mode == 'error_freq':
                    self.page_swap_error_freq(called_page, mem)
                if mode == 'zone':
                    self.page_swap_zone(called_page, mem)
            else:
                f = list(filter(lambda k: k[1] == called_page, mem))[0]
                index = mem.index(f)
                mem[index] = (self.id, called_page, 0)
            # zwiększenie kwantu czasu dla wszystkich ramek
            for i in range(len(mem)):
                page = mem[i]
                mem[i] = (self.id, page[1], page[2]+1)

    def page_swap_proportional_allocation(self, called_page, mem):
        max_pages = int(1.0 * len(self.pages) / PAGES_COUNT * MEM_LENGTH)
        tmp = [k for k in mem]
        if len(self.allocated_pages) >= max_pages:
            filtered = list(filter(lambda f: f[1] in self.allocated_pages, tmp))
            sort = sorted(filtered, key=lambda k: k[2], reverse=True)
            p = sort.pop(0)
            self.allocated_pages.pop(self.allocated_pages.index(p[1]))
            i = mem.index(p)
            frame = (self.id, called_page, 0)
            mem[i] = frame
            self.allocated_pages.append(called_page)
        else:
            sort = sorted(tmp, key=lambda k: k[2], reverse=True)
            p = sort.pop(0)
            i = mem.index(p)
            frame = (self.id, called_page, 0)
            mem[i] = frame
            self.allocated_pages.append(called_page)

    def page_swap_equal_allocation(self, called_page, mem):
        max_pages = MEM_LENGTH / 10
        tmp = [k for k in mem]
        if len(self.allocated_pages) >= max_pages:
            filtered = list(filter(lambda f: f[1] in self.allocated_pages, tmp))
            sort = sorted(filtered, key=lambda k: k[2], reverse=True)
            p = sort.pop(0)
            self.allocated_pages.pop(self.allocated_pages.index(p[1]))
            i = mem.index(p)
            frame = (self.id, called_page, 0)
            mem[i] = frame
            self.allocated_pages.append(called_page)
        else:
            sort = sorted(tmp, key=lambda k: k[2], reverse=True)
            p = sort.pop(0)
            i = mem.index(p)
            frame = (self.id, called_page, 0)
            mem[i] = frame
            self.allocated_pages.append(called_page)

    def page_swap_error_freq(self, called_page, mem):
        tmp = [k for k in mem]
        pp = 100.0 * self.page_errors / self.call_counter
        if pp > 30:
            filtered = list(filter(lambda f: f[1] not in self.allocated_pages, tmp))
        else:
            filtered = list(filter(lambda f: f[1] in self.allocated_pages, tmp))
        sort = sorted(filtered, key=lambda k: k[2], reverse=True)
        p = sort.pop(0)
        try:
            self.allocated_pages.pop(self.allocated_pages.index(p[1]))
        except ValueError:
            pass
        i = mem.index(p)
        frame = (self.id, called_page, 0)
        mem[i] = frame
        self.allocated_pages.append(called_page)

    def calculate_mem_length(self):
        max_pages = int(1.0 * len(self.called_pages) / PAGES_COUNT * MEM_LENGTH)
        return max_pages

    def page_swap_zone(self, called_page, mem):
        max_pages = self.calculate_mem_length() # liczenie zbioru roboczego
        tmp = [k for k in mem]
        if max_pages >= MEM_LENGTH / 10:
            filtered = list(filter(lambda f: f[1] in self.allocated_pages, tmp))
        else:
            filtered = list(filter(lambda f: f[1] not in self.allocated_pages, tmp))
        sort = sorted(filtered, key=lambda k: k[2], reverse=True)
        p = sort.pop(0)
        try:
            self.allocated_pages.pop(self.allocated_pages.index(p[1]))
        except ValueError:
            pass
        i = mem.index(p)
        frame = (self.id, called_page, 0)
        mem[i] = frame
        self.allocated_pages.append(called_page)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    #import matplotlib.animation as animation

    plt.legend(bbox_to_anchor=(1, 1), loc=2,
               borderaxespad=0.)
    plt.axis([1, 10000, 100, 8000])
    plt.ion()
    plt.xlabel('Page call count')
    plt.ylabel('Page errors')
    #plt.yscale('log')

    procs = []
    procs.append(Process(1, [i for i in range(0, 100)]))
    procs.append(Process(2, [i for i in range(100, 300)]))
    procs.append(Process(3, [i for i in range(300, 450)]))
    procs.append(Process(4, [i for i in range(450, 750)]))
    procs.append(Process(5, [i for i in range(750, 1000)]))
    procs.append(Process(6, [i for i in range(1000, 1400)]))
    procs.append(Process(7, [i for i in range(1400, 1500)]))
    procs.append(Process(8, [i for i in range(1500, 1700)]))
    procs.append(Process(9, [i for i in range(1700, 1900)]))
    procs.append(Process(10, [i for i in range(1900, 2000)]))
    mem = [(None, None, 0) for i in range(MEM_LENGTH)]
    for i in range(100):
        for p in procs:
            p.run(mem, 'proportional_allocation')
        y = sum(p.page_errors for p in procs)
        x = sum(p.call_counter for p in procs)
        a = plt.scatter(x, y, color="r")
        plt.pause(0.05)

    print ( "Przydział proporcjonalny: ", sum(p.call_counter for p in procs), sum(p.page_errors for p in procs) )

    for p in procs:
        p.call_counter = 0
        p.page_errors = 0
        p.allocated_pages = []
        p.called_pages = []

    mem = [(None, None, 0) for i in range(MEM_LENGTH)]
    for i in range(100):
        for p in procs:
            p.run(mem, 'equal_allocation')
        y = sum(p.page_errors for p in procs)
        x = sum(p.call_counter for p in procs)
        a = plt.scatter(x, y, color="b")
        plt.pause(0.05)

    print ( "Przydział równy: ", sum(p.call_counter for p in procs), sum(p.page_errors for p in procs) )

    for p in procs:
        p.call_counter = 0
        p.page_errors = 0
        p.allocated_pages = []
        p.called_pages = []

    mem = [(None, None, 0) for i in range(MEM_LENGTH)]
    for i in range(100):
        for p in procs:
            p.run(mem, 'error_freq')
        y = sum(p.page_errors for p in procs)
        x = sum(p.call_counter for p in procs)
        a = plt.scatter(x, y, color="m")
        plt.pause(0.05)

    print ( "Sterowanie częstością błędów: ", sum(p.call_counter for p in procs), sum(p.page_errors for p in procs) )

    for p in procs:
        p.call_counter = 0
        p.page_errors = 0
        p.allocated_pages = []
        p.called_pages = []

    mem = [(None, None, 0) for i in range(MEM_LENGTH)]
    for i in range(100):
        for p in procs:
            p.run(mem, 'zone')
        y = sum(p.page_errors for p in procs)
        x = sum(p.call_counter for p in procs)
        a = plt.scatter(x, y, color="c")
        plt.pause(0.05)

    print ( "Model strefowy: ", sum(p.call_counter for p in procs), sum(p.page_errors for p in procs) )
    while True:
        plt.pause(1)

