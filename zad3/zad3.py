import random

DEBUG = True

PAGES = lambda n: [i for i in range(n)]

MEM = lambda n: {
    'fifo': [i for i in range(n)],
    'rand': [i for i in range(n)],
    'lru': [(i, 0) for i in range(n)],
    'approx_lru': [(i, 0) for i in range(n)],
    'opt': [i for i in range(n)]
}

PAGE_ERRORS = {
    'fifo': 0,
    'rand': 0,
    'lru': 0,
    'approx_lru': 0,
    'opt': 0
}


def get_random_page(pages, last):
    take_local_page = random.randrange(0, 10) > 3
    if take_local_page:
        next = random.choice(pages[last:last+2])
    else:
        next = random.choice(pages)
    return next


def load_page(memories, page_num, alg, page_loads=None):
    mem = memories[alg.__name__]
    if page_loads is not None:
        alg(page_num, mem, page_loads=page_loads)
    else:
        alg(page_num, mem)


def fifo(page_num, mem):
    if page_num not in mem:
        PAGE_ERRORS['fifo'] += 1
        mem.pop(0)
        mem.append(page_num)


def rand(page_num, mem):
    if page_num not in mem:
        PAGE_ERRORS['rand'] += 1
        r = random.choice(mem)
        mem.pop(mem.index(r))
        mem.append(page_num)


def lru(page_num, mem):
    p = [i for i, time in mem]
    if page_num not in p:
        PAGE_ERRORS['lru'] += 1
        tmp = [k for k in mem]
        sort = sorted(tmp, key=lambda k: k[1], reverse=True)
        i = sort.pop(0)
        mem.pop(mem.index(i))
        mem.append((page_num, 0))
    else:
        f = list(filter(lambda k: k[0] == page_num, mem))[0]
        index = mem.index(f)
        mem[index] = (f[0], 0)
    for i in range(len(mem)):
        page = mem[i]
        mem[i] = (page[0], page[1]+1)
    #print(mem)
    #input()


def approx_lru(page_num, mem):
    p = [i for i, time in mem]
    if page_num not in p:
        PAGE_ERRORS['approx_lru'] += 1
        tmp = [k for k in mem]
        sort = sorted(tmp, key=lambda k: k[1])
        i = sort.pop(0)
        mem.pop(mem.index(i))
        for i in mem:
            mem[mem.index(i)] = (i[0], 0)
        mem.append((page_num, 1))
    else:
        f = list(filter(lambda k: k[0] == page_num, mem))[0]
        i = mem.index(f)
        mem[i] = (f[0], 1)


def generate_page_loads(pages, num):
    l = []
    seed = random.choice(pages)
    next = seed
    for i in range(num):
        next = get_random_page(pages, next)
        l.append(next)
    return l


def opt(page_num, mem, page_loads):
    if page_num not in mem:
        PAGE_ERRORS['opt'] += 1
        max_page_index = -1
        to_delete = None
        #print(mem)
        for i in mem:
            if i in page_loads:
                if page_loads.index(i) > max_page_index:
                    max_page_index = page_loads.index(i)
                    to_delete = i
            else:
                to_delete = i
        mem[mem.index(to_delete)] = page_num
        #print(MEM['opt'])
        #input()


if __name__ == '__main__':
    d = 0
    for m in [3, 5, 10, 20, 30, 50, 100]:
        k = m * (2 + d)
        d += 1
        memory = MEM(m)
        pages = PAGES(k)
        page_loads = generate_page_loads(pages, 1000)
        i = 0
        #print(page_loads)
        for next in page_loads:
            load_page(memory, next, fifo)
            load_page(memory, next, rand)
            load_page(memory, next, lru)
            load_page(memory, next, approx_lru)
            i += 1
            load_page(memory, next, opt, page_loads=page_loads[i:])
        print ("FIFO(%d, %d): %d errors" % (m, k, PAGE_ERRORS['fifo']))
        print ("RAND(%d, %d): %d errors" % (m, k, PAGE_ERRORS['rand']))
        print ("LRU(%d, %d): %d errors" % (m, k, PAGE_ERRORS['lru']))
        print ("APPROX LRU(%d, %d): %d errors" % (m, k, PAGE_ERRORS['approx_lru']))
        print ("OPT(%d, %d): %d errors" % (m, k, PAGE_ERRORS['opt']))
        print ("*********************************************")
        for k, v in PAGE_ERRORS.items():
            PAGE_ERRORS[k] = 0
